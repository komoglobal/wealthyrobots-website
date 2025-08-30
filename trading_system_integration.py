#!/usr/bin/env python3
"""
Example integration of Data Management System with Trading System
This shows how to prevent the file explosion that was causing Cursor to freeze
"""

import time
import json
from datetime import datetime
from data_management_system import DataManager

class TradingSystem:
    def __init__(self):
        """Initialize trading system with data management"""
        self.data_manager = DataManager()
        self.is_running = False
        
        print("Trading System initialized with Data Management")
        print("✅ No more file explosion!")
        print("✅ Automatic cleanup enabled")
        print("✅ Compressed storage")
    
    def start_trading(self):
        """Start the trading system"""
        self.is_running = True
        print("🚀 Trading system started")
        
        try:
            while self.is_running:
                # Simulate market data collection
                market_data = self._collect_market_data()
                
                # ✅ USE THIS INSTEAD OF CREATING INDIVIDUAL FILES
                # This prevents the 100,000+ file problem
                self.data_manager.save_market_data(market_data, "current")
                
                # Optional: Save daily snapshot at market close
                if self._is_market_close():
                    self.data_manager.save_market_data(market_data, "daily")
                
                # Wait before next collection (configurable)
                time.sleep(300)  # 5 minutes instead of every second
                
        except KeyboardInterrupt:
            print("\n🛑 Trading system stopped")
            self.stop_trading()
    
    def stop_trading(self):
        """Stop the trading system"""
        self.is_running = False
        print("Trading system stopped")
    
    def _collect_market_data(self):
        """Simulate collecting market data"""
        return {
            "timestamp": datetime.now().isoformat(),
            "symbols": ["AAPL", "GOOGL", "MSFT"],
            "prices": {
                "AAPL": 150.25 + (time.time() % 10),
                "GOOGL": 2800.50 + (time.time() % 20),
                "MSFT": 320.75 + (time.time() % 15)
            },
            "volume": int(time.time() % 1000000),
            "market_status": "open"
        }
    
    def _is_market_close(self):
        """Check if it's market close time"""
        now = datetime.now()
        return now.hour == 16 and now.minute == 0  # 4:00 PM
    
    def get_current_data(self):
        """Get current market data"""
        return self.data_manager.get_current_market_data()
    
    def get_historical_data(self, start_date, end_date):
        """Get historical market data"""
        return self.data_manager.get_historical_data(start_date, end_date)
    
    def get_storage_info(self):
        """Get storage statistics"""
        return self.data_manager.get_storage_stats()

def main():
    """Example usage"""
    print("=== WealthyRobot Trading System with Data Management ===")
    
    # Initialize trading system
    trading_system = TradingSystem()
    
    # Show current storage status
    print("\n📊 Current Storage Status:")
    stats = trading_system.get_storage_info()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Start trading (this will run continuously)
    print("\n🚀 Starting trading system...")
    print("Press Ctrl+C to stop")
    
    try:
        trading_system.start_trading()
    except KeyboardInterrupt:
        print("\n🛑 Stopping trading system...")
        trading_system.stop_trading()

if __name__ == "__main__":
    main()
