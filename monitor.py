#!/usr/bin/env python3
"""
Multi-Protocol Trading System Monitor
Real-time monitoring dashboard for the trading system
"""

import os
import json
import time
import curses
from datetime import datetime
from multi_protocol_trading_system import MultiProtocolTradingSystem

class TradingSystemMonitor:
    def __init__(self):
        self.trading_system = MultiProtocolTradingSystem()
        self.screen = None
        self.running = True
        
    def init_screen(self):
        """Initialize the curses screen"""
        self.screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        
        # Define color pairs
        curses.init_pair(1, curses.COLOR_GREEN, -1)    # Success
        curses.init_pair(2, curses.COLOR_RED, -1)      # Error
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # Warning
        curses.init_pair(4, curses.COLOR_BLUE, -1)     # Info
        curses.init_pair(5, curses.COLOR_CYAN, -1)     # Highlight
        
    def cleanup_screen(self):
        """Clean up the curses screen"""
        if self.screen:
            curses.nocbreak()
            self.screen.keypad(False)
            curses.echo()
            curses.endwin()
    
    def draw_header(self):
        """Draw the header section"""
        height, width = self.screen.getmaxyx()
        
        # Title
        title = "🚀 MULTI-PROTOCOL TRADING SYSTEM MONITOR"
        self.screen.addstr(0, (width - len(title)) // 2, title, curses.color_pair(5))
        
        # Timestamp
        timestamp = f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.screen.addstr(1, width - len(timestamp) - 2, timestamp, curses.color_pair(4))
        
        # Separator
        self.screen.addstr(2, 0, "=" * width, curses.color_pair(4))
    
    def draw_system_status(self):
        """Draw system status section"""
        height, width = self.screen.getmaxyx()
        
        # Section header
        self.screen.addstr(4, 0, "🏥 SYSTEM STATUS", curses.color_pair(5))
        
        try:
            health = self.trading_system.monitor_system_health()
            
            # Overall status
            status_color = curses.color_pair(1) if health['status'] == 'healthy' else curses.color_pair(2)
            self.screen.addstr(5, 2, f"Overall Status: {health['status'].upper()}", status_color)
            
            # Protocol status
            self.screen.addstr(6, 2, "Protocols:", curses.color_pair(4))
            y_pos = 7
            for protocol, status in health['protocols'].items():
                color = curses.color_pair(1) if status['connected'] else curses.color_pair(2)
                self.screen.addstr(y_pos, 4, f"{protocol.upper()}: {'✅' if status['connected'] else '❌'}", color)
                y_pos += 1
            
            # API endpoints
            self.screen.addstr(y_pos, 2, "API Endpoints:", curses.color_pair(4))
            y_pos += 1
            for endpoint_type, data in health['api_endpoints'].items():
                self.screen.addstr(y_pos, 4, f"{endpoint_type}: {data['healthy']}/{data['total']} healthy", 
                                 curses.color_pair(1) if data['healthy'] == data['total'] else curses.color_pair(3))
                y_pos += 1
                
        except Exception as e:
            self.screen.addstr(5, 2, f"Error getting system status: {e}", curses.color_pair(2))
    
    def draw_opportunities(self):
        """Draw opportunities section"""
        height, width = self.screen.getmaxyx()
        
        # Section header
        self.screen.addstr(4, width // 2, "🔍 OPPORTUNITIES", curses.color_pair(5))
        
        try:
            # Scan for opportunities
            opportunities = self.trading_system.scan_all_opportunities()
            total_opps = sum(len(opps) for opps in opportunities.values())
            
            self.screen.addstr(5, width // 2 + 2, f"Total Found: {total_opps}", curses.color_pair(4))
            
            # Get best opportunities
            best_opps = self.trading_system.find_best_opportunities(opportunities, limit=3)
            
            y_pos = 6
            for i, opp in enumerate(best_opps):
                if y_pos >= height - 5:  # Leave space for footer
                    break
                    
                # Opportunity info
                opp_text = f"{i+1}. {opp['protocol'].upper()}: {opp['opportunity_type']}"
                self.screen.addstr(y_pos, width // 2 + 2, opp_text, curses.color_pair(4))
                y_pos += 1
                
                # Score and APY
                score_text = f"   Score: {opp['_score']:.1f} | APY: {opp['estimated_apy']}%"
                self.screen.addstr(y_pos, width // 2 + 2, score_text, curses.color_pair(1))
                y_pos += 1
                
        except Exception as e:
            self.screen.addstr(5, width // 2 + 2, f"Error: {e}", curses.color_pair(2))
    
    def draw_performance(self):
        """Draw performance metrics section"""
        height, width = self.screen.getmaxyx()
        
        # Section header
        self.screen.addstr(height // 2, 0, "📊 PERFORMANCE METRICS", curses.color_pair(5))
        
        try:
            # Wallet balance
            balance = self.trading_system.get_wallet_balance()
            balance_text = f"Wallet Balance: {balance:.6f} ALGO" if balance else "Wallet Balance: Unknown"
            self.screen.addstr(height // 2 + 1, 2, balance_text, curses.color_pair(4))
            
            # Last trade time
            last_trade = getattr(self.trading_system, '_last_trade_time', 'Never')
            last_trade_text = f"Last Trade: {last_trade}"
            self.screen.addstr(height // 2 + 2, 2, last_trade_text, curses.color_pair(4))
            
            # Configuration info
            env = self.trading_system.config.get('environment', 'development')
            env_text = f"Environment: {env.upper()}"
            self.screen.addstr(height // 2 + 3, 2, env_text, curses.color_pair(4))
            
        except Exception as e:
            self.screen.addstr(height // 2 + 1, 2, f"Error: {e}", curses.color_pair(2))
    
    def draw_footer(self):
        """Draw the footer section"""
        height, width = self.screen.getmaxyx()
        
        # Separator
        self.screen.addstr(height - 3, 0, "=" * width, curses.color_pair(4))
        
        # Instructions
        instructions = "Press 'q' to quit, 'r' to refresh, 's' to scan opportunities"
        self.screen.addstr(height - 2, (width - len(instructions)) // 2, instructions, curses.color_pair(3))
        
        # Status
        status = "Monitoring Active" if self.running else "Stopping..."
        self.screen.addstr(height - 1, (width - len(status)) // 2, status, curses.color_pair(1))
    
    def handle_input(self):
        """Handle user input"""
        self.screen.nodelay(True)
        
        try:
            key = self.screen.getch()
            if key == ord('q'):
                self.running = False
            elif key == ord('r'):
                self.refresh_display()
            elif key == ord('s'):
                self.scan_opportunities()
        except curses.error:
            pass  # No input available
    
    def refresh_display(self):
        """Refresh the display"""
        self.screen.clear()
        self.draw_header()
        self.draw_system_status()
        self.draw_opportunities()
        self.draw_performance()
        self.draw_footer()
        self.screen.refresh()
    
    def scan_opportunities(self):
        """Manually trigger opportunity scan"""
        try:
            self.trading_system._automated_opportunity_scan()
        except Exception as e:
            pass  # Don't crash the monitor
    
    def run(self):
        """Main monitoring loop"""
        try:
            self.init_screen()
            
            while self.running:
                self.refresh_display()
                self.handle_input()
                time.sleep(2)  # Update every 2 seconds
                
        except KeyboardInterrupt:
            self.running = False
        finally:
            self.cleanup_screen()

def main():
    """Start the monitoring dashboard"""
    monitor = TradingSystemMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
