#!/bin/bash

echo "🚀 Starting WealthyRobot Autonomous Trading Fund..."

# Start all services
sudo systemctl start autonomous-trading-fund
sudo systemctl start agent-bridge

echo "✅ All services started"
echo ""
echo "📊 Service Status:"
sudo systemctl status autonomous-trading-fund --no-pager -l
echo ""
sudo systemctl status agent-bridge --no-pager -l
echo ""
echo "📋 To view logs:"
echo "   sudo journalctl -u autonomous-trading-fund -f"
echo "   sudo journalctl -u agent-bridge -f"
