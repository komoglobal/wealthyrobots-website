#!/usr/bin/env python3
"""
Enhanced Algorand DeFi Trading System with Data Management
Integrates DataManager to prevent file explosion and Cursor freezing
"""

import os
import sys
import time
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import our data management system
from data_management_system import DataManager

class AlgorandDeFiTradingSystem:
    """Enhanced Algorand DeFi Trading System with Data Management"""
    
    def __init__(self):
        """Initialize trading system with data management"""
        print("🚀 Initializing Algorand DeFi Trading System with Data Management")
        
        # Initialize data manager to prevent file explosion
        self.data_manager = DataManager()
        print("✅ Data Manager initialized - No more file explosion!")
        
        # Load configuration
        self.config = self._load_config()
        
        # Trading state
        self.is_running = False
        self.active_positions = {}
        self.trade_history = []
        self.market_data_cache = {}
        
        # Performance tracking
        self.daily_pnl = 0.0
        self.total_trades = 0
        self.winning_trades = 0
        
        print("🎯 Trading system ready with automatic data management")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load trading configuration"""
        config_file = Path("algorand_defi_config.py")
        if config_file.exists():
            # Import the config class
            sys.path.append(str(Path.cwd()))
            try:
                from algorand_defi_config import AlgorandDeFiConfig
                config_instance = AlgorandDeFiConfig()
                return config_instance.get_config_dict()
            except ImportError as e:
                print(f"⚠️ Could not import config: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration if config file not found"""
        return {
            "network": "mainnet",
            "max_position_size_algo": 100.0,
            "max_daily_trades": 10,
            "risk_per_trade": 0.05,
            "enabled_strategies": ["momentum", "mean_reversion"],
            "market_data_interval": 300,  # 5 minutes, not every second!
            "price_update_frequency": 60   # 1 minute for price updates
        }
    
    async def start_trading(self):
        """Start the trading system with data management"""
        self.is_running = True
        print("🚀 Starting Algorand DeFi trading system...")
        print("✅ Data management active - preventing file explosion")
        
        try:
            while self.is_running:
                # Collect market data
                market_data = await self._collect_market_data()
                
                # ✅ USE DATAMANAGER INSTEAD OF CREATING INDIVIDUAL FILES
                # This prevents the 100,000+ file problem that was freezing Cursor
                self.data_manager.save_market_data(market_data, "current")
                
                # Update market data cache
                self.market_data_cache = market_data
                
                # Execute trading strategies
                await self._execute_trading_strategies()
                
                # Save daily snapshot at market close
                if self._is_market_close():
                    self.data_manager.save_market_data(market_data, "daily")
                    await self._generate_daily_report()
                
                # Wait before next iteration (configurable)
                await asyncio.sleep(self.config.get("market_data_interval", 300))
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping trading system...")
            await self.stop_trading()
        except Exception as e:
            print(f"❌ Error in trading loop: {e}")
            await self.stop_trading()
    
    async def stop_trading(self):
        """Stop the trading system"""
        self.is_running = False
        print("🛑 Trading system stopped")
        
        # Save final state
        final_data = {
            "timestamp": datetime.now().isoformat(),
            "final_state": {
                "active_positions": self.active_positions,
                "daily_pnl": self.daily_pnl,
                "total_trades": self.total_trades,
                "winning_trades": self.winning_trades
            }
        }
        
        self.data_manager.save_market_data(final_data, "daily")
        print("✅ Final state saved to data management system")
    
    async def _collect_market_data(self) -> Dict[str, Any]:
        """Collect market data (simulated for now)"""
        # Simulate collecting real market data
        current_time = datetime.now()
        
        market_data = {
            "timestamp": current_time.isoformat(),
            "network": self.config.get("network", "mainnet"),
            "assets": {
                "ALGO": {
                    "price_usd": 0.15 + (time.time() % 0.1),
                    "volume_24h": 1000000 + (time.time() % 500000),
                    "market_cap": 1000000000 + (time.time() % 100000000)
                },
                "USDC": {
                    "price_usd": 1.0,
                    "volume_24h": 5000000 + (time.time() % 2000000),
                    "market_cap": 50000000000 + (time.time() % 10000000)
                },
                "USDT": {
                    "price_usd": 1.0 + (time.time() % 0.02),
                    "volume_24h": 3000000 + (time.time() % 1500000),
                    "market_cap": 40000000000 + (time.time() % 8000000)
                }
            },
            "protocols": {
                "tinyman": {
                    "tvl": 5000000 + (time.time() % 1000000),
                    "volume_24h": 200000 + (time.time() % 100000),
                    "fees_24h": 1000 + (time.time() % 500)
                },
                "pact": {
                    "tvl": 3000000 + (time.time() % 800000),
                    "volume_24h": 150000 + (time.time() % 75000),
                    "fees_24h": 750 + (time.time() % 375)
                }
            },
            "trading_opportunities": self._identify_trading_opportunities(),
            "risk_metrics": self._calculate_risk_metrics()
        }
        
        return market_data
    
    def _identify_trading_opportunities(self) -> List[Dict[str, Any]]:
        """Identify potential trading opportunities"""
        opportunities = []
        
        # Simulate finding arbitrage opportunities
        if time.time() % 100 < 30:  # 30% chance of opportunity
            opportunities.append({
                "type": "arbitrage",
                "protocols": ["tinyman", "pact"],
                "asset_pair": "ALGO/USDC",
                "price_difference": 0.02 + (time.time() % 0.03),
                "estimated_profit": 5.0 + (time.time() % 10.0)
            })
        
        # Simulate momentum signals
        if time.time() % 100 < 40:  # 40% chance of momentum
            opportunities.append({
                "type": "momentum",
                "asset": "ALGO",
                "signal_strength": 0.7 + (time.time() % 0.3),
                "trend_direction": "up" if time.time() % 2 == 0 else "down"
            })
        
        return opportunities
    
    def _calculate_risk_metrics(self) -> Dict[str, Any]:
        """Calculate current risk metrics"""
        return {
            "portfolio_volatility": 0.15 + (time.time() % 0.1),
            "max_drawdown": 0.05 + (time.time() % 0.03),
            "var_95": 0.08 + (time.time() % 0.05),
            "correlation_matrix": {
                "ALGO_USDC": 0.3 + (time.time() % 0.4),
                "ALGO_USDT": 0.4 + (time.time() % 0.3),
                "USDC_USDT": 0.9 + (time.time() % 0.1)
            }
        }
    
    async def _execute_trading_strategies(self):
        """Execute trading strategies based on market data"""
        if not self.market_data_cache:
            return
        
        # Check if we should execute trades
        if self.total_trades >= self.config.get("max_daily_trades", 10):
            return
        
        # Execute momentum strategy
        if "momentum" in self.config.get("enabled_strategies", []):
            await self._execute_momentum_strategy()
        
        # Execute arbitrage strategy
        if "arbitrage" in self.config.get("enabled_strategies", []):
            await self._execute_arbitrage_strategy()
    
    async def _execute_momentum_strategy(self):
        """Execute momentum trading strategy"""
        # Simulate momentum trading logic
        if time.time() % 100 < 20:  # 20% chance of trade
            trade = {
                "id": f"momentum_{int(time.time())}",
                "strategy": "momentum",
                "asset": "ALGO",
                "action": "buy" if time.time() % 2 == 0 else "sell",
                "amount": 10.0 + (time.time() % 20.0),
                "timestamp": datetime.now().isoformat(),
                "estimated_price": 0.15 + (time.time() % 0.1)
            }
            
            self._record_trade(trade)
            print(f"📈 Momentum trade executed: {trade['action']} {trade['amount']} ALGO")
    
    async def _execute_arbitrage_strategy(self):
        """Execute arbitrage trading strategy"""
        # Simulate arbitrage trading logic
        if time.time() % 100 < 15:  # 15% chance of trade
            trade = {
                "id": f"arbitrage_{int(time.time())}",
                "strategy": "arbitrage",
                "protocols": ["tinyman", "pact"],
                "asset_pair": "ALGO/USDC",
                "action": "buy_low_sell_high",
                "amount": 5.0 + (time.time() % 10.0),
                "timestamp": datetime.now().isoformat(),
                "estimated_profit": 2.0 + (time.time() % 5.0)
            }
            
            self._record_trade(trade)
            print(f"🔄 Arbitrage trade executed: {trade['action']} for {trade['estimated_profit']:.2f} profit")
    
    def _record_trade(self, trade: Dict[str, Any]):
        """Record a trade in the system"""
        self.trade_history.append(trade)
        self.total_trades += 1
        
        # Simulate PnL calculation
        if trade.get("estimated_profit"):
            self.daily_pnl += trade["estimated_profit"]
            self.winning_trades += 1
        
        # Save trade to data management system
        trade_data = {
            "timestamp": datetime.now().isoformat(),
            "trade": trade,
            "system_state": {
                "total_trades": self.total_trades,
                "daily_pnl": self.daily_pnl,
                "winning_trades": self.winning_trades
            }
        }
        
        self.data_manager.save_market_data(trade_data, "current")
    
    def _is_market_close(self) -> bool:
        """Check if it's market close time"""
        now = datetime.now()
        return now.hour == 16 and now.minute == 0  # 4:00 PM
    
    async def _generate_daily_report(self):
        """Generate and save daily trading report"""
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "trading_summary": {
                "total_trades": self.total_trades,
                "winning_trades": self.winning_trades,
                "win_rate": self.winning_trades / max(self.total_trades, 1),
                "daily_pnl": self.daily_pnl,
                "active_positions": len(self.active_positions)
            },
            "market_data_summary": self.market_data_cache,
            "risk_metrics": self._calculate_risk_metrics()
        }
        
        # Save daily report using data manager
        self.data_manager.save_market_data(report, "daily")
        print(f"📊 Daily report generated and saved: {report['trading_summary']}")
        
        # Reset daily counters
        self.daily_pnl = 0.0
        self.total_trades = 0
        self.winning_trades = 0
    
    def get_current_data(self) -> Optional[Dict[str, Any]]:
        """Get current market data from data manager"""
        return self.data_manager.get_current_market_data()
    
    def get_historical_data(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get historical data from data manager"""
        return self.data_manager.get_historical_data(start_date, end_date)
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Get storage statistics from data manager"""
        return self.data_manager.get_storage_stats()
    
    def get_trading_summary(self) -> Dict[str, Any]:
        """Get current trading summary"""
        return {
            "is_running": self.is_running,
            "active_positions": len(self.active_positions),
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "daily_pnl": self.daily_pnl,
            "win_rate": self.winning_trades / max(self.total_trades, 1) if self.total_trades > 0 else 0
        }

async def main():
    """Main function to run the enhanced trading system"""
    print("=== 🚀 Enhanced Algorand DeFi Trading System with Data Management ===")
    print("✅ Prevents file explosion and Cursor freezing")
    print("✅ Automatic data management and cleanup")
    print("✅ Organized storage with compression")
    
    # Initialize trading system
    trading_system = AlgorandDeFiTradingSystem()
    
    # Show current storage status
    print("\n📊 Current Storage Status:")
    stats = trading_system.get_storage_info()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show trading summary
    print("\n📈 Trading Summary:")
    summary = trading_system.get_trading_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Start trading system
    print("\n🚀 Starting enhanced trading system...")
    print("Press Ctrl+C to stop")
    print("✅ Data management is active - preventing file explosion!")
    
    try:
        await trading_system.start_trading()
    except KeyboardInterrupt:
        print("\n🛑 Stopping enhanced trading system...")
        await trading_system.stop_trading()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
