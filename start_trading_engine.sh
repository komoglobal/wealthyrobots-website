#!/bin/bash
# WealthyRobot Trading Engine with Virtual Environment

cd /home/ubuntu/wealthyrobot

# Activate virtual environment
source trading_env/bin/activate

# Set Python path to include our fallback modules
export PYTHONPATH="$PWD/trading_env/lib/python3.12/site-packages:$PYTHONPATH"

# Start the trading engine
echo "🚀 Starting WealthyRobot Trading Engine with SDKs..."
./trading_env/bin/python3 run_hybrid_trading_empire.py
