#!/bin/bash

echo "📊 WealthyRobot Autonomous Trading Fund Status"
echo "============================================="

echo ""
echo "🔧 Service Status:"
sudo systemctl status autonomous-trading-fund --no-pager -l
echo ""
sudo systemctl status agent-bridge --no-pager -l

echo ""
echo "📋 Recent Logs:"
echo "Autonomous Fund:"
sudo journalctl -u autonomous-trading-fund --no-pager -n 10
echo ""
echo "Agent Bridge:"
sudo journalctl -u agent-bridge --no-pager -n 10
