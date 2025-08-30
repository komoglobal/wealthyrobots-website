#!/usr/bin/env python3
"""
Twitter API Safety Checker
Verifies posting frequency and rate limits before starting orchestrator
"""

import json
import os
import glob
from datetime import datetime, timedelta

class TwitterSafetyChecker:
    def __init__(self):
        self.safety_issues = []
        self.warnings = []
        self.recommendations = []
        
    def check_live_config_posting_frequency(self):
        """Check posting frequency settings in live_config.json"""
        try:
            with open('live_config.json', 'r') as f:
                config = json.load(f)
            
            print("📋 POSTING FREQUENCY ANALYSIS:")
            
            # Check for posting intervals
            posting_settings = {}
            
            if 'posting' in config:
                posting_settings = config['posting']
                print(f"   Posting Config Found: ✅")
            else:
                print(f"   Posting Config: ❌ Not found")
                self.warnings.append("No posting configuration found")
            
            # Check specific intervals
            interval_keys = ['interval', 'frequency', 'delay', 'wait_time']
            for key in interval_keys:
                if key in posting_settings:
                    print(f"   {key}: {posting_settings[key]}")
            
            # Check for rate limiting
            if 'rate_limit' in posting_settings:
                print(f"   Rate Limiting: ✅ {posting_settings['rate_limit']}")
            else:
                print(f"   Rate Limiting: ⚠️ Not explicitly set")
                self.warnings.append("No explicit rate limiting found")
            
            # Check posts per hour/day
            posts_per_hour = posting_settings.get('posts_per_hour', 'Not set')
            posts_per_day = posting_settings.get('posts_per_day', 'Not set')
            
            print(f"   Posts per hour: {posts_per_hour}")
            print(f"   Posts per day: {posts_per_day}")
            
            if posts_per_hour == 'Not set' and posts_per_day == 'Not set':
                self.warnings.append("No posting limits explicitly set")
            
            return posting_settings
            
        except FileNotFoundError:
            self.safety_issues.append("live_config.json not found")
            return {}
        except Exception as e:
            self.safety_issues.append(f"Error reading config: {e}")
            return {}
    
    def check_orchestrator_posting_logic(self):
        """Check orchestrator for posting frequency controls"""
        try:
            with open('live_orchestrator.py', 'r') as f:
                content = f.read()
            
            print("\n🤖 ORCHESTRATOR POSTING LOGIC:")
            
            # Check for time delays
            if 'time.sleep' in content:
                print("   Sleep/Delay Logic: ✅ Found")
            else:
                print("   Sleep/Delay Logic: ⚠️ Not found")
                self.warnings.append("No explicit sleep delays in orchestrator")
            
            # Check for posting intervals
            interval_keywords = ['interval', 'frequency', 'rate_limit', 'delay']
            found_intervals = []
            
            for keyword in interval_keywords:
                if keyword in content.lower():
                    found_intervals.append(keyword)
            
            if found_intervals:
                print(f"   Interval Controls: ✅ {', '.join(found_intervals)}")
            else:
                print("   Interval Controls: ❌ None found")
                self.safety_issues.append("No posting interval controls in orchestrator")
            
            # Check for Twitter API calls
            twitter_calls = ['post', 'tweet', 'update_status', 'api.update']
            api_calls_found = []
            
            for call in twitter_calls:
                if call in content.lower():
                    api_calls_found.append(call)
            
            if api_calls_found:
                print(f"   Twitter API Calls: ⚠️ {', '.join(api_calls_found)}")
                print("   ⚠️ API calls detected - verify rate limiting")
            else:
                print("   Twitter API Calls: ✅ None detected directly")
            
        except FileNotFoundError:
            self.safety_issues.append("live_orchestrator.py not found")
        except Exception as e:
            self.safety_issues.append(f"Error reading orchestrator: {e}")
    
    def check_recent_posting_activity(self):
        """Check recent posting activity to detect spam patterns"""
        print("\n📊 RECENT POSTING ACTIVITY:")
        
        # Check thread files in last 24 hours
        thread_files = glob.glob("smart_viral_thread_*.txt")
        recent_threads = []
        
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        
        for file_path in thread_files:
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time > last_24h:
                    recent_threads.append((file_path, file_time))
            except:
                pass
        
        recent_threads.sort(key=lambda x: x[1], reverse=True)
        
        print(f"   Threads in last 24h: {len(recent_threads)}")
        
        if len(recent_threads) > 24:  # More than 1 per hour
            self.safety_issues.append(f"High posting frequency: {len(recent_threads)} threads in 24h")
        elif len(recent_threads) > 12:  # More than 1 every 2 hours
            self.warnings.append(f"Moderate posting frequency: {len(recent_threads)} threads in 24h")
        else:
            print("   ✅ Posting frequency appears safe")
        
        # Show recent activity
        if recent_threads:
            print("   Recent threads:")
            for file_path, file_time in recent_threads[:5]:
                time_ago = now - file_time
                hours_ago = int(time_ago.total_seconds() / 3600)
                print(f"     • {file_path} - {hours_ago}h ago")
    
    def check_twitter_api_limits(self):
        """Check against Twitter API rate limits"""
        print("\n🔄 TWITTER API RATE LIMITS:")
        print("   Twitter API v2 limits:")
        print("     • Tweets: 300 per 15-min window (1,200/hour)")
        print("     • Tweet creation: 300 per 15-min window")
        print("     • Media uploads: 300 per 15-min window")
        
        # Recommend safe posting frequency
        print("\n   📋 RECOMMENDED SAFE FREQUENCIES:")
        print("     • Conservative: 1 post every 6 hours (4/day)")
        print("     • Moderate: 1 post every 3 hours (8/day)")
        print("     • Active: 1 post every 1 hour (24/day)")
        print("     • ⚠️ Aggressive: 1 post every 15 min (96/day)")
    
    def check_existing_agents_posting(self):
        """Check how many agents might be posting simultaneously"""
        print("\n🔀 MULTIPLE AGENT POSTING CHECK:")
        
        posting_agents = [
            'social_media_agent.py',
            'twitter_posting_agent.py', 
            'auto_twitter_empire.py',
            'post_to_twitter.py',
            'multi_platform_affiliate.py'
        ]
        
        active_posting_agents = []
        
        for agent in posting_agents:
            if os.path.exists(agent):
                try:
                    with open(agent, 'r') as f:
                        content = f.read()
                    
                    # Check if agent has active posting logic
                    if any(keyword in content.lower() for keyword in ['post', 'tweet', 'api.update']):
                        active_posting_agents.append(agent)
                except:
                    pass
        
        print(f"   Agents with posting logic: {len(active_posting_agents)}")
        
        if len(active_posting_agents) > 1:
            self.warnings.append(f"Multiple posting agents detected: {len(active_posting_agents)}")
            print("   ⚠️ Multiple agents may post simultaneously")
            for agent in active_posting_agents:
                print(f"     • {agent}")
        else:
            print("   ✅ Single posting agent detected")
    
    def generate_safety_recommendations(self):
        """Generate safety recommendations"""
        self.recommendations = []
        
        if self.safety_issues:
            self.recommendations.append("🚨 CRITICAL: Address safety issues before starting")
        
        if len(self.warnings) > 2:
            self.recommendations.append("⚠️ Review warnings and consider safer settings")
        
        # Always recommend safe defaults
        self.recommendations.extend([
            "✅ Recommended: Start with 1 post every 6 hours (4/day)",
            "✅ Monitor first few posts manually",
            "✅ Keep live_config.json posting frequency conservative",
            "✅ Use single posting agent to avoid conflicts"
        ])
    
    def run_safety_check(self):
        """Run complete safety check"""
        print("🛡️ TWITTER API SAFETY CHECK")
        print("="*50)
        
        # Check configuration
        self.check_live_config_posting_frequency()
        
        # Check orchestrator logic
        self.check_orchestrator_posting_logic()
        
        # Check recent activity
        self.check_recent_posting_activity()
        
        # Check API limits
        self.check_twitter_api_limits()
        
        # Check multiple agents
        self.check_existing_agents_posting()
        
        # Generate recommendations
        self.generate_safety_recommendations()
        
        # Print summary
        self.print_safety_summary()
    
    def print_safety_summary(self):
        """Print safety check summary"""
        print("\n" + "="*60)
        print("🛡️ SAFETY CHECK SUMMARY")
        print("="*60)
        
        if self.safety_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.safety_issues)}):")
            for issue in self.safety_issues:
                print(f"   • {issue}")
        
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in self.recommendations:
            print(f"   • {rec}")
        
        # Overall safety assessment
        if self.safety_issues:
            print(f"\n🔴 OVERALL ASSESSMENT: NOT SAFE TO START")
            print("   Fix critical issues before running orchestrator")
        elif len(self.warnings) > 3:
            print(f"\n🟡 OVERALL ASSESSMENT: PROCEED WITH CAUTION")
            print("   Review warnings and consider safer settings")
        else:
            print(f"\n🟢 OVERALL ASSESSMENT: APPEARS SAFE TO START")
            print("   Monitor first few posts to confirm")
        
        print("\n" + "="*60)

def main():
    checker = TwitterSafetyChecker()
    
    print("🚀 Starting Twitter API Safety Check...")
    print("This will verify posting frequency and rate limits before starting.\n")
    
    checker.run_safety_check()

if __name__ == "__main__":
    main()
