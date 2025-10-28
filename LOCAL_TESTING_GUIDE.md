# Local Testing Guide

This guide will help you test the German translation agent locally before deploying to GitHub/Azure/Netlify.

---

## Prerequisites Checklist

✅ Python 3.11 installed
✅ Dependencies installed (`pip install -r requirements.txt`)
✅ `.env` file configured with API keys
✅ LiveKit account and credentials

---

## Step 1: Test the Agent Locally

### Option A: Test Agent in "Dev Mode" (Simplest)

The LiveKit agent can run in development mode and automatically connect to rooms:

```bash
# Run the agent in dev mode
python agent.py dev
```

**What this does:**
- Starts the agent locally on your machine
- Connects to your LiveKit cloud instance
- Waits for incoming connections
- Shows detailed logs in the terminal

**You should see:**
```
INFO:livekit.agents:Starting agent in development mode
INFO:livekit.agents:Connecting to LiveKit: wss://test-p61uftno.livekit.cloud
INFO:edy-translator:Agent ready and waiting for connections...
```

---

### Option B: Test Agent with a Specific Room

If you want to test with a specific room name:

```bash
# Connect to a specific room
python agent.py connect --room test-german-room
```

This will:
- Create or join a room named "test-german-room"
- Start listening for German speech
- Output translation logs

---

## Step 2: Test the Frontend Locally

You can test the frontend WITHOUT deploying to Netlify. Here are 3 options:

### Option 1: Simple HTTP Server (Quickest)

```bash
# Start a local web server
python -m http.server 8000
```

Then open in your browser:
```
http://localhost:8000/index.html
```

**⚠️ LIMITATION:** The Netlify function (`get-token.js`) won't work locally with this method. You'll need to manually create a token or use Option 3 below.

---

### Option 2: Test with LiveKit Playground

Instead of using the frontend, you can test using LiveKit's web playground:

1. Go to https://cloud.livekit.io
2. Navigate to your project
3. Go to "Rooms" → "Create Room"
4. Create a test room (e.g., "test-room-123")
5. Join the room with your browser
6. Enable microphone
7. Start speaking German

**Simultaneously:**
```bash
# In terminal, connect agent to the same room
python agent.py connect --room test-room-123
```

You should:
- See the agent connect in terminal logs
- Hear English translation through your browser
- See transcript logs in the terminal

---

### Option 3: Test with Netlify CLI Locally (Most Complete)

This runs the Netlify function locally so you can test the full stack:

#### Install Netlify CLI:
```bash
npm install -g netlify-cli
```

#### Run locally:
```bash
# In one terminal: Start agent in dev mode
python agent.py dev

# In another terminal: Start Netlify dev server
netlify dev
```

#### What happens:
- Netlify dev server runs at `http://localhost:8888`
- The `get-token` function works locally
- You can test the full user experience

#### Test it:
1. Open `http://localhost:8888` in your browser
2. Click "Start Conversation"
3. Allow microphone access
4. Speak in German
5. Watch for English translation

---

## Step 3: Testing Scenarios

### Test Case 1: Basic Translation
```
German Input: "Guten Morgen, wie geht es dir?"
Expected English: "Good morning, how are you?"
```

**How to verify:**
- ✅ Partial transcripts appear as you speak
- ✅ Final transcript replaces partial one
- ✅ English translation is accurate
- ✅ TTS speaks the English translation

---

### Test Case 2: Partial Transcripts
Speak slowly with pauses:
```
German: "Ich möchte... [pause] ...ein Glas Wasser trinken"
```

**Expected behavior:**
- Partial transcript: "Ich möchte" (while paused)
- Final transcript: "Ich möchte ein Glas Wasser trinken"
- English: "I would like to drink a glass of water"

**Check in logs:**
```
INFO:edy-translator:STT Metrics - Duration: X.XXXs
INFO:edy-translator:LLM Metrics - Tokens: XX | Speed: XX.XX tok/s
```

---

### Test Case 3: Recommendations
Have a conversation with 5+ turns:

```
Turn 1: "Wir müssen das Projekt bis Freitag abschließen"
Turn 2: "Das Budget ist begrenzt"
Turn 3: "Wir brauchen mehr Entwickler"
Turn 4: "Die Deadline ist nicht verhandelbar"
Turn 5: "Was sollten wir priorisieren?"
```

**Expected:**
- After 5 turns, recommendations should appear
- Check data channel logs for recommendation payload

**In frontend:**
You should see an "AI Recommendations" section appear with bullet points

---

## Step 4: Monitor Logs

### What to Look For in Agent Logs:

**✅ Good Signs:**
```
INFO:edy-translator:Translator agent session ready
INFO:edy-translator:STT Metrics - Duration: 0.523s | Audio: 2.145s
INFO:edy-translator:LLM Metrics - Tokens: 45 | Speed: 123.45 tok/s | TTFT: 0.134s
INFO:edy-translator:TTS Metrics - TTFB: 0.234s | Duration: 0.456s
```

