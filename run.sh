#!/bin/bash

# Slack2Spotify Bot Runner
echo "🎵 Starting Slack2Spotify Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file based on config.env.example"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run setup if requested
if [ "$1" = "setup" ]; then
    echo "🔐 Running Spotify setup..."
    python setup.py
    exit 0
fi

# Start the bot
echo "🚀 Starting bot..."
python main.py 