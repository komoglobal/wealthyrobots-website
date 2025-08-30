# 🚀 Multi-Protocol Trading System

A sophisticated, production-ready trading system that automatically detects and executes opportunities across multiple DeFi protocols on the Algorand blockchain.

## ✨ Features

### 🔗 **Multi-Protocol Support**
- **Tinyman** - DEX trading and liquidity provision
- **Pact Finance** - Yield farming and staking
- **Folks Finance** - Lending and borrowing
- **Arbitrage Detection** - Cross-protocol opportunity identification

### 🧠 **Smart Opportunity Detection**
- **Advanced Scoring Algorithm** - Multi-factor opportunity ranking
- **Risk Assessment** - Comprehensive risk scoring and management
- **Arbitrage Detection** - Automatic cross-protocol opportunity identification
- **Real-time Scanning** - Continuous market monitoring

### 🛡️ **Risk Management**
- **Position Sizing** - Configurable trade size limits
- **Portfolio Risk Limits** - Maximum portfolio exposure controls
- **Stop-Loss & Take-Profit** - Automated risk mitigation
- **Protocol-Specific Limits** - Individual protocol risk controls

### 🤖 **Automation & Monitoring**
- **Automated Trading** - Scheduled opportunity scanning and execution
- **Real-time Monitoring** - Live system health and performance tracking
- **Performance Metrics** - Comprehensive trading analytics
- **Health Checks** - Continuous system status monitoring

### ⚙️ **Production Ready**
- **Environment Configuration** - Development/Production configs
- **Comprehensive Logging** - Detailed audit trails
- **Systemd Service** - Production deployment automation
- **Error Handling** - Graceful failure recovery

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd wealthyrobot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configuration**
```bash
# Set environment
export TRADING_ENV=development  # or production

# Configure wallet (create .env file)
echo "ALGORAND_WALLET_ADDRESS=your_wallet_address" > .env
echo "ALGORAND_WALLET_MNEMONIC=your_wallet_mnemonic" >> .env
```

### 3. **Run the System**
```bash
# Interactive mode
python3 multi_protocol_trading_system.py

# Automated trading
python3 multi_protocol_trading_system.py
# Select option 5 from the menu

# Real-time monitoring
python3 monitor.py
```

## 📊 **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Multi-Protocol Trading System            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Tinyman   │  │    Pact     │  │    Folks    │        │
│  │   Client    │  │   Client    │  │   Client    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   AlgoFi    │  │ Smart API   │  │   Risk      │        │
│  │   Client    │  │  Ranker     │  │ Management  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Opportunity │  │ Automated   │  │ Monitoring  │        │
│  │  Detection  │  │  Trading    │  │  Dashboard  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 **Opportunity Detection Algorithm**

### **Scoring Factors**
1. **APY Contribution** (0-50 points)
   - Base score from estimated annual yield
   - Capped at 50 points for risk management

2. **Liquidity Bonus** (0-20 points)
   - High liquidity pools get bonus points
   - Reduces execution risk

3. **Risk Adjustment** (0-30 points deducted)
   - Protocol reputation scoring
   - Opportunity type risk assessment
   - Liquidity and utilization factors

4. **Protocol Reputation** (0-20 points)
   - Established protocols get bonus points
   - Historical reliability scoring

5. **Arbitrage Bonus** (25 points)
   - Cross-protocol arbitrage opportunities
   - Lower risk, higher reward

### **Risk Scoring**
- **Protocol Risk**: 0.1-0.5 based on protocol maturity
- **Type Risk**: 0.1-0.5 based on opportunity type
- **Liquidity Risk**: -0.2 to +0.3 based on pool size
- **APY Risk**: -0.1 to +0.2 based on yield levels

## ⚙️ **Configuration**

### **Environment Files**
- `config/development.yaml` - Development settings
- `config/production.yaml` - Production settings

### **Key Configuration Options**
```yaml
# Testing vs Production Mode
testing_mode: true      # true = self-to-self transactions (testing)
                        # false = real DeFi trades (production)

trading:
  max_position_size: 0.1      # Maximum ALGO per trade
  min_position_size: 0.001    # Minimum ALGO per trade
  max_daily_trades: 10        # Daily trade limit

risk_management:
  max_portfolio_risk: 0.3     # 30% max portfolio risk
  stop_loss_percentage: 0.15  # 15% stop loss
  take_profit_percentage: 0.25 # 25% take profit

protocols:
  tinyman:
    enabled: true
    max_slippage: 0.5         # 0.5% max slippage
    gas_limit: 1000000        # Gas limit for transactions
```

## 🚀 **Production Deployment**

### **Automated Deployment**
```bash
# Run deployment script
./deploy.sh

# Start systemd service
sudo systemctl start multi-protocol-trading

# Check status
sudo systemctl status multi-protocol-trading

# View logs
sudo journalctl -u multi-protocol-trading -f
```

