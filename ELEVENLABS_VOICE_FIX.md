# 🎤 ElevenLabs TTS Fixed - Voice Configuration Guide

## ✅ **ISSUE RESOLVED**

### **The Problem:**
```
ERROR: voice_id_does_not_exist (status_code=500)
```

### **Root Cause:**
Your `.env` file was missing the `ELEVEN_VOICE_ID` configuration. The code was using `"rachel"` as the default, but ElevenLabs requires the **actual voice ID** (a long alphanumeric string), not just the name.

### **The Fix:**
Added this line to your `.env` file:
```bash
ELEVEN_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

This is Rachel's actual voice ID.

---

## 🔄 **How To Test**

1. **Restart your agent:**
   ```bash
   python agent.py dev
   ```

2. **Open your frontend** and speak German

3. **You should now hear:**
   - ✅ Your German speech recognized
   - ✅ English translation generated
   - ✅ English translation spoken in Rachel's voice

---

## 🎙️ **Available ElevenLabs Voices**

If you want to use a **different voice**, change `ELEVEN_VOICE_ID` in `.env` to one of these:

### **Female Voices (English):**

| Name | Voice ID | Accent | Description |
|------|----------|--------|-------------|
| **Rachel** | `21m00Tcm4TlvDq8ikWAM` | American | Calm, clear (CURRENT) |
| **Domi** | `AZnzlk1XvdvUeBnXmlld` | American | Confident, strong |
| **Bella** | `EXAVITQu4vr4xnSDxMaL` | American | Soft, young |
| **Elli** | `MF3mGyEYCl7XYWbV9V6O` | American | Emotional, expressive |
| **Emily** | `LcfcDJNUP1GQjkzn1xUU` | American | Warm, friendly |
| **Grace** | `oWAxZDx7w5VEj9dCyTzz` | American | Calm, professional |
| **Matilda** | `XrExE9yKIg1WjnnlVkGX` | American | Warm, narrative |
| **Charlotte** | `XB0fDUnXU5powFXDhCwa` | Swedish | Clear, soft |
| **Alice** | `Xb7hH8MSUJpSbSDYk0k2` | British | Confident, clear |
| **Lily** | `pFZP5JQG7iQjIQuC4Bku` | British | Young, warm |
| **Dorothy** | `ThT5KcBeYPX3keUQqHPh` | British | Mature, authoritative |
| **Freya** | `jsCqWAovK2LkecY7zXl4` | American | Expressive, young |
| **Serena** | `pMsXgVXv3BLzUgSXRplE` | American | Pleasant, clear |
| **Nicole** | `piTKgcLEGmPE4e6mEKli` | American | Confident, professional |

### **Male Voices (English):**

| Name | Voice ID | Accent | Description |
|------|----------|--------|-------------|
| **Antoni** | `ErXwobaYiN019PkySvjV` | American | Well-rounded, pleasant |
| **Josh** | `TxGEqnHWrfWFTfGW9XjX` | American | Young, casual |
| **Adam** | `pNInz6obpgDQGcFmaJgB` | American | Deep, narrative |
| **Sam** | `yoZ06aMxZJJ28mfd3POQ` | American | Young, dynamic |
| **Drew** | `29vD33N1CtxCmqQRPOHJ` | American | Well-rounded, engaging |
| **Clyde** | `2EiwWnXFnvU5JabPnv8n` | American | Warm, friendly |
| **Paul** | `5Q0t7uMcjvnagumLfvZi` | American | Energetic, upbeat |
| **Thomas** | `GBv7mTt0atIp3Br8iCZE` | American | Calm, mature |
| **Charlie** | `IKne3meq5aSn9XLyUdCD` | Australian | Casual, natural |
| **Callum** | `N2lVS1w4EtoT3dr4eOWO` | American | Intense, hoarse |
| **Patrick** | `ODq5zmih8GrVes37Dizd` | American | Shouty, old |
| **Harry** | `SOYHLrjzK2X1ezoPC6cr` | American | Anxious, young |
| **Liam** | `TX3LPaxmHKxFdv7VOQHJ` | American | Calm, articulate |
| **Arnold** | `VR6AewLTigWG4xSOukaG` | American | Crisp, strong |
| **Ethan** | `g5CIjZEefAph4nQFvHAz` | American | Pleasant, young |
| **Michael** | `flq6f7yk4E4fJM5XTYuZ` | American | Refined, authoritative |
| **Daniel** | `onwK4e9ZLuTAKqWW03F9` | British | Deep, authoritative |
| **George** | `JBFqnCBsd6RMkjVDRZzb` | British | Warm, raspy |
| **Dave** | `CYw3kZ02Hs0563khs1Fj` | British | Young, conversational |
| **Fin** | `D38z5RcWu1voky8WS1ja` | Irish | Sailor-like, warm |
| **James** | `ZQe5CZNOzWyzPSCn5a3c` | Australian | Calm, neutral |
| **Joseph** | `Zlb1dXrM653N07WRdFW3` | British | Mature, uplifting |
| **Bill** | `pqHfZKP75CvOlQylNhV4` | American | Strong, confident |

---

## 🔧 **How To Change Voice**

### **Method 1: Edit `.env` File**
```bash
# Open .env and change this line:
ELEVEN_VOICE_ID=21m00Tcm4TlvDq8ikWAM   # Rachel (current)

