#!/bin/bash
# Check deployment status and health

echo "🔍 Checking WealthyRobot Deployment Status"
echo "=========================================="

# Check GitHub repository
echo "📋 GitHub Status:"
if git status --porcelain > /dev/null 2>&1; then
    echo "  ✅ Git repository connected"
    echo "  📍 Remote: $(git remote get-url origin 2>/dev/null || echo 'Not set')"
    echo "  🌿 Branch: $(git branch --show-current)"
else
    echo "  ❌ Git repository not found"
fi

# Check Vercel status
echo ""
echo "🚀 Vercel Status:"
if command -v vercel > /dev/null 2>&1; then
    echo "  ✅ Vercel CLI installed"
    if vercel --version > /dev/null 2>&1; then
        echo "  ✅ Vercel CLI working"
    else
        echo "  ❌ Vercel CLI authentication needed"
    fi
else
    echo "  ❌ Vercel CLI not installed"
fi

# Check website accessibility
echo ""
echo "🌐 Website Status:"
if curl -s --head --fail "https://wealthyrobots.com" > /dev/null 2>&1; then
    echo "  ✅ Website is accessible"
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://wealthyrobots.com")
    echo "  📊 HTTP Status: $HTTP_STATUS"
else
    echo "  ❌ Website is not accessible"
fi

# Check monitoring system
echo ""
echo "📊 Monitoring Status:"
if pgrep -f "deployment_monitor.sh" > /dev/null 2>&1; then
    echo "  ✅ Monitoring system is running"
else
    echo "  ⚠️  Monitoring system not running (check cron jobs)"
fi

# Show recent deployment logs
echo ""
echo "📝 Recent Deployment Logs:"
if [ -f "/home/ubuntu/wealthyrobot/deployment_health.log" ]; then
    tail -5 /home/ubuntu/wealthyrobot/deployment_health.log
else
    echo "  📄 No deployment logs found yet"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Complete Vercel authentication (if needed)"
echo "2. Configure custom domain in Vercel dashboard"
echo "3. Test the autonomous deployment system"
