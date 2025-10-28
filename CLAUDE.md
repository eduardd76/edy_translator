# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a real-time German-to-English translation voice agent built with LiveKit Agents framework. The system consists of:
- A Python agent (`agent.py`) that performs simultaneous translation and generates conversation recommendations
- A web frontend (`index.html`) hosted on Netlify
- A serverless token generation function for LiveKit authentication
- Azure Container Apps deployment with scale-to-zero capability

## Architecture

```
User Browser (index.html)
    ↓
Netlify Function (get-token.js) → Generates LiveKit token
    ↓
LiveKit Cloud
    ↓
Azure Container App (agent.py) → Translation + Recommendations
```

The agent:
1. Listens to German speech via LiveKit STT (OpenAI Whisper)
2. Translates to English using GPT-4o-mini
3. Speaks English translation via ElevenLabs TTS
4. Publishes structured transcript updates to LiveKit data channel
5. Periodically generates OpenAI-powered recommendations based on conversation

## Development Commands

### Local Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables (copy from .env.example)
cp .env.example .env
# Edit .env with your credentials

# Run agent locally
python agent.py start

# Or use setup script to create .env
./setup.sh
```

### Testing
The agent connects to LiveKit rooms automatically when users join. Test by:
1. Opening index.html in browser (or deploying to Netlify)
2. Starting a conversation
3. Monitoring agent logs for translation activity

### Deployment

#### Deploy to Azure Container Apps
```bash
# Set environment variables first
export LIVEKIT_URL=wss://your-project.livekit.cloud
export LIVEKIT_API_KEY=your_key
export LIVEKIT_API_SECRET=your_secret
export OPENAI_API_KEY=your_key
export ELEVEN_API_KEY=your_key

# Run deployment script
./deploy-azure.sh
```

#### Deploy Frontend to Netlify
1. Push code to GitHub
2. Import repository in Netlify
3. Add environment variables in Netlify dashboard:
   - LIVEKIT_URL
   - LIVEKIT_API_KEY
   - LIVEKIT_API_SECRET

#### Update Deployed Agent
```bash
# Rebuild image
az acr build --registry edyagentacr --image edy-agent:latest --file Dockerfile .

# Update container app
az containerapp update \
  --name edy-agent \
  --resource-group edy-agent-rg \
  --image edyagentacr.azurecr.io/edy-agent:latest
```

#### View Logs
```bash
az containerapp logs show \
  --name edy-agent \
  --resource-group edy-agent-rg \
  --follow
```

## Key Components

### agent.py (Python Agent)

**TranslationState class**: Maintains conversation history buffer
- `turns`: List of completed German→English translation pairs
- `partial`: Current incomplete German utterance
- `as_prompt()`: Formats conversation for recommendation generation

**EdyTranslatorAgent class**: Main agent logic
- Inherits from `livekit.agents.Agent`
- Uses OpenAI Whisper for German STT
- Uses OpenAI GPT-4o-mini for translation
- Uses ElevenLabs Flash v2 for English TTS
- Uses Silero VAD for voice activity detection

**Translation Flow**:
1. `_stt_transcript_wrapper()` receives German transcripts (partial and final)
2. `_translate_text()` calls OpenAI API for German→English translation
3. `_publish_transcript()` sends JSON to LiveKit data channel with format:
   ```json
   {
     "type": "transcript",
     "german": "...",
     "english": "...",
     "final": true/false
   }
   ```
4. On final transcripts, `_schedule_recommendation_update()` triggers recommendation generation

**Recommendations Flow**:
- Debounced: new recommendations cancel pending ones
- Uses conversation window (last 12 turns) as context
- Generates 5-bullet actionable recommendations via GPT-4o
- Publishes to data channel with format:
  ```json
  {
    "type": "recommendations",
    "content": "..."
  }
  ```

**Metrics Collection**: Logs LLM, STT, TTS, and End-of-Utterance metrics for performance monitoring

### index.html (Frontend)

Single-page web interface that:
- Connects to LiveKit room using token from Netlify function
- Handles microphone permissions
- Displays agent connection status
- (Note: Current version may need updates to consume transcript/recommendation data from LiveKit data channel)

### netlify/functions/get-token.js (Serverless Function)

Generates LiveKit access tokens:
- Creates unique room name: `edy-{timestamp}-{random}`
- Grants room join, publish, and subscribe permissions
- Returns token + LiveKit URL + room name to frontend

### Dockerfile

Production container:
- Base: Python 3.11-slim
- Installs gcc for native dependencies
- Runs `python agent.py start` as entrypoint

## Environment Variables

Required for agent (agent.py):
- `LIVEKIT_URL`: LiveKit server WebSocket URL
- `LIVEKIT_API_KEY`: LiveKit API key
- `LIVEKIT_API_SECRET`: LiveKit API secret
- `OPENAI_API_KEY`: OpenAI API key for Whisper STT and GPT translation
- `ELEVEN_API_KEY`: ElevenLabs API key for TTS

Optional:
- `TRANSLATION_MODEL`: Translation model (default: "gpt-4o-mini")
- `RECOMMENDATION_MODEL`: Recommendation model (default: "gpt-4o")
- `ELEVEN_VOICE_ID`: ElevenLabs voice ID (default: "rachel")

Required for Netlify function:
- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

## Code Patterns

### Adding New Translation Features

To modify translation behavior, edit `_translate_text()`:
```python
async def _translate_text(self, german_text: str, is_final: bool) -> str:
    # Adjust temperature based on finality
    temperature = 0.1 if is_final else 0.3
    # Modify system prompt or add context here
```

### Changing TTS Voice

Browse voices at https://elevenlabs.io/voice-library, then:
```python
tts = elevenlabs.TTS(
    voice_id="YOUR_VOICE_ID",  # Change this
    model="eleven_flash_v2"
)
```

Or set environment variable: `ELEVEN_VOICE_ID=your_voice_id`

### Switching to OpenAI TTS (Cost Optimization)

Replace in `__init__`:
```python
tts = openai.TTS(voice="alloy")  # Cheaper than ElevenLabs
```

### Adjusting Recommendation Frequency

Recommendations trigger on every final transcript. To batch:
```python
if final and len(self.state.turns) % 5 == 0:  # Every 5 turns
    await self._schedule_recommendation_update()
```

### Custom Data Channel Messages

To send new data types to frontend:
```python
payload = json.dumps({
    "type": "custom_event",
    "data": "your_data"
}).encode("utf-8")
await self.session.publish_data(payload, topic="translator")
```

## Cost Optimization

- Agent uses scale-to-zero on Azure (min-replicas: 0)
- Only runs when users connect to LiveKit rooms
- Uses GPT-4o-mini for cost-effective translation
- Uses ElevenLabs Flash v2 (fastest/cheapest TTS)
- Typical cost: $10-30/month for moderate usage

See COSTS.md for detailed breakdown and optimization strategies.

## Important Notes

- Never commit `.env` file (contains API keys)
- Always regenerate API keys if exposed
- Agent automatically connects to LiveKit rooms based on configuration
- Frontend requires HTTPS for microphone access (Netlify provides this)
- Azure Container Registry name (`edyagentacr`) must be globally unique - change in deploy-azure.sh if taken

## Known Issues & Fixes

### Session Property Conflict (FIXED)
**Issue:** The `Agent` base class has a read-only `session` property. Earlier versions tried to set `self.session = None` which caused:
```
AttributeError: property 'session' of 'EdyTranslatorAgent' object has no setter
```

**Fix:** Renamed all `self.session` references to `self._agent_session` throughout the codebase (lines 68, 140, 199, 211, 221, 264, 279).
