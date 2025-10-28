# Talk to Virtual Edy - Deployment Guide

Beautiful voice AI assistant deployed on Netlify (frontend) and Azure (agent).

## 🏗️ Architecture

```
User → Netlify Frontend → LiveKit Cloud ← Azure Container App (Agent)
```

- **Frontend**: Beautiful web interface on Netlify (free)
- **Agent**: Python worker on Azure Container Apps (only runs when users connect)
- **LiveKit**: Real-time communication server (you're already using this)

## 💰 Cost Estimate

### Azure Container Apps (Scale-to-Zero)
- **When idle (0 users)**: $0/month
- **When active**: ~$0.02/hour = ~$5-10/month for moderate use
- **0.5 vCPU, 1GB RAM** is sufficient

### Netlify
- **FREE** (includes 100GB bandwidth/month)

### Total: $5-10/month (only when users are talking to Edy)

---

## 🚨 CRITICAL: First Steps

### 1. Regenerate ALL API Keys

Your current keys are exposed in the code. You MUST regenerate:

1. **OpenAI API Key**: https://platform.openai.com/api-keys
2. **ElevenLabs API Key**: https://elevenlabs.io/app/settings/api-keys
3. **LiveKit Credentials**: https://cloud.livekit.io/

---

## 📋 Prerequisites

1. **Azure Account**: https://azure.microsoft.com/free/
2. **Netlify Account**: https://netlify.com (sign up with GitHub)
3. **GitHub Account**: To push your code
4. **Azure CLI**: Install on your computer

---

## 🚀 Deployment Steps

### Part 1: Deploy Frontend to Netlify

1. **Create a GitHub repository**:
   ```bash
   git init
   git add index.html netlify.toml package.json netlify/
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/edy-voice-agent.git
   git push -u origin main
   ```

2. **Deploy to Netlify**:
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select your repository
   - Build settings:
     - Build command: (leave empty)
     - Publish directory: `.`
   - Click "Deploy site"

3. **Add Environment Variables in Netlify**:
   - Go to Site settings → Environment variables
   - Add these variables:
     ```
     LIVEKIT_URL=wss://your-project.livekit.cloud
     LIVEKIT_API_KEY=your_api_key
     LIVEKIT_API_SECRET=your_api_secret
     ```

---

### Part 2: Deploy Agent to Azure

1. **Install Azure CLI**:
   ```bash
   # macOS
   brew install azure-cli
   
   # Windows
   # Download from: https://aka.ms/installazurecliwindows
   
   # Linux
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Set Environment Variables**:
   ```bash
   export LIVEKIT_URL=wss://your-project.livekit.cloud
   export LIVEKIT_API_KEY=your_new_api_key
   export LIVEKIT_API_SECRET=your_new_api_secret
   export OPENAI_API_KEY=sk-proj-your_new_key
   export ELEVEN_API_KEY=sk_your_new_key
   ```

3. **Run Deployment Script**:
   ```bash
   chmod +x deploy-azure.sh
   ./deploy-azure.sh
   ```

4. **The script will**:
   - Create Azure resources
   - Build and push Docker image
   - Deploy container with scale-to-zero
   - Configure environment variables

---

## 🔧 Manual Azure Deployment (Alternative)

If the script doesn't work, deploy manually:

```bash
# 1. Login
az login

# 2. Create resource group
az group create --name edy-agent-rg --location eastus

# 3. Create container registry
az acr create --resource-group edy-agent-rg --name edyagentacr --sku Basic

# 4. Build image
az acr build --registry edyagentacr --image edy-agent:latest --file Dockerfile .

# 5. Create container environment
az containerapp env create \
  --name edy-env \
  --resource-group edy-agent-rg \
  --location eastus

# 6. Deploy container app
az containerapp create \
  --name edy-agent \
  --resource-group edy-agent-rg \
  --environment edy-env \
  --image edyagentacr.azurecr.io/edy-agent:latest \
  --registry-server edyagentacr.azurecr.io \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 0 \
  --max-replicas 1 \
  --env-vars \
    LIVEKIT_URL=$LIVEKIT_URL \
    LIVEKIT_API_KEY=$LIVEKIT_API_KEY \
    LIVEKIT_API_SECRET=$LIVEKIT_API_SECRET \
    OPENAI_API_KEY=$OPENAI_API_KEY \
    ELEVEN_API_KEY=$ELEVEN_API_KEY
```

---

## 🧪 Testing

1. Open your Netlify URL (e.g., `https://your-site-name.netlify.app`)
2. Click "Start Conversation"
3. Allow microphone access
4. Start speaking!

**Check Azure logs**:
```bash
az containerapp logs show \
  --name edy-agent \
  --resource-group edy-agent-rg \
  --follow
```

---

## 📊 Monitoring & Costs

### View Azure Costs:
```bash
az consumption usage list --resource-group edy-agent-rg
```

### Monitor Container App:
- Azure Portal → Container Apps → edy-agent → Metrics
- Check: CPU usage, memory, replica count

---

## 🛠️ Updating Your Agent

### Update the code:
```bash
# Make changes to agent.py
# Then rebuild and deploy:
az acr build --registry edyagentacr --image edy-agent:latest --file Dockerfile .

# Update the container app:
az containerapp update \
  --name edy-agent \
  --resource-group edy-agent-rg \
  --image edyagentacr.azurecr.io/edy-agent:latest
```

---

## ❗ Troubleshooting

### Agent not connecting?
1. Check environment variables are set correctly
2. View logs: `az containerapp logs show --name edy-agent --resource-group edy-agent-rg --follow`
3. Verify LiveKit credentials are correct

### Frontend not loading?
1. Check Netlify deploy logs
2. Verify environment variables are set in Netlify
3. Check browser console for errors

### High Azure costs?
1. Check if agent is scaling down: `az containerapp show --name edy-agent --resource-group edy-agent-rg`
2. Ensure `--min-replicas 0` is set
3. Agent should only run when users connect

---

## 🗑️ Cleanup

To delete all Azure resources:
```bash
az group delete --name edy-agent-rg --yes --no-wait
```

---

## 📝 Files Overview

```
.
├── agent.py                     # Production agent code
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container definition
├── index.html                   # Frontend web page
├── netlify.toml                 # Netlify configuration
├── package.json                 # Node dependencies
├── netlify/functions/
│   └── get-token.js            # Token generation function
├── deploy-azure.sh             # Azure deployment script
└── .env.example                # Environment variables template
```

---

## 🎯 Next Steps

1. **Customize the agent**:
   - Edit `agent.py` instructions
   - Change TTS voice ID
   - Adjust LLM model

2. **Improve frontend**:
   - Add branding
   - Customize colors
   - Add analytics

3. **Monitor usage**:
   - Set up Azure alerts
   - Track conversation metrics
   - Monitor costs

---

## 🆘 Support

- Azure docs: https://learn.microsoft.com/azure/container-apps/
- LiveKit docs: https://docs.livekit.io/
- Netlify docs: https://docs.netlify.com/

---

**Good luck with your deployment! 🚀**
