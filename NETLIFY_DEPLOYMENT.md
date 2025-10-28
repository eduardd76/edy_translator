# 🚀 Netlify Deployment Guide - Step by Step

This guide will help you deploy the German translator frontend to Netlify from your GitHub repository.

**Time Required:** 10-15 minutes
**Cost:** FREE (Netlify free tier)

---

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ GitHub repository: https://github.com/eduardd76/edy_translator
- ✅ Netlify account (free) - Sign up at https://netlify.com
- ✅ Your LiveKit credentials from `.env` file

---

## 🎯 Step 1: Go to Netlify

### 1.1 Open Netlify
Go to: **https://app.netlify.com**

### 1.2 Sign In
- If you have an account: Click **"Log in"**
- If you don't: Click **"Sign up"**
  - Choose: **"Sign up with GitHub"** (easiest option)
  - Authorize Netlify to access your GitHub account

**Why GitHub sign-in?** Makes connecting your repository much easier!

---

## 🎯 Step 2: Create New Site

### 2.1 Click "Add new site"
- On your Netlify dashboard (main page)
- Look for the button: **"Add new site"** or **"Import from Git"**
- Click it

### 2.2 Choose "Import an existing project"
You'll see three options:
- Import from Git
- Deploy manually
- Start from template

**Click:** "Import from Git" → "Deploy with GitHub"

---

## 🎯 Step 3: Connect GitHub Repository

### 3.1 Authorize Netlify (if prompted)
- You may see: "Netlify would like permission to access your GitHub account"
- Click **"Authorize Netlify"**

### 3.2 Search for your repository
- You'll see a list of your GitHub repositories
- Type in search box: **"edy_translator"**
- Click on: **eduardd76/edy_translator**

**Can't find it?**
- Click "Configure Netlify on GitHub" at the bottom
- Grant access to the repository
- Come back to Netlify and refresh

---

## 🎯 Step 4: Configure Build Settings

You'll see a page titled "Deploy settings for eduardd76/edy_translator"

### 4.1 Site Settings

**Owner:** (Your Netlify team name - leave as is)

**Branch to deploy:**
- Select: **main**

**Base directory:**
- Leave **EMPTY** (blank)

### 4.2 Build Settings

**Build command:**
- Leave **EMPTY** (blank)
- (This is a static site with serverless functions)

**Publish directory:**
- Type: `.` (just a single dot)
- This means: publish from the root directory

**Functions directory:**
- Should auto-detect: `netlify/functions`
- If not, type: `netlify/functions`

---

## 🎯 Step 5: Add Environment Variables (CRITICAL!)

This is the **MOST IMPORTANT STEP** - your app won't work without these!

### 5.1 Scroll down to "Environment variables"

### 5.2 Click "Add environment variables" or "New variable"

### 5.3 Add these THREE variables:

#### Variable 1: LIVEKIT_URL
```
Key: LIVEKIT_URL
Value: wss://test-p61uftno.livekit.cloud
```
*Copy from your .env file*

Click "Add" or save

#### Variable 2: LIVEKIT_API_KEY
```
Key: LIVEKIT_API_KEY
Value: APIX5jniKDEaESA
```
*Copy from your .env file*

Click "Add" or save

#### Variable 3: LIVEKIT_API_SECRET
```
Key: LIVEKIT_API_SECRET
Value: vLqg4keXeeJbwOHbnapUc7hekyeTTBxIjMudAe5YIxZN
```
*Copy from your .env file*

Click "Add" or save

### ⚠️ IMPORTANT:
These values are from YOUR .env file. Open your `.env` file locally and copy the EXACT values!

---

## 🎯 Step 6: Deploy!

### 6.1 Click "Deploy [site-name]" button
- Usually at the bottom of the page
- Big, colorful button

### 6.2 Wait for deployment
You'll see:
- ⏳ "Site deploy in progress"
- A log showing build steps
- Progress indicator

**Takes:** ~1-2 minutes

### 6.3 Watch for "Site is live"
When done, you'll see:
- ✅ "Site is live"
- A random URL like: `https://spontaneous-unicorn-123abc.netlify.app`

---

## 🎯 Step 7: Test Your Deployment

### 7.1 Click the site URL
- Netlify shows your site URL at the top
- Click it to open in a new tab

### 7.2 What you should see:
- Beautiful gradient purple background
- Title: "Talk to Virtual Edy"
- Button: "Start Conversation"
- Status: "Ready to connect"

### 7.3 Test the app:

**IMPORTANT:** Make sure your **agent is running** first!

**In your local Terminal:**
```bash
cd F:\Agentic_Apps\edy-translator
python agent.py dev
```

**Then in the Netlify site:**
1. Click "Start Conversation"
2. Allow microphone access
3. Say: **"Guten Morgen"**
4. You should hear: **"Good morning"**

---

## 🎯 Step 8: Customize Your Site URL (Optional)

### 8.1 Go to Site Settings
- Click "Site settings" in Netlify dashboard
- Or click "Domain management"

### 8.2 Change Site Name
- Look for "Site information"
- Click "Change site name"
- Enter a custom name: `edy-german-translator`
- Your URL becomes: `https://edy-german-translator.netlify.app`

---

## ✅ Deployment Checklist

After deployment, verify:

- [ ] Site is live and accessible
- [ ] Frontend loads without errors
- [ ] "Start Conversation" button works
- [ ] Microphone permission prompt appears
- [ ] Can hear audio output
- [ ] German speech is transcribed
- [ ] English translation appears
- [ ] Both transcript panels show text

