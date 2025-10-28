#!/bin/bash

# Azure Container Apps Deployment Script for Edy Voice Agent
# This script deploys the LiveKit agent to Azure with scale-to-zero configuration

set -e

# Configuration
RESOURCE_GROUP="edy-agent-rg"
LOCATION="eastus"
CONTAINER_ENV="edy-env"
CONTAINER_APP="edy-agent"
ACR_NAME="edyagentacr"  # Azure Container Registry name (must be globally unique)

echo "🚀 Starting deployment to Azure Container Apps..."

# 1. Login to Azure (if not already logged in)
echo "📝 Checking Azure login..."
az account show &>/dev/null || az login

# 2. Create Resource Group
echo "📦 Creating resource group..."
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

# 3. Create Azure Container Registry
echo "🐳 Creating container registry..."
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $ACR_NAME \
    --sku Basic \
    --admin-enabled true

# 4. Build and push Docker image
echo "🔨 Building Docker image..."
az acr build \
    --registry $ACR_NAME \
    --image edy-agent:latest \
    --file Dockerfile \
    .

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query "loginServer" -o tsv)

# 5. Create Container Apps Environment
echo "🌍 Creating Container Apps environment..."
az containerapp env create \
    --name $CONTAINER_ENV \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION

# 6. Deploy Container App with scale-to-zero
echo "🚢 Deploying container app..."
az containerapp create \
    --name $CONTAINER_APP \
    --resource-group $RESOURCE_GROUP \
    --environment $CONTAINER_ENV \
    --image "${ACR_LOGIN_SERVER}/edy-agent:latest" \
    --registry-server $ACR_LOGIN_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --cpu 0.5 \
    --memory 1.0Gi \
    --min-replicas 0 \
    --max-replicas 1 \
    --secrets \
        livekit-url=$LIVEKIT_URL \
        livekit-api-key=$LIVEKIT_API_KEY \
        livekit-api-secret=$LIVEKIT_API_SECRET \
        openai-api-key=$OPENAI_API_KEY \
        eleven-api-key=$ELEVEN_API_KEY \
    --env-vars \
        LIVEKIT_URL=secretref:livekit-url \
        LIVEKIT_API_KEY=secretref:livekit-api-key \
        LIVEKIT_API_SECRET=secretref:livekit-api-secret \
        OPENAI_API_KEY=secretref:openai-api-key \
        ELEVEN_API_KEY=secretref:eleven-api-key

echo "✅ Deployment complete!"
echo ""
echo "📊 Resource Group: $RESOURCE_GROUP"
echo "🌐 Container App: $CONTAINER_APP"
echo ""
echo "To view logs:"
echo "  az containerapp logs show --name $CONTAINER_APP --resource-group $RESOURCE_GROUP --follow"
echo ""
echo "⚠️  IMPORTANT: Set these environment variables before running:"
echo "  export LIVEKIT_URL=wss://your-project.livekit.cloud"
echo "  export LIVEKIT_API_KEY=your_key"
echo "  export LIVEKIT_API_SECRET=your_secret"
echo "  export OPENAI_API_KEY=your_key"
echo "  export ELEVEN_API_KEY=your_key"
