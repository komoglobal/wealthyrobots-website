#!/bin/bash
# Quick Context Status Updater
echo "📊 REAL-TIME STATUS UPDATE ($(date))"
echo "========================================"
echo ""
echo "🚨 CRITICAL ALERTS:"
if [ -f live_config.json ] && grep -q '"emergency_mode": true' live_config.json; then
    echo "- 🚨 EMERGENCY MODE ACTIVE - Automation paused"
elif [ -f live_config.json ] && grep -q '"posting_enabled": false' live_config.json; then
    echo "- ⚠️ Posting disabled"
else
    echo "- ✅ Systems operational"
fi
echo ""
echo "📈 TODAY'S ACTIVITY:"
echo "- Posts created: $(ls smart_viral_thread_$(date +%Y%m%d)*.txt 2>/dev/null | wc -l)"
echo "- Recent files: $(find . -name "*.json" -o -name "*.log" -o -name "*.txt" -mtime -1 | wc -l) files modified in 24h"
echo "- Running processes: $(ps aux | grep -E "(orchestrator|agent|empire)" | grep -v grep | wc -l)"
echo ""
echo "📝 LATEST CONTENT:"
ls -lt smart_viral_thread*.txt 2>/dev/null | head -3 | awk '{print "- " $9}'
echo ""
echo "========================================"
echo "📚 FULL SYSTEM CONTEXT:"
cat claude_context_summary_latest.md 2>/dev/null || echo "Context file not found"
echo "========================================"
echo "💡 Copy everything above for new Claude chats"
