# 🚀 Quick Start - Test in 2 Minutes

This is the **EASIEST** way to test your German translator locally.

---

## Step 1: Start the Agent (Terminal 1)

```bash
python agent.py dev
```

**You should see:**
```
✅ Watching F:\Agentic_Apps\edy-translator
✅ registered worker
```

**Leave this running!**

---

## Step 2: Start the Test Server (Terminal 2)

Open a **NEW terminal** and run:

```bash
python local_server.py
```

**You should see:**
```
============================================================
🚀 German Translator - Local Test Server
============================================================

✅ Server running at: http://localhost:8000
✅ LiveKit URL: wss://test-p61uftno.livekit.cloud

📖 Instructions:
   1. Open: http://localhost:8000/test-simple.html
   2. Click 'Start Conversation'
   3. Allow microphone access
   4. Speak in German!
```

**Leave this running too!**

---

## Step 3: Open Your Browser

Go to:
```
http://localhost:8000/test-simple.html
```

---

## Step 4: Test!

1. Click **"Start Conversation"** button
2. Allow microphone access when prompted
3. **Speak in German:**
   - "Guten Morgen"
   - "Wie geht es dir?"
   - "Das Wetter ist schön"

---

## What You Should See

### In the Browser:
- ✅ Status changes to: "✅ Connected! Start speaking in German..."
- ✅ Two panels appear:
  - **Left panel:** Your German speech (real-time)
  - **Right panel:** English translation (real-time)
- ✅ Debug log at bottom shows connection progress

### In Terminal 1 (Agent):
```
INFO:edy-translator:Connecting to room: test-1735344000-abc123
INFO:edy-translator:Translator agent session ready
INFO:edy-translator:STT Metrics - Duration: 0.523s | Audio: 2.145s
INFO:edy-translator:LLM Metrics - Tokens: 45 | Speed: 123.45 tok/s
INFO:edy-translator:TTS Metrics - TTFB: 0.234s
```

### In Terminal 2 (Server):
```
✅ Generated token for room: test-1735344000-abc123
📄 /test-simple.html
```

### You Should HEAR:
English translation of your German speech through your computer speakers!

---

## Troubleshooting

### Problem: "Nothing happens when I click Start Conversation"

**Check the browser console:**
- Right-click → Inspect → Console tab
- Look for error messages

**Common fixes:**
1. Make sure Terminal 2 (server) is running on port 8000
2. Try refreshing the browser page
3. Check the Debug Log at the bottom of the page

---

### Problem: "Token request failed"

**In Terminal 2, you should see:**
```
✅ Generated token for room: test-1735344000-abc123
```

**If you see an error:**
1. Check your .env file has all credentials
2. Restart the server: `python local_server.py`

---

### Problem: "Connected but no translation"

**Check Terminal 1 (agent):**
- Should show: "Connecting to room: test-..."
- Should show: "Translator agent session ready"

**If agent doesn't connect:**
1. Stop agent (Ctrl+C)
2. Restart: `python agent.py dev`

---

### Problem: "Can't hear the translation"

**Checklist:**
1. ✅ Check your computer speakers are on
2. ✅ Check volume is up
3. ✅ Look in Terminal 1 for TTS metrics
4. ✅ Try speaking a longer sentence

---

## Test Phrases

Try these German phrases:

| German | Expected English |
|--------|------------------|
| Guten Morgen | Good morning |
| Wie geht es dir? | How are you? |
| Ich heiße Maria | My name is Maria |
| Das Wetter ist schön | The weather is nice |
| Ich möchte Kaffee trinken | I would like to drink coffee |
| Wo ist die Toilette? | Where is the bathroom? |

---

## Success Checklist

- [ ] Terminal 1 running: `python agent.py dev`
- [ ] Terminal 2 running: `python local_server.py`
- [ ] Browser shows: http://localhost:8000/test-simple.html
- [ ] Clicked "Start Conversation"
- [ ] Allowed microphone access
- [ ] Status shows "Connected!"
- [ ] Spoke German
- [ ] Saw German text in left panel
- [ ] Saw English text in right panel
- [ ] Heard English audio through speakers

If all checkboxes are checked: **🎉 SUCCESS!**

---

## Next Steps After Testing

Once this works:

1. **Stop both terminals** (Ctrl+C)
2. **Deploy to production:**
   - Push code to GitHub
   - Deploy frontend to Netlify
   - Deploy agent to Azure

3. **See deployment guides:**
   - README.md - Full deployment instructions
   - CLAUDE.md - Architecture and development guide

---

## Quick Reference

**Start testing:**
```bash
# Terminal 1
python agent.py dev

# Terminal 2
python local_server.py

# Browser
http://localhost:8000/test-simple.html
```

**Stop testing:**
- Terminal 1: Ctrl+C
- Terminal 2: Ctrl+C
- Browser: Close tab

---

**That's it! You're ready to test! 🚀**
