#!/bin/bash
# Autonomous Deployment Monitor
WEBSITE_URL="https://wealthyrobots.com"
LOG_FILE="/home/ubuntu/wealthyrobot/deployment_health.log"
PROJECT_DIR="/home/ubuntu/wealthyrobot"

echo "$(date): Checking deployment health..." >> $LOG_FILE

# Check if website is accessible
if curl -s --head --fail "$WEBSITE_URL" > /dev/null 2>&1; then
    echo "$(date): ✅ Website is healthy" >> $LOG_FILE
else
    echo "$(date): ❌ Website is down - triggering redeploy" >> $LOG_FILE
    cd $PROJECT_DIR

    # Quick redeploy
    git add .
    git commit -m "Emergency redeploy - $(date)" 2>/dev/null || true
    git push origin main 2>/dev/null || true

    echo "$(date): Redeploy attempt completed" >> $LOG_FILE
fi
