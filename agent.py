"""
LiveKit Voice Agent reworked as a real-time German to English translator
with transcript streaming and recommendation generation.
"""

import asyncio
import json
import logging
import os
from typing import List, Optional
from textwrap import dedent

from dotenv import load_dotenv
from openai import AsyncOpenAI, APIError

load_dotenv()

logger = logging.getLogger("edy-translator")
logger.setLevel(logging.INFO)

from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli
from livekit.agents.metrics import EOUMetrics, LLMMetrics, STTMetrics, TTSMetrics
from livekit.plugins import elevenlabs, openai, silero


class TranslationState:
    """In-memory buffer for the ongoing conversation."""

    def __init__(self) -> None:
        self.turns: List[dict] = []
        self.partial: Optional[str] = None

    def add_turn(self, german: str, english: str) -> None:
        self.turns.append({"de": german, "en": english})
        self.partial = None

    def update_partial(self, german: str) -> None:
        self.partial = german

    def as_prompt(self, max_turns: int = 12) -> str:
        history = self.turns[-max_turns:]
        lines = []
        for turn in history:
            lines.append(f"German: {turn['de']}")
            lines.append(f"English: {turn['en']}")
        if self.partial:
            lines.append(f"Ongoing German (partial): {self.partial}")
        return "\n".join(lines)


