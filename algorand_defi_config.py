#!/usr/bin/env python3
"""
Algorand DeFi Trading Configuration
Environment variables and settings for real Algorand DeFi trading
"""

import os
from typing import Dict, Any

class AlgorandDeFiConfig:
    """Configuration class for Algorand DeFi trading"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        
        # Network Configuration
        self.network = os.getenv('ALGORAND_NETWORK', 'mainnet')
        self.algod_address = os.getenv('ALGOD_ADDRESS', 'https://mainnet-api.algonode.cloud')
        self.algod_token = os.getenv('ALGOD_TOKEN', '')
        
        # Wallet Configuration
        self.wallet_mnemonic = os.getenv('ALGORAND_WALLET_MNEMONIC', '')
        self.wallet_address = os.getenv('ALGORAND_WALLET_ADDRESS', '')
        
        # Trading Parameters
        self.max_position_size_algo = float(os.getenv('MAX_POSITION_SIZE_ALGO', '100'))
        self.max_daily_trades = int(os.getenv('MAX_DAILY_TRADES', '10'))
        self.risk_per_trade = float(os.getenv('RISK_PER_TRADE', '0.05'))
        self.slippage_tolerance = float(os.getenv('SLIPPAGE_TOLERANCE', '0.02'))
        
        # DeFi Protocol Settings
        self.enabled_protocols = os.getenv('ENABLED_PROTOCOLS', 'tinyman,pact,folks_finance').split(',')
        self.preferred_protocol = os.getenv('PREFERRED_PROTOCOL', 'tinyman')
        
        # Risk Management
        self.max_portfolio_risk = float(os.getenv('MAX_PORTFOLIO_RISK', '0.20'))
        self.daily_loss_limit = float(os.getenv('DAILY_LOSS_LIMIT', '0.05'))
        self.position_size_limit = float(os.getenv('POSITION_SIZE_LIMIT', '0.10'))
        
        # Market Data
        self.market_data_interval = int(os.getenv('MARKET_DATA_INTERVAL', '30'))
        self.price_update_frequency = int(os.getenv('PRICE_UPDATE_FREQUENCY', '10'))
        
        # Trading Strategies
        self.enabled_strategies = os.getenv('ENABLED_STRATEGIES', 'momentum,mean_reversion,yield_farming,arbitrage').split(',')
        self.strategy_weights = {
            'momentum': float(os.getenv('MOMENTUM_WEIGHT', '0.25')),
            'mean_reversion': float(os.getenv('MEAN_REVERSION_WEIGHT', '0.25')),
            'yield_farming': float(os.getenv('YIELD_FARMING_WEIGHT', '0.25')),
            'arbitrage': float(os.getenv('ARBITRAGE_WEIGHT', '0.25'))
        }
        
        # Asset Configuration
        self.trading_pairs = [
            {'base': 'ALGO', 'quote': 'USDC', 'min_amount': 1.0, 'max_amount': 100.0},
            {'base': 'ALGO', 'quote': 'USDT', 'min_amount': 1.0, 'max_amount': 100.0},
            {'base': 'ALGO', 'quote': 'STBL', 'min_amount': 1.0, 'max_amount': 100.0},
            {'base': 'USDC', 'quote': 'USDT', 'min_amount': 10.0, 'max_amount': 1000.0},
            {'base': 'USDC', 'quote': 'STBL', 'min_amount': 10.0, 'max_amount': 1000.0}
        ]
        
        # Fee Structure
        self.protocol_fees = {
            'tinyman': 0.005,      # 0.5%
            'pact': 0.003,         # 0.3%
            'folks_finance': 0.004, # 0.4%
            'algofi': 0.006        # 0.6%
        }
        
        # Slippage Protection
        self.slippage_limits = {
            'tinyman': 0.02,       # 2%
            'pact': 0.01,          # 1%
            'folks_finance': 0.03, # 3%
            'algofi': 0.025        # 2.5%
        }
        
        # Liquidity Requirements
        self.min_liquidity_algo = float(os.getenv('MIN_LIQUIDITY_ALGO', '10000'))
        self.min_volume_24h = float(os.getenv('MIN_VOLUME_24H', '5000'))
        
        # Performance Tracking
        self.performance_metrics = {
            'track_pnl': True,
            'track_sharpe_ratio': True,
            'track_max_drawdown': True,
            'track_win_rate': True
        }
        
        # Notifications
        self.notifications = {
            'trade_executed': True,
            'position_closed': True,
            'risk_alert': True,
            'daily_summary': True
        }
        
        # Logging
        self.logging = {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'file': os.getenv('LOG_FILE', 'algorand_defi_trading.log'),
            'max_size_mb': int(os.getenv('LOG_MAX_SIZE_MB', '100')),
            'backup_count': int(os.getenv('LOG_BACKUP_COUNT', '5'))
        }
        
        return self.get_config_dict()
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return {
            'network': self.network,
            'algod_address': self.algod_address,
            'wallet_address': self.wallet_address[:10] + '...' if self.wallet_address else None,
            'max_position_size_algo': self.max_position_size_algo,
            'max_daily_trades': self.max_daily_trades,
            'risk_per_trade': self.risk_per_trade,
            'enabled_protocols': self.enabled_protocols,
            'preferred_protocol': self.preferred_protocol,
            'enabled_strategies': self.enabled_strategies,
            'trading_pairs': len(self.trading_pairs),
            'min_liquidity_algo': self.min_liquidity_algo
        }
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate configuration and return any issues"""
        issues = []
        warnings = []
        
        # Check required settings
        if not self.wallet_mnemonic and not self.wallet_address:
            issues.append("No wallet configured (ALGORAND_WALLET_MNEMONIC or ALGORAND_WALLET_ADDRESS)")
        
        if self.network == 'mainnet' and not self.algod_token:
            warnings.append("No ALGOD_TOKEN set for mainnet (may hit rate limits)")
        
        if self.max_position_size_algo > 1000:
            warnings.append("Large position size configured (>1000 ALGO)")
        
        if self.risk_per_trade > 0.10:
            warnings.append("High risk per trade (>10%)")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
    
    def print_config_summary(self):
        """Print configuration summary"""
        print("🟢 ALGORAND DEFI TRADING CONFIGURATION")
        print("=" * 50)
        
        config = self.get_config_dict()
        for key, value in config.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Validate configuration
        validation = self.validate_config()
        print("\n🔍 CONFIGURATION VALIDATION:")
        if validation['valid']:
            print("   ✅ Configuration is valid")
        else:
            print("   ❌ Configuration has issues:")
            for issue in validation['issues']:
                print(f"      - {issue}")
        
        if validation['warnings']:
            print("   ⚠️ Warnings:")
            for warning in validation['warnings']:
                print(f"      - {warning}")
        
        print("\n📋 NEXT STEPS:")
        if not validation['valid']:
            print("   1. Fix configuration issues above")
            print("   2. Set required environment variables")
            print("   3. Restart the trading agent")
        else:
            print("   1. Configuration is ready")
            print("   2. Start trading with: python3 algorand_defi_trading_agent.py")
            print("   3. Monitor performance and adjust parameters")

