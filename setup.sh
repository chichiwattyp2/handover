#!/bin/bash

# WhatsApp Chat Analyzer - Setup Script
# This script helps you set up the application quickly

echo "🚀 WhatsApp Chat Analyzer - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your ANTHROPIC_API_KEY"
    echo "   You can get an API key from: https://console.anthropic.com/"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Run parser test
echo "🧪 Running parser test..."
python test_parser.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup completed successfully!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Edit .env and add your ANTHROPIC_API_KEY"
    echo "   2. Run: source venv/bin/activate (if not already activated)"
    echo "   3. Run: python app.py"
    echo "   4. Open: http://localhost:5000"
    echo ""
else
    echo "⚠️  Parser test had issues, but setup is complete"
    echo "   You can still run the application after adding your API key"
    echo ""
fi
