#!/usr/bin/env python3
"""
WealthyRobot Optimized Autonomous Trading Fund
Designed to integrate seamlessly with existing optimization systems
"""

import time
import logging
import yaml
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import schedule
import threading

# Import our trading system
from multi_protocol_trading_system import MultiProtocolTradingSystem

class OptimizedAutonomousTradingFund:
    def __init__(self):
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self.trading_system = None
        self.running = False
        self.last_scan = None
        self.last_health_check = None
        self.scan_count = 0
        
        # Performance tracking
        self.start_time = datetime.now()
        self.total_opportunities = 0
        self.successful_trades = 0
        
        print("🚀 WealthyRobot Optimized Autonomous Trading Fund")
        print("🔧 Designed for seamless system integration")
        
    def _load_config(self) -> Dict:
        """Load optimized configuration"""
        config_path = "config/optimized_integration.yaml"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Fallback configuration
            return {
                "performance": {
                    "scan_interval": 300,
                    "health_check_interval": 600,
                    "quiet_mode": True
                },
                "logging": {
                    "level": "INFO",
                    "quiet_mode": True
                }
            }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup optimized logging"""
        logger = logging.getLogger("OptimizedFund")
        logger.setLevel(logging.INFO)
        
        # Only log to systemd journal (no file spam)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def initialize_trading_system(self):
        """Initialize the trading system with error handling"""
        try:
            self.trading_system = MultiProtocolTradingSystem()
            self.logger.info("✅ Trading system initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize trading system: {e}")
            return False
    
    def scan_opportunities(self):
        """Scan for trading opportunities (optimized)"""
        if not self.trading_system:
            self.logger.warning("⚠️ Trading system not initialized, skipping scan")
            return
        
        try:
            self.scan_count += 1
            self.last_scan = datetime.now()
            
            # Only log every 10th scan to reduce spam
            if self.scan_count % 10 == 0:
                self.logger.info(f"🔍 Scan #{self.scan_count} - Checking for opportunities...")
            
            opportunities = self.trading_system.scan_all_opportunities()
            
            if opportunities and any(opportunities.values()):
                total_opps = sum(len(opps) for opps in opportunities.values() if opps)
                self.total_opportunities += total_opps
                
                if self.scan_count % 10 == 0:  # Reduce log spam
                    self.logger.info(f"📊 Found {total_opps} opportunities (Total: {self.total_opportunities})")
                
                # Auto-execute best opportunities (with risk management)
                self._execute_best_opportunities(opportunities)
            else:
                if self.scan_count % 20 == 0:  # Very quiet logging
                    self.logger.info("🔍 No opportunities found in this scan")
                    
        except Exception as e:
            self.logger.error(f"❌ Error during opportunity scan: {e}")
    
    def _execute_best_opportunities(self, opportunities: Dict):
        """Execute best opportunities with risk management"""
        try:
            best_opps = self.trading_system.find_best_opportunities(opportunities)
            if best_opps:
                for opp in best_opps[:2]:  # Limit to top 2 opportunities
                    if self.trading_system.check_risk_limits(opp):
                        success = self.trading_system.execute_best_opportunity(opp)
                        if success:
                            self.successful_trades += 1
                            self.logger.info(f"✅ Executed trade: {opp.get('protocol', 'Unknown')}")
        except Exception as e:
            self.logger.error(f"❌ Error executing opportunities: {e}")
    
    def health_check(self):
        """Perform system health check (optimized)"""
        if not self.trading_system:
            return
        
        try:
            self.last_health_check = datetime.now()
            health = self.trading_system.monitor_system_health()
            
            # Only log critical issues to reduce spam
            if health.get('status') == 'critical':
                self.logger.critical(f"🚨 CRITICAL: {health.get('message', 'Unknown issue')}")
            elif health.get('status') == 'warning' and self.scan_count % 50 == 0:
                self.logger.warning(f"⚠️ Warning: {health.get('message', 'Unknown issue')}")
                
        except Exception as e:
            self.logger.error(f"❌ Health check failed: {e}")
    
    def generate_performance_summary(self):
        """Generate performance summary (minimal logging)"""
        if self.scan_count % 100 == 0:  # Very infrequent logging
            runtime = datetime.now() - self.start_time
            scan_rate = self.scan_count / (runtime.total_seconds() / 3600)  # scans per hour
            
            self.logger.info(f"📊 Performance Summary: {self.scan_count} scans, "
                           f"{self.total_opportunities} opportunities, "
                           f"{self.successful_trades} trades, "
                           f"{scan_rate:.1f} scans/hour")
    
    def run_autonomous_loop(self):
        """Main autonomous control loop"""
        self.running = True
        
        # Schedule tasks
        scan_interval = self.config.get("performance", {}).get("scan_interval", 300)
        health_interval = self.config.get("performance", {}).get("health_check_interval", 600)
        
        schedule.every(scan_interval).seconds.do(self.scan_opportunities)
        schedule.every(health_interval).seconds.do(self.health_check)
        schedule.every(3600).seconds.do(self.generate_performance_summary)  # Hourly
        
        self.logger.info(f"🔄 Autonomous loop started - Scan: {scan_interval}s, Health: {health_interval}s")
        
        # Initial scan
        self.scan_opportunities()
        
        # Main loop
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("🛑 Shutdown requested")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in autonomous loop: {e}")
                time.sleep(5)  # Wait before retrying
        
        self.logger.info("🔄 Autonomous loop stopped")
    
    def start(self):
        """Start the optimized autonomous fund"""
        if self.initialize_trading_system():
            self.logger.info("🚀 Starting optimized autonomous trading fund...")
            self.run_autonomous_loop()
        else:
            self.logger.error("❌ Failed to start - trading system initialization failed")

def main():
    """Main entry point"""
    fund = OptimizedAutonomousTradingFund()
    fund.start()

if __name__ == "__main__":
    main()



