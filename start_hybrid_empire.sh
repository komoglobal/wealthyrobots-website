#!/bin/bash
# Start Hybrid Algorand Trading Empire
# Combines AlgoFund reliability with advanced trading capabilities

echo "🚀 STARTING HYBRID ALGORAND TRADING EMPIRE"
echo "=========================================="
echo "🎯 Combining AlgoFund reliability + Advanced trading capabilities"
echo "🔧 Best of both worlds: Working pools + Advanced systems"
echo ""

# Check if we're in the right directory
if [ ! -f "hybrid_algorand_trading_empire.py" ]; then
    echo "❌ Error: hybrid_algorand_trading_empire.py not found"
    echo "   Please run this script from the wealthyrobot directory"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 not found"
    echo "   Please install Python3 to run the hybrid empire"
    exit 1
fi

# Check if required files exist
echo "🔍 Checking system components..."
required_files=(
    "hybrid_algorand_trading_empire.py"
    "config/hybrid_empire_config.yaml"
    "algofund/pool_health_report_*.json"
    "opportunities/real_opportunities_*.json"
)

missing_files=()
for pattern in "${required_files[@]}"; do
    if ! ls $pattern &> /dev/null; then
        missing_files+=("$pattern")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "⚠️  Warning: Some required files are missing:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo "   The system may not function optimally"
fi

# Check AlgoFund status
echo "🏦 Checking AlgoFund status..."
if systemctl is-active --quiet algofund-paper.service; then
    echo "   ✅ AlgoFund paper trading service is running"
    ALGOFUND_STATUS="active"
else
    echo "   ⚠️  AlgoFund paper trading service is not running"
    ALGOFUND_STATUS="inactive"
fi

# Check if hybrid system is already running
echo "🔍 Checking if hybrid system is already running..."
if pgrep -f "hybrid_algorand_trading_empire.py" > /dev/null; then
    echo "   ⚠️  Hybrid system is already running"
    echo "   Stopping existing process..."
    pkill -f "hybrid_algorand_trading_empire.py"
    sleep 2
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p hybrid_data
mkdir -p opportunities

# Set up Python environment
echo "🐍 Setting up Python environment..."
if [ -d "venv" ]; then
    echo "   Using existing virtual environment"
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "   Using existing virtual environment (.venv)"
    source .venv/bin/activate
else
    echo "   No virtual environment found, using system Python"
fi

# Check Python dependencies
echo "📦 Checking Python dependencies..."
python3 -c "
import sys
required_modules = ['asyncio', 'json', 'logging', 'datetime', 'typing']
missing_modules = []

for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print(f'❌ Missing modules: {missing_modules}')
    print('Please install required dependencies')
    sys.exit(1)
else:
    print('✅ All required modules available')
"

if [ $? -ne 0 ]; then
    echo "❌ Dependency check failed"
    exit 1
fi

# Start the hybrid empire
echo "🚀 Starting Hybrid Algorand Trading Empire..."
echo "   This will combine:"
echo "   - AlgoFund's reliable pool connections"
echo "   - Real Trading Empire's advanced capabilities"
echo "   - Autonomous Trading Fund's multi-agent system"
echo "   - Multi-Protocol System's protocol integration"
echo "   - Firm Coordination System's agent coordination"
echo "   🚀 REAL TRADING EXECUTION ENABLED - Will execute actual DeFi trades!"
echo "   🔗 BLOCKCHAIN INTEGRATION ACTIVE - Real Algorand transactions!"
echo ""

# Run the hybrid empire
echo "🎯 Launching hybrid system..."
python3 hybrid_algorand_trading_empire.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "✅ Hybrid empire stopped gracefully"
else
    echo "❌ Hybrid empire encountered an error"
    echo "   Check logs/hybrid_empire_*.log for details"
fi

echo ""
echo "🔍 To monitor the hybrid system:"
echo "   - Check status: tail -f logs/hybrid_empire_*.log"
echo "   - View data: ls -la hybrid_data/"
echo "   - Monitor processes: ps aux | grep hybrid"
echo ""
echo "🛑 Hybrid Algorand Trading Empire stopped"
