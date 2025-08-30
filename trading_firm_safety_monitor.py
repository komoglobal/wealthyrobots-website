#!/usr/bin/env python3
"""
TRADING FIRM SAFETY MONITOR
Continuous monitoring and emergency stop system for portfolio protection
"""

import json
import os
import time
import datetime
import subprocess
import signal
import sys
from typing import Dict, Any

class TradingFirmSafetyMonitor:
    def __init__(self):
        print("🛡️ TRADING FIRM SAFETY MONITOR - INITIALIZING...")
        print("🎯 Portfolio Protection: $1000 Safety Threshold")
        
        # Safety parameters
        self.safety_threshold = 1000.0  # Stop if NAV goes under $1000
        self.check_interval = 10  # Check every 10 seconds
        self.emergency_stop_triggered = False
        self.emergency_shutdown_initiated = False
        
        # Portfolio monitoring
        self.nav_log_file = "logs/fund_nav.jsonl"
        self.firm_dashboard_file = "current_firm_dashboard.json"
        self.safety_log_file = "safety_monitor_log.jsonl"
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("✅ Safety Monitor initialized")
        print(f"🛡️ Safety Threshold: ${self.safety_threshold:,.2f}")
        print(f"⏱️ Check Interval: {self.check_interval} seconds")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}, shutting down safety monitor...")
        sys.exit(0)
    
    def get_current_nav(self) -> float:
        """Get the latest NAV value."""
        try:
            if os.path.exists(self.nav_log_file):
                with open(self.nav_log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        data = json.loads(last_line)
                        return float(data.get('nav_usd', 0))
        except Exception as e:
            print(f"❌ Error reading NAV: {e}")
        return 0.0
    
    def get_hot_wallet_value(self) -> float:
        """Get current hot wallet total value in USD."""
        try:
            from algofund.wallets import load_hot_wallet_address, fetch_account_balances
            from algofund.pricing import fetch_algorand_usd_price
            
            addr = load_hot_wallet_address()
            if not addr:
                return 0.0
                
            balances = fetch_account_balances(addr)
            if not balances:
                return 0.0
            
            # Get ALGO price (fallback to recent known price if API fails)
            algo_price = fetch_algorand_usd_price() or 0.15
            
            total_usd = 0.0
            
            # ALGO balance
            if 'ALGO' in balances:
                total_usd += float(balances['ALGO']) * algo_price
            
            # USDT balance (6 decimals)
            if 'ASA_312769' in balances:
                total_usd += float(balances['ASA_312769']) / 1_000_000.0
            
            return total_usd
            
        except Exception as e:
            print(f"❌ Error getting hot wallet value: {e}")
            return 0.0
    
    def emergency_shutdown(self):
        """Emergency shutdown of all trading firm systems."""
        if self.emergency_shutdown_initiated:
            return
            
        self.emergency_shutdown_initiated = True
        print("🚨 EMERGENCY SHUTDOWN INITIATED!")
        print("🛑 Stopping all trading firm systems...")
        
        try:
            # Stop all Python trading processes
            print("🛑 Stopping trading firm processes...")
            subprocess.run(['pkill', '-f', 'trading_firm'], timeout=10)
            subprocess.run(['pkill', '-f', 'enhanced_'], timeout=10)
            subprocess.run(['pkill', '-f', 'comprehensive_'], timeout=10)
            subprocess.run(['pkill', '-f', 'live_pnl_dashboard'], timeout=10)
            
            # Update firm status to emergency stop
            self.update_emergency_status()
            
            print("✅ All trading firm systems stopped")
            print("🚨 TRADING FIRM EMERGENCY STOPPED - Portfolio below safety threshold")
            
            # Log the emergency stop
            self.log_safety_event("EMERGENCY_STOP", f"Portfolio NAV below ${self.safety_threshold:,.2f}")
            
        except Exception as e:
            print(f"❌ Error during emergency shutdown: {e}")
    
    def update_emergency_status(self):
        """Update firm dashboard with emergency stop status."""
        try:
            emergency_status = {
                "timestamp": datetime.datetime.now().isoformat(),
                "firm_status": "emergency_stopped",
                "emergency_reason": f"Portfolio below safety threshold (${self.safety_threshold:,.2f})",
                "last_nav": self.get_current_nav(),
                "hot_wallet_value": self.get_hot_wallet_value(),
                "safety_threshold": self.safety_threshold,
                "stop_time": time.time(),
                "safety_monitor": "active"
            }
            
            # Update current firm dashboard
            with open(self.firm_dashboard_file, "w") as f:
                json.dump(emergency_status, f, indent=2)
            
            # Create emergency stop log
            with open("emergency_stop_log.jsonl", "a") as f:
                f.write(json.dumps(emergency_status) + "\n")
                
        except Exception as e:
            print(f"❌ Error updating emergency status: {e}")
    
    def log_safety_event(self, event_type: str, description: str):
        """Log safety monitoring events."""
        try:
            log_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "event_type": event_type,
                "description": description,
                "nav": self.get_current_nav(),
                "hot_wallet": self.get_hot_wallet_value(),
                "safety_threshold": self.safety_threshold
            }
            
            with open(self.safety_log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
                
        except Exception as e:
            print(f"❌ Error logging safety event: {e}")
    
    def check_portfolio_safety(self) -> bool:
        """Check if portfolio is above safety threshold."""
        current_nav = self.get_current_nav()
        hot_wallet = self.get_hot_wallet_value()
        
        # Use the higher of NAV or hot wallet value
        portfolio_value = max(current_nav, hot_wallet)
        
        # Log current status
        status_msg = f"Portfolio: ${portfolio_value:,.2f} | Threshold: ${self.safety_threshold:,.2f}"
        if portfolio_value < self.safety_threshold:
            print(f"🚨 {status_msg} | ❌ BELOW THRESHOLD!")
            return False
        else:
            print(f"✅ {status_msg} | ✅ SAFE")
            return True
    
    def run_safety_monitor(self):
        """Run the continuous safety monitoring system."""
        print("🚀 STARTING SAFETY MONITORING...")
        print("=" * 60)
        
        cycle = 0
        
        while not self.emergency_stop_triggered:
            cycle += 1
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            print(f"\n📊 SAFETY CHECK #{cycle} | {current_time}")
            print("-" * 40)
            
            # Check portfolio safety
            if not self.check_portfolio_safety():
                print("🚨 SAFETY THRESHOLD BREACHED!")
                print("🛑 Initiating emergency shutdown...")
                self.emergency_stop_triggered = True
                self.emergency_shutdown()
                break
            
            # Log successful check
            self.log_safety_event("SAFETY_CHECK", f"Portfolio above threshold - Cycle #{cycle}")
            
            # Wait for next check
            print(f"⏳ Next safety check in {self.check_interval} seconds...")
            time.sleep(self.check_interval)
        
        print("🛑 Safety monitoring stopped")

def main():
    """Main safety monitor function."""
    monitor = TradingFirmSafetyMonitor()
    monitor.run_safety_monitor()

if __name__ == "__main__":
    main()