### **Manual Deployment**
```bash
# Set production environment
export TRADING_ENV=production

# Start the system
python3 multi_protocol_trading_system.py

# Start automated trading
# Select option 5 from the interactive menu
```

## 📈 **Monitoring & Analytics**

### **Real-time Dashboard**
```bash
# Start monitoring dashboard
python3 monitor.py

# Controls:
# q - Quit
# r - Refresh
# s - Scan opportunities
```

### **Performance Metrics**
- **Opportunity Count** - Total opportunities found
- **Trade Success Rate** - Execution success percentage
- **Portfolio Performance** - Overall return metrics
- **System Health** - Protocol and API status

### **Log Files**
- `logs/trading_system_YYYYMMDD.log` - Daily trading logs
- `logs/performance_metrics_YYYYMMDD.json` - Performance data
- Systemd journal logs for production deployments

## 🔒 **Security Features**

### **Risk Controls**
- **Position Size Limits** - Maximum trade size restrictions
- **Portfolio Risk Limits** - Overall exposure controls
- **Protocol Restrictions** - Disable specific protocols
- **Confirmation Requirements** - Manual trade approval (production)

### **Access Control**
- **Environment Isolation** - Separate dev/prod configs
- **Secure Credentials** - Encrypted wallet storage
- **Permission Management** - File and service permissions

## 🧪 **Testing & Development**

### **Development Mode**
```bash
export TRADING_ENV=development
python3 multi_protocol_trading_system.py
```

### **Testing Mode vs Production Mode**
- **Testing Mode** (`testing_mode: true`):
  - Uses self-to-self transactions to validate infrastructure
  - Safe for development and testing
  - No real DeFi trades executed
  - Validates transaction signing, submission, and confirmation

- **Production Mode** (`testing_mode: false`):
  - Executes real DeFi trades on actual protocols
  - Uses real DeFi SDKs for swaps, liquidity provision, etc.
  - Requires proper risk management and monitoring

### **Why Self-to-Self Transactions?**
The system uses self-to-self transactions during testing to:
1. **Validate Infrastructure** - Test transaction signing, submission, and confirmation
2. **Safety First** - No risk of losing funds during development
3. **Protocol Validation** - Test DeFi protocol connections without executing trades
4. **System Testing** - Validate the entire trading pipeline safely

## 📚 **API Reference**

### **Core Classes**

#### **MultiProtocolTradingSystem**
- `scan_all_opportunities()` - Scan all protocols
- `find_best_opportunities(limit=5)` - Get top opportunities
- `execute_best_opportunity(amount)` - Execute best trade
- `start_automated_trading(interval)` - Start automation

#### **SmartAPIRanker**
- `get_current_rankings()` - Get API endpoint rankings
- `test_all_connectivity()` - Test all endpoints
- `get_network_endpoints()` - Get best network endpoints

### **Key Methods**
```python
# Initialize system
trading_system = MultiProtocolTradingSystem()

# Scan for opportunities
opportunities = trading_system.scan_all_opportunities()

# Get best opportunities with scoring
best_opps = trading_system.find_best_opportunities(opportunities, limit=5)

# Execute trade
success = trading_system.execute_best_opportunity(amount=0.01)

# Start automated trading
trading_system.start_automated_trading(interval_minutes=5)

# Monitor system health
health = trading_system.monitor_system_health()
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check Python environment
python3 --version
which python3
```

#### **API Connection Issues**
- Check network connectivity
- Verify API endpoint URLs
- Review rate limiting settings
- Check wallet configuration

#### **Trade Execution Failures**
- Verify wallet balance
- Check risk management settings
- Review protocol-specific limits
- Examine transaction logs

### **Debug Mode**
```bash
# Set debug logging
export TRADING_ENV=development
# Edit config/development.yaml: log_level: DEBUG

# Run with verbose output
python3 multi_protocol_trading_system.py
```

## 🤝 **Contributing**

### **Development Setup**
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

### **Code Standards**
- Follow PEP 8 style guide
- Add comprehensive docstrings
- Include error handling
- Write unit tests

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ **Disclaimer**

**This software is for educational and research purposes only. Trading cryptocurrencies involves substantial risk of loss and is not suitable for all investors. The value of cryptocurrencies can go down as well as up, and you may lose some or all of your investment. Past performance does not guarantee future results.**

- **No Financial Advice**: This software does not constitute financial advice
- **Risk Warning**: Cryptocurrency trading is highly risky
- **Testing**: Always test with small amounts first
- **Regulations**: Ensure compliance with local regulations

## 🆘 **Support**

### **Documentation**
- Check this README first
- Review configuration files
- Examine log files for errors

### **Issues**
- Search existing issues
- Create new issue with details
- Include error logs and configuration

### **Community**
- Join our Discord/Telegram
- Participate in discussions
- Share experiences and improvements

---

**🚀 Ready to start automated multi-protocol trading on Algorand? Let's go!**
