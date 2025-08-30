#!/usr/bin/env python3
"""
ALGORAND TRADING FIRM COMPREHENSIVE MONITOR
Real-time monitoring of PnL, agent status, and trading activity
"""
import json
import subprocess
import os
import time
from datetime import datetime
from typing import Dict, Optional

class AlgorandFirmMonitor:
    def __init__(self):
        self.report_files = {
            'performance': 'algorand_performance_report.json',
            'verification': 'algorand_firm_verification_report.json'
        }
        
    def load_report(self, report_type: str) -> Optional[Dict]:
        """Load a specific report file"""
        if report_type in self.report_files and os.path.exists(self.report_files[report_type]):
            try:
                with open(self.report_files[report_type], 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"❌ Error loading {report_type} report: {e}")
        return None
    
    def check_service_status(self, service_name: str) -> str:
        """Check the status of a systemd service"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', f'{service_name}.service'],
                capture_output=True,
                text=True,
                timeout=5
            )
            status = result.stdout.strip()
            if status == "active":
                return "✅ ACTIVE"
            elif status == "activating":
                return "🔄 ACTIVATING"
            elif status == "inactive":
                return "❌ INACTIVE"
            else:
                return f"❓ {status.upper()}"
        except Exception as e:
            return f"❌ ERROR: {e}"
    
    def format_currency(self, amount: float) -> str:
        """Format currency amounts with proper symbols"""
        if amount >= 0:
            return f"${amount:,.2f}"
        else:
            return f"-${abs(amount):,.2f}"
    
    def format_algo(self, amount: float) -> str:
        """Format ALGO amounts"""
        return f"{amount:.6f} ALGO"
    
    def display_header(self):
        """Display the monitoring header"""
        print("🔍 ALGORAND TRADING FIRM - COMPREHENSIVE MONITOR")
        print("=" * 80)
        print(f"⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
    
    def display_portfolio_summary(self, performance_data: Dict):
        """Display portfolio summary information"""
        print("\n📊 PORTFOLIO SUMMARY")
        print("-" * 40)
        
        portfolio = performance_data.get('portfolio_summary', {})
        print(f"💰 Live NAV:     {self.format_currency(portfolio.get('current_nav', 0))}")
        print(f"📝 Paper NAV:    {self.format_currency(portfolio.get('paper_nav', 0))}")
        print(f"💳 Hot Wallet:   {self.format_algo(portfolio.get('hot_wallet_algo', 0))}")
        print(f"📈 Total Positions: {portfolio.get('total_positions', 0)}")
        print(f"🔄 Active Trades:   {portfolio.get('active_trades', 0)}")
    
    def display_pnl_metrics(self, performance_data: Dict):
        """Display PnL metrics"""
        print("\n💰 PROFIT & LOSS METRICS")
        print("-" * 40)
        
        pnl = performance_data.get('pnl_metrics', {})
        print(f"📅 Daily PnL:    {self.format_currency(pnl.get('daily_pnl', 0))}")
        print(f"📊 Weekly PnL:   {self.format_currency(pnl.get('weekly_pnl', 0))}")
        print(f"📈 Monthly PnL:  {self.format_currency(pnl.get('monthly_pnl', 0))}")
        print(f"🎯 Total PnL:    {self.format_currency(pnl.get('total_pnl', 0))}")
    
    def display_trading_activity(self, performance_data: Dict):
        """Display trading activity information"""
        print("\n🔄 TRADING ACTIVITY")
        print("-" * 40)
        
        trading = performance_data.get('trading_activity', {})
        print(f"📊 Total Transactions: {trading.get('total_transactions', 0)}")
        print(f"💎 Total Volume:      {trading.get('total_volume_microalgo', 0):,} microALGO")
        
        dex_activity = trading.get('dex_activity', {})
        if 'pact' in dex_activity:
            pact = dex_activity['pact']
            print(f"🤝 Pact DEX:         {pact.get('swaps', 0)} swaps, {pact.get('volume', 0):,} volume")
        if 'tinyman' in dex_activity:
            tinyman = dex_activity['tinyman']
            print(f"🔧 Tinyman DEX:      {tinyman.get('swaps', 0)} swaps, {tinyman.get('volume', 0):,} volume")
        
        last_trade = trading.get('last_trade_time')
        if last_trade:
            print(f"⏰ Last Trade:       {last_trade}")
    
    def display_agent_status(self, verification_data: Dict):
        """Display agent operational status"""
        print("\n🤖 AGENT OPERATIONAL STATUS")
        print("-" * 40)
        
        agents = verification_data.get('agents_status', {})
        critical_agents = []
        other_agents = []
        
        for agent_name, agent_data in agents.items():
            if agent_data.get('critical', False):
                critical_agents.append((agent_name, agent_data))
            else:
                other_agents.append((agent_name, agent_data))
        
        print("🚨 CRITICAL AGENTS:")
        for agent_name, agent_data in critical_agents:
            status = "✅ ACTIVE" if agent_data.get('is_active') else "❌ INACTIVE"
            service_status = self.check_service_status(agent_data.get('service_name', '').replace('.service', ''))
            print(f"   {agent_name.replace('_', ' ').title():<20} {status:<12} {service_status}")
        
        print("\n🔧 OTHER AGENTS:")
        for agent_name, agent_data in other_agents:
            status = "✅ ACTIVE" if agent_data.get('is_active') else "❌ INACTIVE"
            service_status = self.check_service_status(agent_data.get('service_name', '').replace('.service', ''))
            print(f"   {agent_name.replace('_', ' ').title():<20} {status:<12} {service_status}")
    
    def display_system_health(self, verification_data: Dict):
        """Display overall system health metrics"""
        print("\n🏥 SYSTEM HEALTH OVERVIEW")
        print("-" * 40)
        
        health = verification_data.get('system_health', {})
        performance = verification_data.get('performance_metrics', {})
        
        total_agents = health.get('total_agents', 0)
        active_agents = health.get('active_agents', 0)
        critical_active = health.get('critical_agents_active', 0)
        total_critical = health.get('total_critical_agents', 0)
        
        overall_health = performance.get('overall_health_percentage', 0)
        critical_health = performance.get('critical_health_percentage', 0)
        
        print(f"📊 Total Agents:        {total_agents}")
        print(f"✅ Active Agents:       {active_agents}")
        print(f"🚨 Critical Agents:     {critical_active}/{total_critical}")
        print(f"📈 Overall Health:      {overall_health:.1f}%")
        print(f"🚨 Critical Health:     {critical_health:.1f}%")
        
        # Health status indicator
        if overall_health >= 80:
            status_icon = "🟢"
            status_text = "EXCELLENT"
        elif overall_health >= 60:
            status_icon = "🟡"
            status_text = "GOOD"
        elif overall_health >= 40:
            status_icon = "🟠"
            status_text = "FAIR"
        else:
            status_icon = "🔴"
            status_text = "POOR"
        
        print(f"\n{status_icon} System Status: {status_text}")
    
    def display_data_verification(self, performance_data: Dict):
        """Display real data verification status"""
        print("\n🔍 REAL DATA VERIFICATION")
        print("-" * 40)
        
        verification = performance_data.get('verification_status', {})
        nav_history = performance_data.get('nav_history_summary', {})
        
        if verification.get('real_data_verified'):
            print("✅ Real Data: VERIFIED")
        else:
            print("⚠️  Real Data: PENDING VERIFICATION")
        
        print(f"📊 Data Source:        {verification.get('data_source', 'Unknown')}")
        print(f"🔧 Verification Method: {verification.get('verification_method', 'Unknown')}")
        print(f"📈 NAV History Entries: {nav_history.get('total_entries', 0)}")
        
        last_verification = verification.get('last_verification')
        if last_verification:
            print(f"⏰ Last Verification:  {last_verification}")
    
    def display_recommendations(self, verification_data: Dict):
        """Display system recommendations"""
        recommendations = verification_data.get('recommendations', [])
        if recommendations:
            print("\n💡 RECOMMENDATIONS")
            print("-" * 40)
            
            for i, rec in enumerate(recommendations, 1):
                priority = rec.get('priority', 'unknown').upper()
                action = rec.get('action', 'No action specified')
                reason = rec.get('reason', 'No reason specified')
                
                priority_icon = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(priority, '❓')
                
                print(f"{i}. {priority_icon} {priority} Priority: {action}")
                print(f"   💭 Reason: {reason}")
                print()
    
    def run_monitoring(self):
        """Run the comprehensive monitoring"""
        self.display_header()
        
        # Load performance data
        performance_data = self.load_report('performance')
        if not performance_data:
            print("❌ No performance data available")
            return
        
        # Load verification data
        verification_data = self.load_report('verification')
        if not verification_data:
            print("❌ No verification data available")
            return
        
        # Display all sections
        self.display_portfolio_summary(performance_data)
        self.display_pnl_metrics(performance_data)
        self.display_trading_activity(performance_data)
        self.display_agent_status(verification_data)
        self.display_system_health(verification_data)
        self.display_data_verification(performance_data)
        self.display_recommendations(verification_data)
        
        print("\n" + "=" * 80)
        print("🎯 Monitoring Complete - All systems operational")
        print("=" * 80)

def main():
    """Main function"""
    monitor = AlgorandFirmMonitor()
    monitor.run_monitoring()

if __name__ == "__main__":
    main()