class EdyTranslatorAgent(Agent):
    """
    Voice agent focused on simultaneous translation.

    Listens to German speech, produces English translations, publishes structured
    transcript updates to the LiveKit data channel, and periodically surfaces
    OpenAI-generated recommendations about the discussion.
    """

    def __init__(self) -> None:
        self.translation_model = os.getenv("TRANSLATION_MODEL", "gpt-4o-mini")
        self.recommendation_model = os.getenv("RECOMMENDATION_MODEL", "gpt-4o")
        self._openai = AsyncOpenAI()

        self.state = TranslationState()
        self._recommendation_lock = asyncio.Lock()
        self._recommendation_task: Optional[asyncio.Task] = None
        self._agent_session: Optional[AgentSession] = None

        llm = openai.LLM(model=self.translation_model)
        stt = openai.STT(model="whisper-1", language="de")
        tts = elevenlabs.TTS(
            voice_id=os.getenv("ELEVEN_VOICE_ID", "rachel"), model="eleven_flash_v2"
        )
        vad = silero.VAD.load()

        super().__init__(
            instructions=dedent(
                """
                You are a simultaneous interpreter. Your only task is to translate what you
                hear from German into fluent, idiomatic English. Return only the English
                translation without commentary, filler, apologies, or markup.
                """
            ).strip(),
            stt=stt,
            llm=llm,
            tts=tts,
            vad=vad,
        )

        llm.on("metrics_collected", self._llm_metrics_wrapper)
        stt.on("metrics_collected", self._stt_metrics_wrapper)
        stt.on("eou_metrics_collected", self._eou_metrics_wrapper)
        stt.on("transcript", self._stt_transcript_wrapper)
        tts.on("metrics_collected", self._tts_metrics_wrapper)

        logger.info("✅ STT transcript handler registered")

    def _llm_metrics_wrapper(self, metrics: LLMMetrics):
        asyncio.create_task(self.on_llm_metrics_collected(metrics))

    def _stt_metrics_wrapper(self, metrics: STTMetrics):
        asyncio.create_task(self.on_stt_metrics_collected(metrics))

    def _eou_metrics_wrapper(self, metrics: EOUMetrics):
        asyncio.create_task(self.on_eou_metrics_collected(metrics))

    def _tts_metrics_wrapper(self, metrics: TTSMetrics):
        asyncio.create_task(self.on_tts_metrics_collected(metrics))

    async def on_llm_metrics_collected(self, metrics: LLMMetrics) -> None:
        logger.info(
            "LLM Metrics - Tokens: %s | Speed: %.2f tok/s | TTFT: %.3fs",
            metrics.completion_tokens,
            metrics.tokens_per_second,
            metrics.ttft,
        )

    async def on_stt_metrics_collected(self, metrics: STTMetrics) -> None:
        logger.info(
            "STT Metrics - Duration: %.3fs | Audio: %.3fs",
            metrics.duration,
            metrics.audio_duration,
        )

    async def on_eou_metrics_collected(self, metrics: EOUMetrics) -> None:
        logger.info(
            "EOU Metrics - VAD Delay: %.3fs | Transcript Delay: %.3fs",
            metrics.end_of_utterance_delay,
            metrics.transcription_delay,
        )

    async def on_tts_metrics_collected(self, metrics: TTSMetrics) -> None:
        logger.info(
            "TTS Metrics - TTFB: %.3fs | Duration: %.3fs | Audio: %.3fs",
            metrics.ttfb,
            metrics.duration,
            metrics.audio_duration,
        )

    async def on_session_started(self, session: AgentSession) -> None:  # type: ignore[override]
        self._agent_session = session
        logger.info("✅ Translator agent session ready (session=%s)", session)
        logger.info("✅ Agent session stored in self._agent_session")

    def _stt_transcript_wrapper(self, transcript):
        asyncio.create_task(self._handle_transcript_event(transcript))

    async def _handle_transcript_event(self, transcript) -> None:
        text = getattr(transcript, "text", "") or getattr(transcript, "transcript", "")
        if not text:
            logger.debug("Empty transcript, skipping")
            return

        is_final = bool(
            getattr(transcript, "is_final", getattr(transcript, "final", False))
        )

        logger.info("📝 Transcript received: '%s' (final=%s)", text[:50], is_final)

        if not is_final:
            self.state.update_partial(text)

        translation = await self._translate_text(text, is_final=is_final)
        logger.info("🔄 Translation: '%s' → '%s'", text[:30], translation[:30])

        await self._publish_transcript(
            german=text, english=translation, is_final=is_final
        )

        if is_final:
            self.state.add_turn(german=text, english=translation)
            await self._schedule_recommendation_update()

    async def _translate_text(self, german_text: str, is_final: bool) -> str:
        temperature = 0.1 if is_final else 0.3
        try:
            response = await self._openai.chat.completions.create(
                model=self.translation_model,
                temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Translate the user's German sentence into English. "
                            "Respond with the English translation only."
                        ),
                    },
                    {"role": "user", "content": german_text},
                ],
            )
            english = (
                response.choices[0].message.content.strip()
                if response.choices
                else ""
            )
        except APIError as exc:
            logger.exception("Translation request failed: %s", exc)
            english = ""

        return english or "[translation unavailable]"

    async def _publish_transcript(
        self, german: str, english: str, is_final: bool
    ) -> None:

        if not self._agent_session:
            logger.warning("⚠️ No agent session available, cannot publish transcript")
            return

        payload = json.dumps(
            {
                "type": "transcript",
                "german": german,
                "english": english,
                "final": is_final,
            }
        ).encode("utf-8")

        logger.info("📡 Publishing transcript to data channel (size=%d bytes)", len(payload))
        await self._agent_session.publish_data(payload, topic="translator")
        logger.info("✅ Transcript published successfully")

    async def _schedule_recommendation_update(self) -> None:
        if self._recommendation_task and not self._recommendation_task.done():
            self._recommendation_task.cancel()

        self._recommendation_task = asyncio.create_task(self._update_recommendations())

    async def _update_recommendations(self) -> None:
        async with self._recommendation_lock:
            if not self._agent_session or not self.state.turns:
                return

            conversation_window = self.state.as_prompt()
            try:
                response = await self._openai.chat.completions.create(
                    model=self.recommendation_model,
                    temperature=0.4,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You analyze bilingual meeting transcripts. "
                                "Return concise English recommendations about "
                                "next steps, risks, and opportunities based on the conversation. "
                                "Use short bullet points (max 5) and avoid repetition."
                            ),
                        },
                        {
                            "role": "user",
                            "content": conversation_window,
                        },
                    ],
                )
                recommendations = (
                    response.choices[0].message.content.strip()
                    if response.choices
                    else ""
                )
            except APIError as exc:
                logger.exception("Recommendation generation failed: %s", exc)
                recommendations = ""

            if not recommendations:
                return

            payload = json.dumps(
                {
                    "type": "recommendations",
                    "content": recommendations,
                }
            ).encode("utf-8")

            await self._agent_session.publish_data(payload, topic="translator")


async def entrypoint(ctx: JobContext):
    """
    Main entrypoint for the agent worker.
    Connects to LiveKit room and starts the translator session.
    """

    logger.info("Connecting to room: %s", ctx.room.name)

    await ctx.connect()

    session = AgentSession()
    agent = EdyTranslatorAgent()
    agent._agent_session = session

    await session.start(
        agent=agent,
        room=ctx.room,
    )

    logger.info("Translator agent session started successfully")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        ),
    )