**⚠️ Warning Signs:**
```
ERROR:openai:Translation request failed: APIError
WARNING:livekit:Connection lost, reconnecting...
```

**❌ Critical Issues:**
```
ERROR:edy-translator:Missing LiveKit configuration
ERROR:openai:Incorrect API key provided
```

---

## Step 5: Test German Characters

Test with umlauts and special characters:

```
"Schöne grüße aus München"
"Das Mädchen spielt Fußball"
"Die Tür ist geschlossen"
```

**Expected:**
- ✅ Whisper correctly transcribes: "Schöne", "grüße", "München"
- ✅ UTF-8 encoding preserves characters in data channel
- ✅ Frontend displays characters correctly

---

## Troubleshooting

### Issue: "Agent not connecting"

**Solution:**
```bash
# Check environment variables are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('URL:', os.getenv('LIVEKIT_URL'))"
```

If it prints `URL: None`, your `.env` file isn't being read.

---

### Issue: "Translation request failed"

**Possible causes:**
1. Invalid OpenAI API key
2. Insufficient OpenAI credits
3. Rate limit exceeded

**Check:**
```bash
# Test OpenAI API directly
python -c "from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(); print(client.models.list())"
```

---

### Issue: "No audio output"

**Possible causes:**
1. ElevenLabs API key invalid
2. Voice ID doesn't exist
3. TTS quota exceeded

**Check:**
```bash
# Verify ElevenLabs API key
curl -H "xi-api-key: YOUR_KEY" https://api.elevenlabs.io/v1/user
```

---

### Issue: "Frontend can't connect"

**If using `netlify dev`:**
```bash
# Check if function is running
curl -X POST http://localhost:8888/.netlify/functions/get-token
```

**Expected response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "url": "wss://test-p61uftno.livekit.cloud",
  "roomName": "edy-1735344000-abc123"
}
```

---

## Step 6: Test Metrics & Performance

### Monitor Latency

**What to measure:**
- **STT Duration:** Should be < 500ms
- **Translation Duration:** Should be < 300ms
- **TTS TTFB:** Should be < 400ms
- **Total End-to-End:** Should be < 1200ms

**How to test:**
Look for these metrics in logs after speaking:

```
INFO:edy-translator:STT Metrics - Duration: 0.423s | Audio: 2.345s
INFO:edy-translator:LLM Metrics - Tokens: 38 | Speed: 145.67 tok/s | TTFT: 0.156s
INFO:edy-translator:TTS Metrics - TTFB: 0.312s | Duration: 0.543s | Audio: 1.234s
```

---

## Step 7: Verify Before GitHub Upload

Before pushing to GitHub, verify:

- [ ] `.env` is in `.gitignore` (never commit API keys!)
- [ ] Agent starts without errors
- [ ] German speech is transcribed correctly
- [ ] English translation is accurate
- [ ] TTS output is clear
- [ ] Recommendations generate after 5+ turns
- [ ] Frontend receives data channel messages
- [ ] No API errors in logs

**Check `.gitignore`:**
```bash
cat .gitignore | grep .env
```

Should output: `.env`

---

## Quick Test Command

Run this all-in-one test:

```bash
# 1. Check environment
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ LIVEKIT_URL:', os.getenv('LIVEKIT_URL')[:30] + '...'); print('✅ OPENAI_API_KEY:', os.getenv('OPENAI_API_KEY')[:20] + '...'); print('✅ ELEVEN_API_KEY:', os.getenv('ELEVEN_API_KEY')[:20] + '...')"

# 2. Start agent in dev mode
python agent.py dev
```

---

## Next Steps After Local Testing

Once everything works locally:

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: German translation agent"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/edy-translator.git
   git push -u origin main
   ```

2. **Deploy to Netlify:**
   - Import GitHub repo
   - Add environment variables
   - Deploy

3. **Deploy to Azure:**
   ```bash
   ./deploy-azure.sh
   ```

4. **Monitor production:**
   ```bash
   az containerapp logs show --name edy-agent --resource-group edy-agent-rg --follow
   ```

---

## Cost Monitoring During Testing

**Local testing costs:**
- OpenAI Whisper: $0.006/minute
- OpenAI GPT-4o-mini: ~$0.001 per conversation turn
- ElevenLabs: Depends on plan (free tier: 10k chars)

**Estimate for 30 minutes of testing:**
- Whisper: $0.18
- Translation: $0.05
- TTS: $0.00 (free tier)
- **Total: ~$0.25**

Very affordable for thorough testing!

---

## Summary

**Simplest local test:**
```bash
# Terminal 1: Start agent
python agent.py dev

# Terminal 2: Start frontend
netlify dev

# Browser: Open http://localhost:8888
```

**Alternative (no Netlify CLI):**
Use LiveKit Playground + agent in terminal

**Before GitHub:**
Double-check `.env` is not committed!

---

Good luck with your testing! 🚀
