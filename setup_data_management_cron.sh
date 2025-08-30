#!/bin/bash
# Setup script for Data Management Agent cron job

echo "🔧 Setting up Data Management Agent cron job..."

# Create the cron job entry (runs every 6 hours)
CRON_JOB="0 */6 * * * /usr/bin/python3 /home/ubuntu/wealthyrobot/data_management_agent.py >> /home/ubuntu/wealthyrobot/logs/data_management_cron.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job added: $CRON_JOB"
echo "📅 Data Management Agent will run every 6 hours"
echo "📝 Logs will be written to: logs/data_management_cron.log"

# Create logs directory if it doesn't exist
mkdir -p logs

# Make the agent executable
chmod +x data_management_agent.py

echo "🎯 Setup complete! The agent will automatically clean duplicates every 6 hours."
echo "💡 You can manually run it anytime with: python3 data_management_agent.py"
