#!/bin/bash

# Quick Deployment Script for Bot Services
# This script helps you deploy both Flask backend and Rasa bot

echo "🚀 Quick Deployment Script for Bot Services"
echo "=========================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
else
    echo "✅ Railway CLI already installed"
fi

# Check if user is logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway. Please login first:"
    echo "   railway login"
    exit 1
fi

echo ""
echo "📁 Deploying Flask Backend (bot/backend/)..."
echo "=========================================="

cd bot/backend

# Initialize Railway project if not already done
if [ ! -f ".railway" ]; then
    echo "🔧 Initializing Railway project..."
    railway init
fi

# Set environment variables
echo "🔐 Setting environment variables..."
echo "   Please enter your Gmail credentials:"
read -p "   Gmail Email: " GMAIL_EMAIL
read -s -p "   Gmail App Password: " GMAIL_PASSWORD
echo ""

railway variables set EMAIL_HOST=smtp.gmail.com
railway variables set EMAIL_PORT=587
railway variables set EMAIL_USERNAME=$GMAIL_EMAIL
railway variables set EMAIL_PASSWORD=$GMAIL_PASSWORD

# Deploy
echo "🚀 Deploying Flask backend..."
railway up

echo ""
echo "📁 Deploying Rasa Bot..."
echo "=========================================="

cd ../..

# Initialize Railway project for Rasa if not already done
if [ ! -f "bot/.railway" ]; then
    echo "🔧 Initializing Railway project for Rasa..."
    cd bot
    railway init
    cd ..
fi

cd bot

# Set Rasa environment variables
echo "🔐 Setting Rasa environment variables..."
railway variables set RASA_MODEL_PATH=models/
railway variables set RASA_ACTIONS_URL=https://your-actions-url.railway.app

# Deploy Rasa
echo "🚀 Deploying Rasa bot..."
railway up

echo ""
echo "✅ Deployment completed!"
echo ""
echo "🔗 Your services are now deployed:"
echo "   - Flask Backend: Check Railway dashboard for URL"
echo "   - Rasa Bot: Check Railway dashboard for URL"
echo ""
echo "📝 Next steps:"
echo "   1. Update your frontend URLs"
echo "   2. Test all endpoints"
echo "   3. Configure CORS if needed"
echo "   4. Set up monitoring"
echo ""
echo "📚 For detailed instructions, see:"
echo "   - bot/DEPLOYMENT_GUIDE.md"
echo "   - gvkss/bot-backend/DEPLOYMENT_GUIDE.md"
