#!/bin/bash

# Multi-Protocol Trading System Production Deployment Script
# This script sets up the production environment and starts the trading system

set -e

echo "🚀 Deploying Multi-Protocol Trading System..."

# Set environment
export TRADING_ENV=production

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p config
mkdir -p data

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

# Check configuration
if [ ! -f "config/production.yaml" ]; then
    echo "⚠️  Production config not found, copying from development..."
    cp config/development.yaml config/production.yaml
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

# Create systemd service file
echo "⚙️  Creating systemd service..."
sudo tee /etc/systemd/system/multi-protocol-trading.service > /dev/null <<EOF
[Unit]
Description=Multi-Protocol Trading System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$(pwd)
Environment=TRADING_ENV=production
ExecStart=$(pwd)/venv/bin/python3 multi_protocol_trading_system.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl enable multi-protocol-trading.service

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Review configuration in config/production.yaml"
echo "2. Start the service: sudo systemctl start multi-protocol-trading"
echo "3. Check status: sudo systemctl status multi-protocol-trading"
echo "4. View logs: sudo journalctl -u multi-protocol-trading -f"
echo ""
echo "🤖 To start automated trading:"
echo "   python3 multi_protocol_trading_system.py"
echo "   Then select option 5 from the menu"