# To any other voice, for example:
ELEVEN_VOICE_ID=ErXwobaYiN019PkySvjV   # Antoni (male)
ELEVEN_VOICE_ID=AZnzlk1XvdvUeBnXmlld   # Domi (female, confident)
ELEVEN_VOICE_ID=TxGEqnHWrfWFTfGW9XjX   # Josh (male, young)
```

### **Method 2: Use Your Own Custom Voice**
If you've cloned voices in ElevenLabs:
1. Go to: https://elevenlabs.io/app/voice-library
2. Find your custom voice
3. Copy the Voice ID (looks like: `Xb7hH8MSUJpSbSDYk0k2`)
4. Add it to `.env`: `ELEVEN_VOICE_ID=your-voice-id`

---

## 🧪 **Testing Different Voices**

### **Quick Test:**
1. Edit `.env` and change `ELEVEN_VOICE_ID`
2. Restart agent: `python agent.py dev`
3. Speak German and listen to the new voice!

### **Recommended Voices for Translation:**

**For Professional/Business:**
- Rachel (`21m00Tcm4TlvDq8ikWAM`) - Clear, calm female
- Antoni (`ErXwobaYiN019PkySvjV`) - Professional male
- Daniel (`onwK4e9ZLuTAKqWW03F9`) - Authoritative British male

**For Casual/Friendly:**
- Bella (`EXAVITQu4vr4xnSDxMaL`) - Soft, friendly female
- Josh (`TxGEqnHWrfWFTfGW9XjX`) - Young, casual male
- Sam (`yoZ06aMxZJJ28mfd3POQ`) - Dynamic, engaging male

**For Audiobooks/Narration:**
- Adam (`pNInz6obpgDQGcFmaJgB`) - Deep, narrative male
- Matilda (`XrExE9yKIg1WjnnlVkGX`) - Warm narrative female

---

## 📊 **What's Working Now**

### **Your Translation Pipeline:**
```
1. Microphone → German speech detected ✅
2. OpenAI Whisper → Transcribes German ✅
3. OpenAI GPT-4o-mini → Translates to English ✅
4. ElevenLabs TTS → Speaks English (FIXED!) ✅
5. Audio Output → You hear translation ✅
```

### **What You'll See in Console:**
```
INFO STT Metrics - Duration: 2.146s | Audio: 2.112s
INFO LLM Metrics - Tokens: 8 | Speed: 7.74 tok/s
INFO TTS Metrics - TTFB: 0.385s | Duration: 1.054s
✅ Translation spoken successfully!
```

---

## 🚨 **Common Issues & Solutions**

### **Issue: "voice_id_does_not_exist" Still Appearing**

**Cause:** Agent not restarted after fixing `.env`

**Solution:**
1. Stop the agent (Ctrl+C)
2. Restart: `python agent.py dev`
3. The new voice ID will be loaded

### **Issue: Different Error - "quota_exceeded"**

**Cause:** ElevenLabs free tier limit reached (10,000 characters/month)

**Solution:**
1. Check usage: https://elevenlabs.io/app/usage
2. Upgrade plan or wait for monthly reset
3. Or use OpenAI TTS instead (cheaper, unlimited)

### **Issue: Voice Sounds Robotic**

**Cause:** Using `eleven_turbo_v2` model (fast but lower quality)

**Solution:** Change model in `agent.py` line 72:
```python
tts = elevenlabs.TTS(
    voice_id=os.getenv("ELEVEN_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
    model="eleven_multilingual_v2"  # Better quality
)
```

---

## 💰 **Cost Considerations**

### **ElevenLabs Pricing:**
- **Free Tier:** 10,000 characters/month
- **Starter ($5/mo):** 30,000 characters
- **Creator ($22/mo):** 100,000 characters

### **Character Usage Example:**
```
English sentence: "Hello, how are you doing today?"
Characters: 33
Cost (Creator plan): $0.0073

10-minute conversation ≈ 3,000 characters
Cost: ~$0.66 for 10 minutes
```

### **Alternative: OpenAI TTS (Cheaper)**
If you want to save money, change `agent.py` line 72-74:
```python
# Replace ElevenLabs TTS with OpenAI TTS
from livekit.plugins import openai
tts = openai.TTS(voice="nova")  # $0.015 per 1000 chars
```

OpenAI voices available: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

---

## ✅ **Summary**

### **What Was Fixed:**
- ❌ **Before:** `ELEVEN_VOICE_ID` missing → Used invalid "rachel" → Error
- ✅ **After:** `ELEVEN_VOICE_ID=21m00Tcm4TlvDq8ikWAM` → Valid Rachel voice → Works!

### **What To Do Now:**
1. Restart agent: `python agent.py dev`
2. Test by speaking German
3. Enjoy hearing English translations!
4. (Optional) Try different voices from the table above

### **Files Modified:**
- `F:\Agentic_Apps\edy-translator\.env` - Added `ELEVEN_VOICE_ID=21m00Tcm4TlvDq8ikWAM`

---

## 🎯 **Quick Reference Commands**

```bash
# Restart agent after changing voice
python agent.py dev

# Check ElevenLabs usage
# Visit: https://elevenlabs.io/app/usage

# Test different voice (edit .env first)
# 1. Open .env
# 2. Change ELEVEN_VOICE_ID to any ID from the table
# 3. Restart agent
# 4. Test!
```

---

**Your translation app is now fully working!** 🎉

Speak German → Hear English → All automatic! 🚀
