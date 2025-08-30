#!/bin/bash

# WealthyRobot Autonomous Trading Fund - Master Deployment Script
# This script sets up the complete autonomous trading fund system

set -e

echo "🚀 WEALTHYROBOT AUTONOMOUS TRADING FUND - DEPLOYMENT"
echo "=================================================="

# Set environment
export TRADING_ENV=production
export AUTONOMOUS_MODE=true

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p logs
mkdir -p config
mkdir -p data
mkdir -p reports
mkdir -p backups
mkdir -p optimized_empire

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Additional dependencies for autonomous fund
echo "📦 Installing autonomous fund dependencies..."
pip install schedule pyyaml

# Check configuration files
echo "⚙️  Checking configuration..."
if [ ! -f "config/production.yaml" ]; then
    echo "⚠️  Production config not found, copying from development..."
    cp config/development.yaml config/production.yaml
fi

if [ ! -f "config/fund_config.yaml" ]; then
    echo "⚠️  Fund config not found, creating default..."
    # Fund config should already be created
fi

# Check wallet configuration
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with wallet credentials."
    exit 1
fi

# Set permissions
echo "🔐 Setting permissions..."
chmod 600 .env
chmod 600 config/*.yaml

# Create systemd service for autonomous fund
echo "⚙️  Creating systemd service for autonomous fund..."
sudo tee /etc/systemd/system/autonomous-trading-fund.service > /dev/null <<EOF
[Unit]
Description=WealthyRobot Autonomous Trading Fund
After=network.target
Wants=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$(pwd)
Environment=TRADING_ENV=production
Environment=AUTONOMOUS_MODE=true
ExecStart=$(pwd)/venv/bin/python3 autonomous_trading_fund.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for agent bridge
echo "⚙️  Creating systemd service for agent bridge..."
sudo tee /etc/systemd/system/agent-bridge.service > /dev/null <<EOF
[Unit]
Description=WealthyRobot Agent Integration Bridge
After=network.target
Wants=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$(pwd)
Environment=TRADING_ENV=production
ExecStart=$(pwd)/venv/bin/python3 agent_integration_bridge.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for enhanced trading system
echo "⚙️  Creating systemd service for enhanced trading system..."
sudo tee /etc/systemd/system/enhanced-trading-system.service > /dev/null <<EOF
[Unit]
Description=WealthyRobot Enhanced Multi-Protocol Trading System
After=network.target
Wants=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$(pwd)
Environment=TRADING_ENV=production
ExecStart=$(pwd)/venv/bin/python3 multi_protocol_trading_system.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable services
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

echo "🔧 Enabling services..."
sudo systemctl enable autonomous-trading-fund.service
sudo systemctl enable agent-bridge.service
sudo systemctl enable enhanced-trading-system.service

# Create startup script
echo "📝 Creating startup script..."
cat > start_autonomous_fund.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting WealthyRobot Autonomous Trading Fund..."

# Start all services
sudo systemctl start autonomous-trading-fund
sudo systemctl start agent-bridge
sudo systemctl start enhanced-trading-system

echo "✅ All services started"
echo ""
echo "📊 Service Status:"
sudo systemctl status autonomous-trading-fund --no-pager -l
echo ""
sudo systemctl status agent-bridge --no-pager -l
echo ""
sudo systemctl status enhanced-trading-system --no-pager -l
echo ""
echo "📋 To view logs:"
echo "   sudo journalctl -u autonomous-trading-fund -f"
echo "   sudo journalctl -u agent-bridge -f"
echo "   sudo journalctl -u enhanced-trading-system -f"
EOF

chmod +x start_autonomous_fund.sh

# Create stop script
echo "📝 Creating stop script..."
cat > stop_autonomous_fund.sh << 'EOF'
#!/bin/bash

echo "🛑 Stopping WealthyRobot Autonomous Trading Fund..."

# Stop all services
sudo systemctl stop autonomous-trading-fund
sudo systemctl stop agent-bridge
sudo systemctl stop enhanced-trading-system

echo "✅ All services stopped"
EOF

chmod +x stop_autonomous_fund.sh

# Create status script
echo "📝 Creating status script..."
cat > status_autonomous_fund.sh << 'EOF'
#!/bin/bash

echo "📊 WealthyRobot Autonomous Trading Fund Status"
echo "============================================="

echo ""
echo "🔧 Service Status:"
sudo systemctl status autonomous-trading-fund --no-pager -l
echo ""
sudo systemctl status agent-bridge --no-pager -l
echo ""
sudo systemctl status enhanced-trading-system --no-pager -l

echo ""
echo "📋 Recent Logs:"
echo "Autonomous Fund:"
sudo journalctl -u autonomous-trading-fund --no-pager -n 10
echo ""
echo "Agent Bridge:"
sudo journalctl -u agent-bridge --no-pager -n 10
echo ""
echo "Enhanced Trading System:"
sudo journalctl -u enhanced-trading-system --no-pager -n 10
EOF

chmod +x status_autonomous_fund.sh

# Create monitoring script
echo "📝 Creating monitoring script..."
cat > monitor_autonomous_fund.sh << 'EOF'
#!/bin/bash

echo "📈 WealthyRobot Autonomous Trading Fund - Real-time Monitoring"
echo "============================================================="

# Start monitoring dashboard
python3 monitor.py
EOF

chmod +x monitor_autonomous_fund.sh

# Create backup script
echo "📝 Creating backup script..."
cat > backup_autonomous_fund.sh << 'EOF'
#!/bin/bash

echo "💾 Creating WealthyRobot Autonomous Trading Fund Backup..."
echo "========================================================"

timestamp=$(date +"%Y%m%d_%H%M%S")
backup_dir="backups/autonomous_fund_backup_$timestamp"

mkdir -p "$backup_dir"

# Backup key files and directories
echo "📁 Backing up configuration..."
cp -r config/ "$backup_dir/"
cp -r logs/ "$backup_dir/"
cp -r reports/ "$backup_dir/"

echo "📄 Backing up source code..."
cp *.py "$backup_dir/"
cp *.sh "$backup_dir/"
cp requirements.txt "$backup_dir/"
cp README.md "$backup_dir/"

echo "🔐 Backing up wallet configuration..."
if [ -f ".env" ]; then
    cp .env "$backup_dir/"
fi

echo "✅ Backup completed: $backup_dir"
echo "📊 Backup size: $(du -sh "$backup_dir" | cut -f1)"
EOF

chmod +x backup_autonomous_fund.sh

# Create upgrade script
echo "📝 Creating upgrade script..."
cat > upgrade_autonomous_fund.sh << 'EOF'
#!/bin/bash

echo "🔄 Upgrading WealthyRobot Autonomous Trading Fund..."
echo "=================================================="

# Stop services
echo "🛑 Stopping services..."
sudo systemctl stop autonomous-trading-fund
sudo systemctl stop agent-bridge
sudo systemctl stop enhanced-trading-system

# Create backup
echo "💾 Creating backup..."
./backup_autonomous_fund.sh

# Pull latest changes (if using git)
if [ -d ".git" ]; then
    echo "📥 Pulling latest changes..."
    git pull origin main
fi

# Update dependencies
echo "📦 Updating dependencies..."
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Restart services
echo "🚀 Restarting services..."
sudo systemctl start autonomous-trading-fund
sudo systemctl start agent-bridge
sudo systemctl start enhanced-trading-system

echo "✅ Upgrade completed successfully!"
EOF

chmod +x upgrade_autonomous_fund.sh

echo ""
echo "✅ AUTONOMOUS TRADING FUND DEPLOYMENT COMPLETED!"
echo "=============================================="
echo ""
echo "📋 Available Commands:"
echo "   ./start_autonomous_fund.sh     - Start all services"
echo "   ./stop_autonomous_fund.sh      - Stop all services"
echo "   ./status_autonomous_fund.sh    - Check service status"
echo "   ./monitor_autonomous_fund.sh   - Open monitoring dashboard"
echo "   ./backup_autonomous_fund.sh    - Create system backup"
echo "   ./upgrade_autonomous_fund.sh   - Upgrade system"
echo ""
echo "🔧 Manual Service Management:"
echo "   sudo systemctl start autonomous-trading-fund"
echo "   sudo systemctl start agent-bridge"
echo "   sudo systemctl start enhanced-trading-system"
echo ""
echo "📊 View Logs:"
echo "   sudo journalctl -u autonomous-trading-fund -f"
echo "   sudo journalctl -u agent-bridge -f"
echo "   sudo journalctl -u enhanced-trading-system -f"
echo ""
echo "🚀 To start the autonomous fund:"
echo "   ./start_autonomous_fund.sh"
echo ""
echo "🤖 The system will automatically:"
echo "   - Discover and integrate all agents"
echo "   - Execute autonomous trading decisions"
echo "   - Monitor system health and self-repair"
echo "   - Check for upgrades and self-upgrade"
echo "   - Scan for new trading strategies"
echo "   - Generate comprehensive reports"
echo ""
echo "🎯 Ready for fully autonomous operation!"
