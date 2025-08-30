#!/bin/bash

echo "🚀 INSTALLING WEALTHYROBOT AUTONOMOUS SERVICE"
echo "=============================================="
echo "🎯 This will make your empire run FOREVER without manual intervention"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   echo "💡 Run as ubuntu user instead"
   exit 1
fi

# Check if we're in the right directory
if [[ ! -f "wealthyrobot_autonomous_service.py" ]]; then
    echo "❌ Please run this script from the wealthyrobot directory"
    exit 1
fi

echo "🔧 Installing required dependencies..."
sudo apt-get update
sudo apt-get install -y python3-psutil

echo "📦 Installing Python dependencies..."
pip3 install psutil

echo "🔐 Setting up systemd service..."

# Copy service file to systemd directory
sudo cp wealthyrobot-autonomous.service /etc/systemd/system/

# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable wealthyrobot-autonomous.service

echo "✅ Service installed and enabled!"
echo ""
echo "🎯 SERVICE STATUS:"
echo "=================="
echo "📋 Service Name: wealthyrobot-autonomous.service"
echo "🚀 Auto-start: ENABLED (will start on every boot)"
echo "🔄 Auto-restart: ENABLED (will restart if it fails)"
echo "📊 Logs: journalctl -u wealthyrobot-autonomous.service"
echo ""
echo "🎮 COMMANDS YOU CAN USE:"
echo "========================"
echo "  🚀 Start now:     sudo systemctl start wealthyrobot-autonomous"
echo "  🛑 Stop:          sudo systemctl stop wealthyrobot-autonomous"
echo "  🔄 Restart:       sudo systemctl restart wealthyrobot-autonomous"
echo "  📊 Status:        sudo systemctl status wealthyrobot-autonomous"
echo "  📋 Logs:          sudo journalctl -u wealthyrobot-autonomous -f"
echo "  🚫 Disable:       sudo systemctl disable wealthyrobot-autonomous"
echo ""
echo "🎯 WHAT HAPPENS NOW:"
echo "===================="
echo "✅ Service is installed and enabled"
echo "✅ Will start automatically on next boot"
echo "✅ Will restart automatically if it fails"
echo "✅ Your empire will run FOREVER without you"
echo ""
echo "🚀 To start the service NOW (optional):"
echo "   sudo systemctl start wealthyrobot-autonomous"
echo ""
echo "🎊 INSTALLATION COMPLETE!"
echo "🎯 Your WealthyRobot Empire is now FULLY AUTONOMOUS!"