---

## 🐛 Troubleshooting

### Problem: "Site deploy failed"

**Check build log for errors:**
1. Click on the failed deploy
2. Read the error message
3. Common issues:
   - Functions directory not found → Check `netlify.toml`
   - Missing dependencies → Check `package.json`

**Solution:**
- Make sure `netlify.toml` exists in your repo
- Make sure `netlify/functions/get-token.js` exists

---

### Problem: "Token generation failed"

**Symptoms:**
- Browser shows: "Failed to get token"
- Can't connect to conversation

**Check:**
1. Go to Netlify Dashboard
2. Site settings → Environment variables
3. Verify all 3 variables are set:
   - ✅ LIVEKIT_URL
   - ✅ LIVEKIT_API_KEY
   - ✅ LIVEKIT_API_SECRET

**To fix:**
1. Add missing variables
2. Trigger new deploy:
   - Deploys → Trigger deploy → Deploy site

---

### Problem: "Connected but no translation"

**Symptoms:**
- Site says "Connected"
- Microphone works
- But no translation happens

**Check:**
1. **Is your local agent running?**
   ```bash
   python agent.py dev
   ```

2. Look at agent terminal - should show:
   ```
   INFO:edy-translator:Connecting to room: edy-...
   ```

**Note:** The agent must be running locally for now. Later you'll deploy it to Azure!

---

### Problem: "Can't hear audio"

**Check:**
1. ✅ Agent is running locally
2. ✅ Computer speakers are on
3. ✅ Volume is up
4. ✅ Browser has audio permission

**Debug:**
- Open browser console (F12)
- Look for errors
- Check if audio track is connected

---

### Problem: "Environment variables not working"

**Symptoms:**
- Function returns error about missing credentials

**Fix:**
1. Go to Site settings → Environment variables
2. Delete all variables
3. Add them again ONE BY ONE
4. Make sure there are NO extra spaces
5. Trigger new deploy

---

## 📱 View Function Logs

To see if the token generation function is working:

1. Go to Netlify Dashboard
2. Click your site
3. Go to **"Functions"** tab
4. Click **"get-token"**
5. View logs to see:
   - Requests coming in
   - Tokens being generated
   - Any errors

---

## 🔄 Automatic Deployments

**Good news!** Netlify is now connected to your GitHub repo.

**What this means:**
- Every time you `git push` to GitHub
- Netlify automatically rebuilds and deploys
- No manual steps needed!

**To deploy updates:**
```bash
# Make changes to your code
git add .
git commit -m "Update: your changes"
git push

# Netlify automatically deploys in 1-2 minutes
```

---

## 🌐 Custom Domain (Optional)

Want a custom domain like `translator.yourdomain.com`?

### Step 1: Buy a domain
- Namecheap, Google Domains, etc.

### Step 2: Add to Netlify
1. Site settings → Domain management
2. Click "Add custom domain"
3. Enter your domain
4. Follow DNS setup instructions

### Step 3: Enable HTTPS
- Netlify provides free SSL
- Auto-enabled for custom domains

---

## 💰 Netlify Costs

### Free Tier Includes:
- ✅ 100GB bandwidth/month
- ✅ 300 build minutes/month
- ✅ Unlimited sites
- ✅ Serverless functions: 125k requests/month
- ✅ SSL certificate
- ✅ Continuous deployment

**Cost for this app:** $0/month (stays within free tier)

---

## 🎉 Success!

If everything works:
- ✅ Site is deployed
- ✅ Can click "Start Conversation"
- ✅ Can speak German
- ✅ Hear English translation
- ✅ See transcripts in real-time

**Your Netlify URL:**
`https://[your-site-name].netlify.app`

---

## 📊 What's Deployed

### Files on Netlify:
- `index.html` - Main frontend
- `netlify.toml` - Configuration
- `netlify/functions/get-token.js` - Token generation
- `package.json` - Dependencies

### What Netlify Does:
1. Hosts your HTML/CSS/JS
2. Runs serverless function to generate tokens
3. Handles HTTPS automatically
4. Provides CDN for fast loading
5. Auto-deploys on git push

---

## 🚀 Next Steps

Now that your frontend is on Netlify:

### 1. Deploy Agent to Azure
Your agent still runs locally. To make it production-ready:
- Follow `README.md` for Azure deployment
- Or ask: "Help me deploy agent to Azure"

### 2. Test from Any Device
- Share your Netlify URL with others
- Test from phone, tablet, different computers
- Note: Agent must be running (locally or on Azure)

### 3. Monitor Usage
Netlify Dashboard shows:
- Number of visitors
- Bandwidth used
- Function invocations
- Build history

---

## 📞 Need Help?

**Netlify Support:**
- Docs: https://docs.netlify.com
- Community: https://answers.netlify.com

**Common Commands:**

```bash
# View deployment status
netlify status

# Open site in browser
netlify open:site

# View function logs
netlify functions:log get-token

# Trigger new deploy
netlify deploy --prod
```

---

## ✅ Deployment Complete!

**Congratulations!** Your German translator frontend is now:
- ✅ Deployed on Netlify
- ✅ Accessible from anywhere
- ✅ Auto-deploys on git push
- ✅ Running on HTTPS
- ✅ Using serverless functions
- ✅ FREE!

**Share your link:**
`https://[your-site-name].netlify.app`

🎉 Great job!
