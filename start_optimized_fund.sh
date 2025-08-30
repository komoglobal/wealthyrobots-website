#!/bin/bash

echo "🚀 Starting WealthyRobot Optimized Trading Fund..."
echo "🔧 Integrating with existing optimization systems..."

# Check if services are already running
if systemctl is-active --quiet autonomous-trading-fund; then
    echo "⚠️  Autonomous fund already running, restarting for optimization..."
    sudo systemctl restart autonomous-trading-fund
else
    sudo systemctl start autonomous-trading-fund
fi

if systemctl is-active --quiet agent-bridge; then
    echo "⚠️  Agent bridge already running, restarting for optimization..."
    sudo systemctl restart agent-bridge
else
    sudo systemctl start agent-bridge
fi

# Wait for services to stabilize
echo "⏳ Waiting for services to stabilize..."
sleep 5

echo "✅ All services started and optimized"
echo ""
echo "📊 Service Status:"
sudo systemctl status autonomous-trading-fund --no-pager -l
echo ""
sudo systemctl status agent-bridge --no-pager -l

echo ""
echo "🔍 System Integration Status:"
echo "   - Using systemd journal for logging (no file spam)"
echo "   - Quiet mode enabled (minimal console output)"
echo "   - Performance optimized for existing systems"
echo "   - Background priority set to low"
echo ""

echo "📋 Monitoring Commands:"
echo "   Status: ./status_autonomous_fund.sh"
echo "   Live Logs: sudo journalctl -u autonomous-trading-fund -f"
echo "   Agent Bridge: sudo journalctl -u agent-bridge -f"
echo "   System Resources: htop"
echo ""
echo "🎯 System is now running autonomously with your existing optimization infrastructure!"



