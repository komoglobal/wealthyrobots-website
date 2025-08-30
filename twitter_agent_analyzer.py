#!/usr/bin/env python3
"""
Twitter Agent Analysis & Consolidation
Analyzes all Twitter agents to understand their functions and create consolidation strategy
"""

import os
import json
from datetime import datetime

class TwitterAgentAnalyzer:
    def __init__(self):
        self.twitter_agents = [
            'social_media_agent.py',
            'twitter_posting_agent.py', 
            'auto_twitter_empire.py',
            'post_to_twitter.py',
            'multi_platform_affiliate.py'
        ]
        self.agent_analysis = {}
        
    def analyze_agent_functions(self, agent_file):
        """Analyze what a specific agent does"""
        if not os.path.exists(agent_file):
            return {"status": "not_found"}
        
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            analysis = {
                "status": "found",
                "file_size": len(content),
                "functions": [],
                "capabilities": {
                    "posts_content": False,
                    "generates_threads": False,
                    "handles_images": False,
                    "manages_scheduling": False,
                    "affiliate_integration": False,
                    "engagement_tracking": False,
                    "hashtag_management": False,
                    "profile_management": False
                },
                "posting_frequency": "unknown",
                "content_types": [],
                "key_features": []
            }
            
            # Analyze functions
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('def '):
                    func_name = line.strip().split('def ')[1].split('(')[0]
                    analysis["functions"].append(func_name)
            
            # Analyze capabilities
            content_lower = content.lower()
            
            # Check posting capabilities
            if any(keyword in content_lower for keyword in ['tweet', 'post', 'update_status']):
                analysis["capabilities"]["posts_content"] = True
            
            if any(keyword in content_lower for keyword in ['thread', 'viral_thread', 'smart_thread']):
                analysis["capabilities"]["generates_threads"] = True
            
            if any(keyword in content_lower for keyword in ['image', 'photo', 'media', 'visual']):
                analysis["capabilities"]["handles_images"] = True
            
            if any(keyword in content_lower for keyword in ['schedule', 'interval', 'frequency', 'timer']):
                analysis["capabilities"]["manages_scheduling"] = True
            
            if any(keyword in content_lower for keyword in ['affiliate', 'amazon', 'wealthyrobot-20']):
                analysis["capabilities"]["affiliate_integration"] = True
            
            if any(keyword in content_lower for keyword in ['engagement', 'likes', 'retweets', 'replies']):
                analysis["capabilities"]["engagement_tracking"] = True
            
            if any(keyword in content_lower for keyword in ['hashtag', '#ai', '#business']):
                analysis["capabilities"]["hashtag_management"] = True
            
            if any(keyword in content_lower for keyword in ['profile', 'bio', 'avatar', 'banner']):
                analysis["capabilities"]["profile_management"] = True
            
            # Extract posting frequency if mentioned
            if 'every' in content_lower:
                for line in lines:
                    if 'every' in line.lower() and any(time_word in line.lower() for time_word in ['hour', 'minute', 'day']):
                        analysis["posting_frequency"] = line.strip()[:100]
                        break
            
            # Identify content types
            if 'educational' in content_lower:
                analysis["content_types"].append("educational")
            if 'entertaining' in content_lower:
                analysis["content_types"].append("entertaining")
            if 'community' in content_lower:
                analysis["content_types"].append("community")
            if 'promotional' in content_lower or 'affiliate' in content_lower:
                analysis["content_types"].append("promotional")
            
            # Key features
            if analysis["capabilities"]["generates_threads"]:
                analysis["key_features"].append("Thread Generation")
            if analysis["capabilities"]["handles_images"]:
                analysis["key_features"].append("Image Handling")
            if analysis["capabilities"]["manages_scheduling"]:
                analysis["key_features"].append("Scheduling")
            if analysis["capabilities"]["affiliate_integration"]:
                analysis["key_features"].append("Affiliate Links")
            
            return analysis
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def analyze_current_posting_schedule(self):
        """Analyze current posting schedule from config and recent activity"""
        schedule_analysis = {
            "config_schedule": "unknown",
            "actual_activity": [],
            "recommended_affiliate_frequency": "1 per day (25% of posts)"
        }
        
        # Check config
        try:
            with open('live_config.json', 'r') as f:
                config = json.load(f)
            
            posting_config = config.get('posting', {})
            if posting_config:
                interval = posting_config.get('interval_hours', 'unknown')
                posts_per_day = posting_config.get('posts_per_day', 'unknown')
                schedule_analysis["config_schedule"] = f"{posts_per_day} posts/day, every {interval} hours"
        except:
            pass
        
        # Check recent activity pattern
        import glob
        thread_files = glob.glob("smart_viral_thread_*.txt")
        thread_files.sort(key=os.path.getmtime, reverse=True)
        
        for file_path in thread_files[:10]:
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                with open(file_path, 'r') as f:
                    content = f.read()
                
                has_affiliate = 'wealthyrobot-20' in content or 'amazon.com' in content
                
                schedule_analysis["actual_activity"].append({
                    "file": file_path,
                    "time": file_time.strftime("%Y-%m-%d %H:%M"),
                    "has_affiliate": has_affiliate,
                    "content_length": len(content)
                })
            except:
                pass
        
        return schedule_analysis
    
    def create_consolidation_strategy(self):
        """Create strategy for consolidating Twitter agents"""
        strategy = {
            "primary_agent": None,
            "agents_to_keep": [],
            "agents_to_merge": [],
            "agents_to_disable": [],
            "consolidation_plan": [],
            "posting_strategy": {
                "total_posts_per_day": 4,
                "affiliate_posts_per_day": 1,
                "value_posts_per_day": 3,
                "posting_schedule": "Every 6 hours (0:00, 6:00, 12:00, 18:00)"
            }
        }
        
        # Analyze each agent's capabilities
        agent_capabilities = {}
        for agent in self.twitter_agents:
            analysis = self.agent_analysis.get(agent, {})
            if analysis.get("status") == "found":
                capabilities = analysis.get("capabilities", {})
                agent_capabilities[agent] = capabilities
        
        # Determine primary agent (most comprehensive)
        best_agent = None
        max_capabilities = 0
        
        for agent, capabilities in agent_capabilities.items():
            capability_count = sum(1 for cap in capabilities.values() if cap)
            if capability_count > max_capabilities:
                max_capabilities = capability_count
                best_agent = agent
        
        strategy["primary_agent"] = best_agent
        
        # Categorize agents
        for agent, capabilities in agent_capabilities.items():
            if agent == best_agent:
                strategy["agents_to_keep"].append(agent)
            elif capabilities.get("generates_threads") and capabilities.get("affiliate_integration"):
                strategy["agents_to_merge"].append(agent)
            else:
                strategy["agents_to_disable"].append(agent)
        
        # Create consolidation plan
        strategy["consolidation_plan"] = [
            f"Keep {best_agent} as primary posting agent",
            f"Merge unique features from {len(strategy['agents_to_merge'])} other agents",
            f"Disable {len(strategy['agents_to_disable'])} redundant agents",
            "Implement 4-post daily schedule with 1 affiliate post",
            "Add intelligent content rotation (educational/entertaining/community/affiliate)"
        ]
        
        return strategy
    
    def run_analysis(self):
        """Run complete Twitter agent analysis"""
        print("🔍 Analyzing Twitter Agents...")
        
        # Analyze each agent
        for agent in self.twitter_agents:
            print(f"\nAnalyzing {agent}...")
            self.agent_analysis[agent] = self.analyze_agent_functions(agent)
        
        # Analyze current schedule
        print(f"\nAnalyzing current posting schedule...")
        schedule_analysis = self.analyze_current_posting_schedule()
        
        # Create consolidation strategy
        print(f"\nCreating consolidation strategy...")
        consolidation_strategy = self.create_consolidation_strategy()
        
        return {
            "agent_analysis": self.agent_analysis,
            "schedule_analysis": schedule_analysis,
            "consolidation_strategy": consolidation_strategy
        }
    
    def print_analysis_report(self, results):
        """Print comprehensive analysis report"""
        print("\n" + "="*70)
        print("🐦 TWITTER AGENT ANALYSIS REPORT")
        print("="*70)
        
        # Agent Analysis
        print(f"\n📊 AGENT CAPABILITIES ANALYSIS:")
        for agent, analysis in results["agent_analysis"].items():
            if analysis.get("status") == "found":
                print(f"\n   📱 {agent}:")
                capabilities = analysis.get("capabilities", {})
                for cap_name, has_cap in capabilities.items():
                    icon = "✅" if has_cap else "❌"
                    print(f"     {icon} {cap_name.replace('_', ' ').title()}")
                
                if analysis.get("key_features"):
                    print(f"     🔑 Key Features: {', '.join(analysis['key_features'])}")
                
                if analysis.get("functions"):
                    print(f"     🔧 Functions: {len(analysis['functions'])} total")
            else:
                print(f"\n   ❌ {agent}: {analysis.get('status', 'unknown')}")
        
        # Current Schedule
        print(f"\n⏰ CURRENT POSTING SCHEDULE:")
        schedule = results["schedule_analysis"]
        print(f"   Config Schedule: {schedule.get('config_schedule', 'Not configured')}")
        
        print(f"\n   Recent Activity (last 10 posts):")
        for activity in schedule.get("actual_activity", [])[:5]:
            affiliate_icon = "💰" if activity["has_affiliate"] else "📝"
            print(f"     {affiliate_icon} {activity['time']} - {activity['file']}")
        
        # Consolidation Strategy
        print(f"\n🎯 CONSOLIDATION STRATEGY:")
        strategy = results["consolidation_strategy"]
        
        print(f"   Primary Agent: {strategy.get('primary_agent', 'TBD')}")
        print(f"   Agents to Keep: {len(strategy.get('agents_to_keep', []))}")
        print(f"   Agents to Merge: {len(strategy.get('agents_to_merge', []))}")
        print(f"   Agents to Disable: {len(strategy.get('agents_to_disable', []))}")
        
        print(f"\n📅 RECOMMENDED POSTING STRATEGY:")
        posting = strategy.get("posting_strategy", {})
        print(f"   Total Posts/Day: {posting.get('total_posts_per_day', 4)}")
        print(f"   Affiliate Posts/Day: {posting.get('affiliate_posts_per_day', 1)}")
        print(f"   Value Posts/Day: {posting.get('value_posts_per_day', 3)}")
        print(f"   Schedule: {posting.get('posting_schedule', 'Every 6 hours')}")
        
        print(f"\n🔧 CONSOLIDATION PLAN:")
        for i, step in enumerate(strategy.get("consolidation_plan", []), 1):
            print(f"   {i}. {step}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print(f"   • Consolidate to 1 primary posting agent")
        print(f"   • Maintain 3:1 value-to-affiliate ratio")
        print(f"   • Use 6-hour posting intervals")
        print(f"   • Implement content type rotation")
        print(f"   • Add engagement tracking")
        
        print("\n" + "="*70)
    
    def create_consolidated_agent_template(self, results):
        """Create template for consolidated Twitter agent"""
        strategy = results["consolidation_strategy"]
        primary_agent = strategy.get("primary_agent", "social_media_agent.py")
        
        template = f'''#!/usr/bin/env python3
"""
Consolidated Twitter Agent - WealthyRobot
Handles all Twitter posting with smart content rotation and affiliate integration
Based on analysis of existing agents: {", ".join(self.twitter_agents)}
"""

import json
import time
import random
from datetime import datetime, timedelta

class ConsolidatedTwitterAgent:
    def __init__(self):
        self.config = self.load_config()
        self.content_types = ["educational", "entertaining", "community", "affiliate"]
        self.last_post_times = {{}}
        self.daily_post_count = 0
        self.daily_affiliate_count = 0
        
    def load_config(self):
        """Load configuration"""
        try:
            with open('live_config.json', 'r') as f:
                return json.load(f)
        except:
            return {{}}
    
    def should_post_now(self):
        """Check if posting is allowed based on schedule"""
        posting_config = self.config.get('posting', {{}})
        interval_hours = posting_config.get('interval_hours', 6)
        max_daily = posting_config.get('posts_per_day', 4)
        
        # Check daily limit
        if self.daily_post_count >= max_daily:
            return False, "Daily limit reached"
        
        # Check time interval
        now = datetime.now()
        last_post = self.last_post_times.get('last_post', datetime.min)
        
        if (now - last_post).total_seconds() < interval_hours * 3600:
            return False, "Too soon since last post"
        
        return True, "OK to post"
    
    def determine_content_type(self):
        """Determine what type of content to post next"""
        affiliate_config = self.config.get('affiliate', {{}})
        max_affiliate_daily = 1  # 1 affiliate post per day
        
        # If we haven't posted affiliate content today and it's time
        if self.daily_affiliate_count < max_affiliate_daily:
            # 25% chance for affiliate content, or if we're late in the day
            if random.random() < 0.25 or self.daily_post_count >= 3:
                return "affiliate"
        
        # Otherwise, rotate through value content
        value_types = ["educational", "entertaining", "community"]
        return random.choice(value_types)
    
    def generate_content(self, content_type):
        """Generate content based on type"""
        # This would integrate with your existing content generation
        # from dynamic_content_selector.py and other agents
        
        if content_type == "affiliate":
            return self.generate_affiliate_content()
        elif content_type == "educational":
            return self.generate_educational_content()
        elif content_type == "entertaining":
            return self.generate_entertaining_content()
        else:  # community
            return self.generate_community_content()
    
    def generate_affiliate_content(self):
        """Generate affiliate content with product promotion"""
        affiliate_config = self.config.get('affiliate', {{}})
        
        # Educational content with affiliate CTA
        content = self.generate_educational_content()
        
        # Add affiliate link
        cta_templates = affiliate_config.get('cta_templates', [
            "📚 Master AI in business with '{{product_name}}': {{product_url}}"
        ])
        
        cta = random.choice(cta_templates).format(
            product_name=affiliate_config.get('product_name', 'The AI Advantage'),
            product_url=affiliate_config.get('product_url', '')
        )
        
        return content + "\\n\\n" + cta + "\\n\\n#AI #Business #WealthyRobot"
    
    def generate_educational_content(self):
        """Generate educational content about AI/business"""
        # Integrate with your existing content generation logic
        return "Educational AI content here..."
    
    def generate_entertaining_content(self):
        """Generate entertaining/engaging content"""
        return "Entertaining AI content here..."
    
    def generate_community_content(self):
        """Generate community-building content"""
        return "Community engagement content here..."
    
    def post_to_twitter(self, content, content_type):
        """Post content to Twitter with proper tracking"""
        try:
            # Your existing Twitter posting logic here
            print(f"Posting {{content_type}} content: {{content[:100]}}...")
            
            # Update tracking
            self.last_post_times['last_post'] = datetime.now()
            self.daily_post_count += 1
            
            if content_type == "affiliate":
                self.daily_affiliate_count += 1
            
            return True
            
        except Exception as e:
            print(f"Error posting: {{e}}")
            return False
    
    def run_posting_cycle(self):
        """Run one posting cycle"""
        can_post, reason = self.should_post_now()
        
        if not can_post:
            print(f"⏰ Skipping post: {{reason}}")
            return False
        
        # Determine content type
        content_type = self.determine_content_type()
        
        # Generate content
        content = self.generate_content(content_type)
        
        # Post to Twitter
        success = self.post_to_twitter(content, content_type)
        
        if success:
            print(f"✅ Successfully posted {{content_type}} content")
        
        return success

# Usage
if __name__ == "__main__":
    agent = ConsolidatedTwitterAgent()
    agent.run_posting_cycle()
'''
        
        return template

def main():
    analyzer = TwitterAgentAnalyzer()
    
    print("🐦 Twitter Agent Analysis & Consolidation")
    print("="*50)
    print("Analyzing your Twitter agents to create consolidation strategy...")
    
    # Run analysis
    results = analyzer.run_analysis()
    
    # Print report
    analyzer.print_analysis_report(results)
    
    # Offer to create consolidated agent
    response = input("\nWould you like to see a consolidated agent template? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        template = analyzer.create_consolidated_agent_template(results)
        
        # Save template
        with open('consolidated_twitter_agent_template.py', 'w') as f:
            f.write(template)
        
        print("\n✅ Consolidated agent template saved to: consolidated_twitter_agent_template.py")
        print("\n💡 This template shows how to merge all your Twitter agents into one efficient system.")

if __name__ == "__main__":
    main()
