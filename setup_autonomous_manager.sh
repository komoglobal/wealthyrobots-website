#!/bin/bash
# Setup Autonomous Data Manager Cron Job
# This script installs the hourly autonomous data manager

echo "🚀 Setting up Autonomous Data Manager..."

# Make script executable
chmod +x /home/ubuntu/wealthyrobot/autonomous_data_manager.sh

# Add to crontab (hourly at minute 0)
(crontab -l 2>/dev/null; echo "0 * * * * /home/ubuntu/wealthyrobot/autonomous_data_manager.sh") | crontab -

echo "✅ Autonomous Data Manager scheduled for hourly execution"
echo "📋 Cron schedule: 0 * * * * (every hour at minute 0)"
echo "📄 Log file: /home/ubuntu/wealthyrobot/autonomous_manager.log"

# Verify installation
echo "📋 Current crontab entries:"
crontab -l | grep autonomous_data_manager

echo ""
echo "🎉 Setup complete! The autonomous data manager will run hourly."
echo "🔍 Monitor progress: tail -f /home/ubuntu/wealthyrobot/autonomous_manager.log"
