# 💰 Cost Breakdown and Calculator

## Monthly Cost Estimate

### Azure Container Apps (Scale-to-Zero)

**Consumption Plan Pricing:**
- **Idle time (0 replicas)**: $0/month 
- **Active time**: $0.000024/vCPU-second + $0.0000025/GB-second

**Your Configuration:**
- 0.5 vCPU, 1GB RAM
- Min replicas: 0 (scales to zero when not in use)
- Max replicas: 1

**Cost Calculation Examples:**

#### Scenario 1: Low Usage (10 hours/month)
```
10 hours = 36,000 seconds
CPU: 36,000 × 0.5 × $0.000024 = $0.43
RAM: 36,000 × 1 × $0.0000025 = $0.09
Total: ~$0.52/month
```

#### Scenario 2: Moderate Usage (100 hours/month)
```
100 hours = 360,000 seconds
CPU: 360,000 × 0.5 × $0.000024 = $4.32
RAM: 360,000 × 1 × $0.0000025 = $0.90
Total: ~$5.22/month
```

#### Scenario 3: Heavy Usage (300 hours/month)
```
300 hours = 1,080,000 seconds
CPU: 1,080,000 × 0.5 × $0.000024 = $12.96
RAM: 1,080,000 × 1 × $0.0000025 = $2.70
Total: ~$15.66/month
```

---

## Other Costs

### Netlify: FREE
- 100GB bandwidth/month
- 300 build minutes/month
- Unlimited serverless function invocations (first 125k/month)

### LiveKit Cloud: 
You're already using this - check your plan at https://cloud.livekit.io

### OpenAI API:
- GPT-4o: $2.50 per 1M input tokens, $10 per 1M output tokens
- Whisper: $0.006 per minute of audio

**Example:** 
- 100 conversations × 5 min each = 500 minutes
- 500 × $0.006 = $3/month for STT

### ElevenLabs:
Check your plan at https://elevenlabs.io/pricing
- Free tier: 10,000 characters/month
- Creator: $5/month for 30,000 characters

---

## Realistic Monthly Total

**Conservative Estimate (Moderate Usage):**
- Azure Container Apps: $5-10
- OpenAI (STT + LLM): $5-15
- ElevenLabs: $0-5 (depending on plan)
- Netlify: $0
- **Total: $10-30/month**

---

## How to Minimize Costs

### 1. Azure Optimizations
✅ **Already doing:**
- Scale-to-zero (min replicas = 0)
- Small instance size (0.5 vCPU, 1GB RAM)

💡 **Additional tips:**
- Monitor usage with Azure Cost Management
- Set up budget alerts at $10, $20, $30
- Use Azure Free Credits if available

### 2. OpenAI Optimizations
- Use GPT-4o-mini instead of GPT-4o (90% cheaper)
  ```python
  llm = openai.LLM(model="gpt-4o-mini")
  ```
- Keep agent instructions concise
- Implement conversation timeouts

### 3. ElevenLabs Optimizations
- Use Free tier if usage is low
- Or switch to OpenAI TTS (cheaper but lower quality):
  ```python
  tts = openai.TTS(voice="alloy")
  ```

---

## Setting Up Cost Alerts

### Azure Budget Alert:
```bash
# Create a budget with email alert
az consumption budget create \
  --budget-name "edy-agent-budget" \
  --amount 20 \
  --time-grain Monthly \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --resource-group edy-agent-rg
```

### Monitor in Real-Time:
```bash
# Check current month costs
az consumption usage list \
  --resource-group edy-agent-rg \
  --start-date 2025-01-01 \
  --end-date 2025-01-31
```

---

## Cost Tracking Tips

1. **Tag your resources** for better cost tracking:
   ```bash
   az containerapp update \
     --name edy-agent \
     --resource-group edy-agent-rg \
     --tags project=edy-agent environment=production
   ```

2. **Check Azure Cost Management Dashboard**:
   - Go to Azure Portal → Cost Management + Billing
   - View by resource group: `edy-agent-rg`

3. **Review monthly**:
   - OpenAI usage: https://platform.openai.com/usage
   - ElevenLabs usage: https://elevenlabs.io/app/usage
   - Azure: Cost Management dashboard

---

## When to Scale Up

If your agent becomes popular and you need better performance:

**Option 1: More CPU/RAM**
```bash
az containerapp update \
  --name edy-agent \
  --resource-group edy-agent-rg \
  --cpu 1.0 \
  --memory 2.0Gi
```
*Cost: ~$10-20/month for moderate use*

**Option 2: Multiple Replicas**
```bash
az containerapp update \
  --name edy-agent \
  --resource-group edy-agent-rg \
  --min-replicas 1 \
  --max-replicas 3
```
*Cost: Scales with usage, but faster response times*

---

## Summary

✅ **Start with**: $10-30/month  
📈 **Scale based on**: Actual usage  
🎯 **Keep costs low**: Use scale-to-zero and monitor usage  
💡 **Pro tip**: Azure gives $200 free credits for 30 days

**The architecture you chose is very cost-effective because:**
- Agent only runs when users connect
- Netlify frontend is free
- You pay only for actual compute time
