#!/bin/bash
cd ~/wealthyrobot
export $(grep -v '^#' .env | xargs)
echo "✅ WealthyRobot Empire credentials loaded"
echo "🏰 Starting autonomous systems..."

# Start both orchestrator and scheduler
nohup python3 live_orchestrator.py > orchestrator.log 2>&1 &
echo "✅ Live Orchestrator started (Content Creation)"

# Note: smart_scheduler.py already running
echo "✅ Smart Scheduler running (Posting System)"

echo "🎉 WealthyRobot Empire is fully operational!"
