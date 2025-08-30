#!/bin/bash

echo "🚀 STARTING ENHANCED COMPREHENSIVE TRADING FIRM INTEGRATION..."
echo "================================================================"

# Check if virtual environment exists
if [ ! -d "trading_firm_env" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv trading_firm_env
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source trading_firm_env/bin/activate

# Install dependencies if needed
echo "📦 Checking dependencies..."
if ! python -c "import numpy, pandas, aiohttp" 2>/dev/null; then
    echo "📥 Installing required dependencies..."
    pip install numpy pandas aiohttp
    echo "✅ Dependencies installed"
else
    echo "✅ All dependencies already available"
fi

# Start the enhanced integration system
echo "🏢 Launching Enhanced Comprehensive Trading Firm Integration..."
echo "================================================================"

# Run the enhanced integration system
python enhanced_comprehensive_integration.py

echo "🛑 Enhanced Integration System stopped"
