#!/bin/bash
echo "🏰 WEALTHYROBOT EMPIRE MONITORING DASHBOARD"
echo "=========================================="
echo "📅 $(date)"
echo ""

echo "🔄 ACTIVE SYSTEMS:"
scheduler_pid=$(pgrep -f smart_scheduler.py)
orchestrator_pid=$(pgrep -f live_orchestrator.py)

if [ "$scheduler_pid" ]; then
    echo "✅ Smart Scheduler: RUNNING (PID: $scheduler_pid)"
else
    echo "❌ Smart Scheduler: STOPPED"
fi

if [ "$orchestrator_pid" ]; then
    echo "✅ Enhanced Orchestrator: RUNNING (PID: $orchestrator_pid)"
else
    echo "❌ Enhanced Orchestrator: STOPPED"  
fi

echo ""
echo "📝 LATEST CONTENT:"
latest_content=$(ls -t smart_viral_thread*.txt 2>/dev/null | head -1)
if [ "$latest_content" ]; then
    echo "📄 $latest_content"
    echo "🕒 Created: $(stat -c %y "$latest_content" | cut -d. -f1)"
else
    echo "❌ No content files found"
fi

echo ""
echo "🎯 NEXT ACTIONS:"
echo "• Content creation: Tonight ~1:00 AM EDT (±30min)"
echo "• Format: 6-tweet educational thread"  
echo "• Strategy: 80% educational, 20% promotional"
echo "• Visual: Auto-detection active"

echo ""
echo "🌐 LIVE TWEETS:"
echo "https://twitter.com/WealthyRobot/status/1953229304717779354"
echo "https://twitter.com/WealthyRobot/status/1953242390614946199"

echo ""
echo "💰 REVENUE READY: Amazon affiliate (wealthyrobot-20) integrated"
echo "🚀 STATUS: FULLY AUTONOMOUS EMPIRE OPERATIONAL!"