def create_env_template():
    """Create environment variables template file"""
    template = """# Algorand DeFi Trading Environment Variables
# Copy this to .env file and fill in your values

# Network Configuration
ALGORAND_NETWORK=mainnet
ALGOD_ADDRESS=https://mainnet-api.algonode.cloud
ALGOD_TOKEN=your_algod_token_here

# Wallet Configuration (REQUIRED - Choose one)
ALGORAND_WALLET_MNEMONIC=your_25_word_mnemonic_phrase_here
# ALGORAND_WALLET_ADDRESS=your_wallet_address_here

# Trading Parameters
MAX_POSITION_SIZE_ALGO=100
MAX_DAILY_TRADES=10
RISK_PER_TRADE=0.05
SLIPPAGE_TOLERANCE=0.02

# Risk Management
MAX_PORTFOLIO_RISK=0.20
DAILY_LOSS_LIMIT=0.05
POSITION_SIZE_LIMIT=0.10

# DeFi Protocols
ENABLED_PROTOCOLS=tinyman,pact,folks_finance
PREFERRED_PROTOCOL=tinyman

# Trading Strategies
ENABLED_STRATEGIES=momentum,mean_reversion,yield_farming,arbitrage
MOMENTUM_WEIGHT=0.25
MEAN_REVERSION_WEIGHT=0.25
YIELD_FARMING_WEIGHT=0.25
ARBITRAGE_WEIGHT=0.25

# Market Data
MARKET_DATA_INTERVAL=30
PRICE_UPDATE_FREQUENCY=10

# Liquidity Requirements
MIN_LIQUIDITY_ALGO=10000
MIN_VOLUME_24H=5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=algorand_defi_trading.log
LOG_MAX_SIZE_MB=100
LOG_BACKUP_COUNT=5
"""
    
    with open('.env.template', 'w') as f:
        f.write(template)
    
    print("📝 Created .env.template file")
    print("   Copy to .env and fill in your values")

if __name__ == "__main__":
    # Load and display configuration
    config = AlgorandDeFiConfig()
    config.print_config_summary()
    
    # Create environment template
    create_env_template()

















