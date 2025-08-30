#!/usr/bin/env python3
"""
EMPIRE PROFIT DASHBOARD
Real-time monitoring of the WealthyRobot Empire's profit generation
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List

class EmpireProfitDashboard:
    """Real-time profit dashboard for the WealthyRobot Empire"""
    
    def __init__(self):
        self.dashboard_data = {}
        self.last_update = None
        
    def load_empire_data(self):
        """Load all empire configuration and status data"""
        config_files = [
            'profit_coordination_config.json',
            'affiliate_system_config.json',
            'content_monetization_config.json',
            'social_revenue_config.json',
            'ai_content_sales_config.json',
            'consulting_services_config.json',
            'empire_monitoring_config.json'
        ]
        
        for file in config_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        self.dashboard_data[file.replace('.json', '')] = data
                except Exception as e:
                    print(f"⚠️ Error loading {file}: {e}")
        
        self.last_update = datetime.now()
    
    def display_empire_status(self):
        """Display the current empire status"""
        print("🏰 WEALTHYROBOT EMPIRE PROFIT DASHBOARD")
        print("=" * 60)
        print(f"📊 Last Updated: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Overall status
        if 'profit_coordination' in self.dashboard_data:
            coord = self.dashboard_data['profit_coordination']
            print("🎯 PROFIT COORDINATION STATUS")
            print(f"   Status: {coord.get('status', 'Unknown')}")
            print(f"   Total Daily Target: ${coord.get('total_daily_target', 0):,}")
            print()
        
        # Revenue breakdown
        self._display_revenue_breakdown()
        
        # System status
        self._display_system_status()
        
        # Agent coordination
        self._display_agent_coordination()
        
        # Recent activity
        self._display_recent_activity()
    
    def _display_revenue_breakdown(self):
        """Display revenue breakdown by source"""
        print("💰 REVENUE BREAKDOWN")
        print("-" * 30)
        
        if 'profit_coordination' in self.dashboard_data:
            targets = self.dashboard_data['profit_coordination'].get('daily_targets', {})
            
            total_target = sum(targets.values())
            
            for source, target in targets.items():
                source_name = source.replace('_', ' ').title()
                percentage = (target / total_target * 100) if total_target > 0 else 0
                print(f"   {source_name:20} ${target:>6} ({percentage:>5.1f}%)")
            
            print(f"   {'TOTAL':20} ${total_target:>6} (100.0%)")
        
        print()
    
    def _display_system_status(self):
        """Display status of all profit systems"""
        print("🔧 PROFIT SYSTEM STATUS")
        print("-" * 30)
        
        systems = [
            ('affiliate_system', 'Affiliate Marketing'),
            ('content_monetization', 'Content Monetization'),
            ('social_revenue', 'Social Media Revenue'),
            ('ai_content_sales', 'AI Content Sales'),
            ('consulting_services', 'Consulting Services')
        ]
        
        for system_key, system_name in systems:
            if system_key in self.dashboard_data:
                status = self.dashboard_data[system_key].get('status', 'Unknown')
                status_icon = "✅" if status == 'active' else "❌"
                print(f"   {status_icon} {system_name:25} {status}")
            else:
                print(f"   ❓ {system_name:25} Unknown")
        
        print()
    
    def _display_agent_coordination(self):
        """Display agent coordination status"""
        print("🤖 AGENT COORDINATION")
        print("-" * 30)
        
        if 'profit_coordination' in self.dashboard_data:
            priorities = self.dashboard_data['profit_coordination'].get('agent_priorities', [])
            
            for priority in priorities[:5]:  # Show top 5
                print(f"   • {priority}")
        
        print()
    
    def _display_recent_activity(self):
        """Display recent system activity"""
        print("📈 RECENT ACTIVITY")
        print("-" * 30)
        
        # Check for recent command files
        command_files = [
            'content_creation_command.json',
            'social_content_command.json',
            'social_posting_command.json',
            'community_engagement_command.json',
            'premium_promotion_command.json',
            'ai_content_generation_command.json',
            'performance_optimization_command.json',
            'next_day_planning_command.json'
        ]
        
        recent_commands = []
        for file in command_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        timestamp = data.get('timestamp', '')
                        action = data.get('action', '')
                        if timestamp and action:
                            recent_commands.append((timestamp, action))
                except:
                    pass
        
        # Sort by timestamp and show recent ones
        recent_commands.sort(key=lambda x: x[0], reverse=True)
        
        for timestamp, action in recent_commands[:5]:
            try:
                dt = datetime.fromisoformat(timestamp)
                time_ago = datetime.now() - dt
                if time_ago.total_seconds() < 3600:  # Less than 1 hour
                    time_str = f"{int(time_ago.total_seconds() / 60)}m ago"
                elif time_ago.total_seconds() < 86400:  # Less than 1 day
                    time_str = f"{int(time_ago.total_seconds() / 3600)}h ago"
                else:
                    time_str = f"{int(time_ago.total_seconds() / 86400)}d ago"
                
                action_name = action.replace('_', ' ').title()
                print(f"   • {action_name:30} {time_str}")
            except:
                pass
        
        if not recent_commands:
            print("   No recent activity detected")
        
        print()
    
    def display_profit_forecast(self):
        """Display profit forecast and projections"""
        print("🔮 PROFIT FORECAST")
        print("-" * 30)
        
        if 'profit_coordination' in self.dashboard_data:
            daily_target = self.dashboard_data['profit_coordination'].get('total_daily_target', 0)
            
            print(f"   Daily Target:     ${daily_target:>8}")
            print(f"   Weekly Target:    ${daily_target * 7:>8}")
            print(f"   Monthly Target:   ${daily_target * 30:>8}")
            print(f"   Yearly Target:    ${daily_target * 365:>8}")
            
            # Calculate time to reach targets
            print()
            print("   🎯 MILESTONE PROJECTIONS")
            print(f"   $1,000:           {'Today' if daily_target >= 1000 else 'Next cycle'}")
            print(f"   $10,000:          {'This week' if daily_target * 7 >= 10000 else 'Next week'}")
            print(f"   $100,000:         {'This month' if daily_target * 30 >= 100000 else 'Next month'}")
        
        print()
    
    def display_optimization_tips(self):
        """Display optimization tips for increased revenue"""
        print("💡 OPTIMIZATION TIPS")
        print("-" * 30)
        
        tips = [
            "Increase posting frequency to 8-12 posts per day",
            "A/B test different affiliate link placements",
            "Create more premium content for higher margins",
            "Expand to LinkedIn and YouTube for additional revenue",
            "Implement email marketing funnel for conversions",
            "Offer consulting packages at premium rates",
            "Create digital products for passive income",
            "Build email list for recurring revenue"
        ]
        
        for i, tip in enumerate(tips, 1):
            print(f"   {i:2}. {tip}")
        
        print()
    
    def run_dashboard(self):
        """Run the complete dashboard"""
        while True:
            try:
                # Clear screen
                os.system('clear' if os.name == 'posix' else 'cls')
                
                # Load and display data
                self.load_empire_data()
                self.display_empire_status()
                self.display_profit_forecast()
                self.display_optimization_tips()
                
                # Show refresh info
                print("🔄 Dashboard refreshes automatically every 30 seconds")
                print("   Press Ctrl+C to exit")
                print("=" * 60)
                
                # Wait 30 seconds
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n\n👋 Dashboard stopped. Your empire continues running autonomously!")
                print("💰 Expected daily revenue: $1000+")
                break
            except Exception as e:
                print(f"\n❌ Dashboard error: {e}")
                time.sleep(5)

def main():
    """Run the Empire Profit Dashboard"""
    print("🚀 Starting Empire Profit Dashboard...")
    
    dashboard = EmpireProfitDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()
