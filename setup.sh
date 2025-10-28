#!/bin/bash

# Quick Start Script for Edy Voice Agent
# This script helps you set up environment variables

echo "🤖 Edy Voice Agent - Quick Setup"
echo "=================================="
echo ""
echo "This script will help you set up your environment variables."
echo ""

# Function to read input
read_input() {
    read -p "$1: " value
    echo $value
}

echo "📝 Please enter your credentials:"
echo ""

LIVEKIT_URL=$(read_input "LiveKit URL (e.g., wss://your-project.livekit.cloud)")
LIVEKIT_API_KEY=$(read_input "LiveKit API Key")
LIVEKIT_API_SECRET=$(read_input "LiveKit API Secret")
OPENAI_API_KEY=$(read_input "OpenAI API Key")
ELEVEN_API_KEY=$(read_input "ElevenLabs API Key")

# Create .env file
cat > .env << EOF
# LiveKit Configuration
LIVEKIT_URL=$LIVEKIT_URL
LIVEKIT_API_KEY=$LIVEKIT_API_KEY
LIVEKIT_API_SECRET=$LIVEKIT_API_SECRET

# AI Provider Keys
OPENAI_API_KEY=$OPENAI_API_KEY
ELEVEN_API_KEY=$ELEVEN_API_KEY
EOF

echo ""
echo "✅ .env file created successfully!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Deploy frontend to Netlify:"
echo "   - Push code to GitHub"
echo "   - Import to Netlify"
echo "   - Add environment variables in Netlify dashboard"
echo ""
echo "2. Deploy agent to Azure:"
echo "   - Run: ./deploy-azure.sh"
echo ""
echo "3. Test your deployment:"
echo "   - Visit your Netlify URL"
echo "   - Click 'Start Conversation'"
echo ""
echo "For detailed instructions, see README.md"
echo ""
