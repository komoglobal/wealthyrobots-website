#!/usr/bin/env python3
"""
ALGORAND PNL TRACKING AND VERIFICATION SYSTEM
Real-time portfolio performance tracking for Algorand-based trading firm
"""

import asyncio
import json
import time
import subprocess
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('algorand_pnl_tracking.log'),
        logging.StreamHandler()
    ]
)

class AlgorandPnLTrackingSystem:
    def __init__(self):
        print("🎯 ALGORAND PNL TRACKING SYSTEM - INITIALIZING...")
        print("🔗 Integrating with algofund services for real-time data")
        
        # System configuration
        self.config = {
            'log_paths': {
                'paper_trading': 'logs/algofund-paper.out',
                'live_trading': 'logs/algofund-live.out',
                'fund_manager': 'logs/algofund-live.out'
            },
            'update_frequency': 30,  # seconds
            'nav_history_length': 1000,
            'performance_metrics': ['nav', 'wallet', 'opps_scanned', 'LIVE_EXECUTE_TXNS']
        }
        
        # Portfolio tracking state
        self.portfolio_state = {
            'current_nav': 0.0,
            'paper_nav': 0.0,
            'live_nav': 0.0,
            'hot_wallet_algo': 0.0,
            'total_positions': 0,
            'active_trades': 0,
            'last_update': None,
            'nav_history': [],
            'pnl_metrics': {
                'daily_pnl': 0.0,
                'weekly_pnl': 0.0,
                'monthly_pnl': 0.0,
                'total_pnl': 0.0
            }
        }
        
        # Trading activity tracking
        self.trading_activity = {
            'total_transactions': 0,
            'total_volume_microalgo': 0,
            'dex_activity': {
                'pact': {'swaps': 0, 'volume': 0},
                'tinyman': {'swaps': 0, 'volume': 0}
            },
            'last_trade_time': None
        }
        
        # Performance verification
        self.verification_status = {
            'real_data_verified': False,
            'last_verification': None,
            'data_source': 'algofund_logs',
            'verification_method': 'log_parsing'
        }
        
        print("✅ Algorand PnL Tracking System initialized")
    
    async def start_monitoring(self):
        """Start continuous monitoring of Algorand portfolio"""
        print("🚀 Starting Algorand portfolio monitoring...")
        
        try:
            while True:
                await self.update_portfolio_status()
                await self.verify_real_data()
                await self.calculate_pnl_metrics()
                await self.generate_performance_report()
                
                print(f"📊 Portfolio Updated: NAV=${self.portfolio_state['current_nav']:.2f}, "
                      f"Daily PnL=${self.portfolio_state['pnl_metrics']['daily_pnl']:.2f}")
                
                await asyncio.sleep(self.config['update_frequency'])
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            logging.error(f"Error in monitoring loop: {e}")
            raise
    
    async def update_portfolio_status(self):
        """Update portfolio status from algofund logs"""
        try:
            # Parse paper trading logs
            paper_data = await self.parse_algofund_logs('paper_trading')
            if paper_data:
                self.portfolio_state['paper_nav'] = paper_data.get('nav', 0.0)
                self.portfolio_state['current_nav'] = paper_data.get('nav', 0.0)
            
            # Parse live trading logs
            live_data = await self.parse_algofund_logs('live_trading')
            if live_data:
                self.portfolio_state['live_nav'] = live_data.get('nav', 0.0)
                if live_data.get('nav'):
                    self.portfolio_state['current_nav'] = live_data.get('nav')
                
                # Update wallet information
                if live_data.get('wallet'):
                    self.portfolio_state['hot_wallet_algo'] = live_data['wallet'].get('algo', 0.0)
                
                # Update trading activity
                await self.update_trading_activity(live_data)
            
            # Update timestamp
            self.portfolio_state['last_update'] = datetime.now()
            
            # Store NAV history
            if self.portfolio_state['current_nav'] > 0:
                self.portfolio_state['nav_history'].append({
                    'timestamp': datetime.now().isoformat(),
                    'nav': self.portfolio_state['current_nav'],
                    'source': 'paper' if self.portfolio_state['current_nav'] == self.portfolio_state['paper_nav'] else 'live'
                })
                
                # Keep only recent history
                if len(self.portfolio_state['nav_history']) > self.config['nav_history_length']:
                    self.portfolio_state['nav_history'] = self.portfolio_state['nav_history'][-self.config['nav_history_length']:]
            
        except Exception as e:
            logging.error(f"Error updating portfolio status: {e}")
    
    async def parse_algofund_logs(self, log_type: str) -> Dict:
        """Parse algofund log files for portfolio data"""
        try:
            log_path = self.config['log_paths'].get(log_type)
            if not log_path or not os.path.exists(log_path):
                return {}
            
            # Read last 50 lines of log file
            result = subprocess.run(
                ['tail', '-50', log_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {}
            
            log_lines = result.stdout.split('\n')
            parsed_data = {}
            
            for line in log_lines:
                if not line.strip():
                    continue
                
                try:
                    # Parse JSON metrics
                    if line.startswith('{') and line.endswith('}'):
                        data = json.loads(line)
                        metric = data.get('metric')
                        
                        if metric == 'nav':
                            parsed_data['nav'] = data.get('usd', 0.0)
                        elif metric == 'wallet':
                            parsed_data['wallet'] = {
                                'kind': data.get('kind', 'unknown'),
                                'address': data.get('address', ''),
                                'algo': data.get('algo', 0.0)
                            }
                        elif metric == 'opps_scanned':
                            parsed_data['opps_scanned'] = {
                                'total': data.get('total', 0),
                                'allowed': data.get('allowed', 0)
                            }
                    
                    # Parse transaction summaries
                    elif 'LIVE_EXECUTE_TXNS:' in line:
                        await self.parse_transaction_summary(line)
                        
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    logging.debug(f"Error parsing log line: {e}")
                    continue
            
            return parsed_data
            
        except Exception as e:
            logging.error(f"Error parsing {log_type} logs: {e}")
            return {}
    
    async def parse_transaction_summary(self, line: str):
        """Parse transaction summary lines from logs"""
        try:
            if 'Tinyman swap' in line:
                self.trading_activity['dex_activity']['tinyman']['swaps'] += 1
                # Extract volume from line
                if 'size_microalgo=' in line:
                    volume = int(line.split('size_microalgo=')[1].split()[0])
                    self.trading_activity['dex_activity']['tinyman']['volume'] += volume
                    self.trading_activity['total_volume_microalgo'] += volume
            
            elif 'Pact swap' in line:
                self.trading_activity['dex_activity']['pact']['swaps'] += 1
                # Extract volume from line
                if 'size_microalgo=' in line:
                    volume = int(line.split('size_microalgo=')[1].split()[0])
                    self.trading_activity['dex_activity']['pact']['volume'] += volume
                    self.trading_activity['total_volume_microalgo'] += volume
            
            self.trading_activity['total_transactions'] += 1
            self.trading_activity['last_trade_time'] = datetime.now()
            
        except Exception as e:
            logging.error(f"Error parsing transaction summary: {e}")
    
    async def update_trading_activity(self, live_data: Dict):
        """Update trading activity metrics"""
        try:
            # Update opportunities scanned
            if live_data.get('opps_scanned'):
                self.portfolio_state['total_positions'] = live_data['opps_scanned'].get('total', 0)
                self.portfolio_state['active_trades'] = live_data['opps_scanned'].get('allowed', 0)
            
        except Exception as e:
            logging.error(f"Error updating trading activity: {e}")
    
    async def calculate_pnl_metrics(self):
        """Calculate PnL metrics from NAV history"""
        try:
            if len(self.portfolio_state['nav_history']) < 2:
                return
            
            current_nav = self.portfolio_state['current_nav']
            nav_history = self.portfolio_state['nav_history']
            
            # Calculate daily PnL
            today = datetime.now().date()
            yesterday_nav = None
            
            for entry in reversed(nav_history):
                entry_date = datetime.fromisoformat(entry['timestamp']).date()
                if entry_date == today - timedelta(days=1):
                    yesterday_nav = entry['nav']
                    break
            
            if yesterday_nav:
                self.portfolio_state['pnl_metrics']['daily_pnl'] = current_nav - yesterday_nav
            
            # Calculate weekly PnL
            week_ago = today - timedelta(days=7)
            week_ago_nav = None
            
            for entry in reversed(nav_history):
                entry_date = datetime.fromisoformat(entry['timestamp']).date()
                if entry_date <= week_ago:
                    week_ago_nav = entry['nav']
                    break
            
            if week_ago_nav:
                self.portfolio_state['pnl_metrics']['weekly_pnl'] = current_nav - week_ago_nav
            
            # Calculate monthly PnL
            month_ago = today - timedelta(days=30)
            month_ago_nav = None
            
            for entry in reversed(nav_history):
                entry_date = datetime.fromisoformat(entry['timestamp']).date()
                if entry_date <= month_ago:
                    month_ago_nav = entry['nav']
                    break
            
            if month_ago_nav:
                self.portfolio_state['pnl_metrics']['monthly_pnl'] = current_nav - month_ago_nav
            
            # Calculate total PnL (assuming starting NAV of $1000)
            starting_nav = 1000.0
            self.portfolio_state['pnl_metrics']['total_pnl'] = current_nav - starting_nav
            
        except Exception as e:
            logging.error(f"Error calculating PnL metrics: {e}")
    
    async def verify_real_data(self):
        """Verify that real data is being used vs simulated data"""
        try:
            # Check if algofund services are actually running
            services_running = await self.check_algofund_services()
            
            # Check if log files are being updated
            logs_active = await self.check_log_activity()
            
            # Check if NAV values are realistic (not hardcoded)
            nav_realistic = await self.check_nav_realism()
            
            # Update verification status
            self.verification_status['real_data_verified'] = (
                services_running and logs_active and nav_realistic
            )
            self.verification_status['last_verification'] = datetime.now()
            
            if self.verification_status['real_data_verified']:
                logging.info("✅ Real data verification passed")
            else:
                logging.warning("⚠️ Real data verification failed")
            
        except Exception as e:
            logging.error(f"Error in real data verification: {e}")
    
    async def check_algofund_services(self) -> bool:
        """Check if algofund services are running"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'algofund'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.returncode == 0 and len(result.stdout.strip().split('\n')) > 0
            
        except Exception as e:
            logging.error(f"Error checking algofund services: {e}")
            return False
    
    async def check_log_activity(self) -> bool:
        """Check if log files are being actively updated"""
        try:
            for log_type, log_path in self.config['log_paths'].items():
                if not os.path.exists(log_path):
                    continue
                
                # Check if log file was modified in last 5 minutes
                stat = os.stat(log_path)
                if time.time() - stat.st_mtime > 300:  # 5 minutes
                    logging.warning(f"Log file {log_type} not recently updated")
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Error checking log activity: {e}")
            return False
    
    async def check_nav_realism(self) -> bool:
        """Check if NAV values are realistic (not hardcoded)"""
        try:
            if len(self.portfolio_state['nav_history']) < 3:
                return False
            
            # Check for variation in NAV (real data should vary)
            recent_navs = [entry['nav'] for entry in self.portfolio_state['nav_history'][-3:]]
            
            # Calculate coefficient of variation
            mean_nav = sum(recent_navs) / len(recent_navs)
            if mean_nav == 0:
                return False
            
            variance = sum((nav - mean_nav) ** 2 for nav in recent_navs) / len(recent_navs)
            std_dev = variance ** 0.5
            cv = std_dev / mean_nav
            
            # If CV is too low, might be hardcoded
            return cv > 0.001  # 0.1% minimum variation
            
        except Exception as e:
            logging.error(f"Error checking NAV realism: {e}")
            return False
    
    async def generate_performance_report(self):
        """Generate comprehensive performance report"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'portfolio_summary': {
                    'current_nav': self.portfolio_state['current_nav'],
                    'paper_nav': self.portfolio_state['paper_nav'],
                    'live_nav': self.portfolio_state['live_nav'],
                    'hot_wallet_algo': self.portfolio_state['hot_wallet_algo'],
                    'total_positions': self.portfolio_state['total_positions'],
                    'active_trades': self.portfolio_state['active_trades']
                },
                'pnl_metrics': self.portfolio_state['pnl_metrics'],
                'trading_activity': self.trading_activity,
                'verification_status': self.verification_status,
                'nav_history_summary': {
                    'total_entries': len(self.portfolio_state['nav_history']),
                    'latest_nav': self.portfolio_state['nav_history'][-1] if self.portfolio_state['nav_history'] else None,
                    'nav_range': {
                        'min': min([entry['nav'] for entry in self.portfolio_state['nav_history']]) if self.portfolio_state['nav_history'] else 0,
                        'max': max([entry['nav'] for entry in self.portfolio_state['nav_history']]) if self.portfolio_state['nav_history'] else 0
                    }
                }
            }
            
            # Save report
            with open('algorand_performance_report.json', 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            # Update current performance dashboard
            with open('current_performance_dashboard.json', 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logging.info("📊 Performance report generated successfully")
            
        except Exception as e:
            logging.error(f"Error generating performance report: {e}")
    
    def get_current_status(self) -> Dict:
        """Get current system status"""
        return {
            'system_status': 'active',
            'last_update': self.portfolio_state['last_update'],
            'portfolio_state': self.portfolio_state,
            'verification_status': self.verification_status
        }

async def main():
    """Main function to run the Algorand PnL tracking system"""
    print("🚀 Starting Algorand PnL Tracking System...")
    
    try:
        # Initialize system
        pnl_system = AlgorandPnLTrackingSystem()
        
        # Start monitoring
        await pnl_system.start_monitoring()
        
    except Exception as e:
        logging.error(f"Fatal error in main: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
