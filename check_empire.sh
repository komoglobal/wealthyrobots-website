#!/bin/bash
echo "🏰 WEALTHYROBOT EMPIRE STATUS"
echo "============================="
echo "📊 Revenue System:"
if pgrep -f "automated_twitter_revenue.py" > /dev/null; then
    echo "✅ RUNNING - Posting every 2 hours"
else
    echo "❌ STOPPED - Restart with: nohup python3 automated_twitter_revenue.py &"
fi

echo ""
echo "🛡️ API Safety:"
python3 twitter_api_monitor.py

echo ""
echo "📈 Empire Agents:"
ps aux | grep -E "(empire|agent|orchestrator)" | grep -v grep | wc -l | xargs echo "Active agents:"

echo ""
echo "🔗 Your Live Tweets:"
echo "  https://twitter.com/WealthyRobot/status/1952904173378298240"
echo "  https://twitter.com/WealthyRobot/status/1952904490891248037"
