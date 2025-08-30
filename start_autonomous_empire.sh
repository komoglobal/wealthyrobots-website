#!/bin/bash

# WealthyRobot Autonomous Empire Startup Script
# This script starts the entire empire automatically

cd /home/ubuntu/wealthyrobot

echo "🚀 Starting WealthyRobot Autonomous Empire..."
echo "⏰ $(date)"

# Check if already running
if pgrep -f "wealthyrobot_autonomous_service_simple.py" > /dev/null; then
    echo "✅ Empire already running"
    exit 0
fi

# Start the autonomous service
echo "🎯 Launching autonomous service..."
nohup python3 wealthyrobot_autonomous_service_simple.py > autonomous_empire.log 2>&1 &

# Wait a moment and check if it started
sleep 5
if pgrep -f "wealthyrobot_autonomous_service_simple.py" > /dev/null; then
    echo "✅ Empire started successfully"
    echo "📊 Log file: autonomous_empire.log"
    echo "🔄 Service will run FOREVER without manual intervention"
else
    echo "❌ Failed to start empire"
    exit 1
fi

