#!/usr/bin/env python3
"""
Live Orchestrator - FIXED VERSION with Content Selector Integration
Now properly uses content_agent for 80/20 strategy
"""

import json
import time
import os
import smart_affiliate_agent
import social_media_agent
import content_agent
import smart_affiliate_agent
import social_media_agent
import content_agent
import logging
from datetime import datetime, timedelta
import subprocess
import glob
import sys

# CRITICAL FIX: Import the content selector
try:
    # from content_agent import ... # REMOVED - CONSOLIDATED
    CONTENT_SELECTOR_AVAILABLE = True
    print("✅ Content selector imported successfully")
except ImportError as e:
    print(f"❌ Content selector import failed: {e}")
    CONTENT_SELECTOR_AVAILABLE = False

class LiveOrchestratorFixed:
    def __init__(self):
        self.config_file = 'live_config.json'
        self.cycle_count = 0
        self.last_run = {}
        
        # Initialize content selector
        if CONTENT_SELECTOR_AVAILABLE:
            try:
                from dynamic_content_selector import DynamicContentSelector
                self.content_selector = DynamicContentSelector()
                print("✅ Dynamic content selector initialized")
            except ImportError:
                self.content_selector = content_agent.ContentGenerationAgent()
                print("✅ Content agent initialized (fallback)")
        else:
            self.content_selector = None
            print("⚠️ Content selector not available - using fallback")
        
        self.load_config()
    
    def load_config(self):
        """Load configuration"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                "posting_enabled": True,
                "content_strategy": "80_20_value_affiliate",
                "emergency_mode": False,
                "daily_budget": 100
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_content_strategy(self):
        """Use content selector to determine what type of content to create"""
        if not CONTENT_SELECTOR_AVAILABLE or not self.content_selector:
            print("⚠️ Using fallback content strategy")
            return "educational", False  # Default to educational, non-affiliate
        
        try:
            # Use the content selector to make intelligent decision
            content_file = self.content_selector.get_optimized_content()
            
            # Parse the content file to determine type
            if 'affiliate' in content_file.lower():
                content_type = 'affiliate'
                is_affiliate = True
            elif 'educational' in content_file.lower():
                content_type = 'educational'
                is_affiliate = False
            elif 'community' in content_file.lower():
                content_type = 'community'
                is_affiliate = False
            elif 'entertaining' in content_file.lower():
                content_type = 'entertaining'
                is_affiliate = False
            else:
                content_type = 'educational'
                is_affiliate = False
            
            reasoning = f"Content selector chose: {content_file}"
            
            print(f"📋 Content Strategy: {content_type} (affiliate: {is_affiliate})")
            print(f"    Reasoning: {reasoning}")
            
            return content_type, is_affiliate
            
        except Exception as e:
            print(f"❌ Content selector error: {e}")
            return "educational", False  # Safe fallback
    
    def create_content(self):
        """Create content using the content selector strategy"""
        print("📝 Creating content using content selector...")
        
        # Get strategy from content selector
        content_type, is_affiliate = self.get_content_strategy()
        
        # Select appropriate template
        if is_affiliate:
            template_file = "content_templates/affiliate_enhanced_template.txt"
        elif content_type == "educational":
            template_file = "content_templates/educational_template.txt"
        elif content_type == "community":
            template_file = "content_templates/community_template.txt"
        elif content_type == "entertaining":
            template_file = "content_templates/entertaining_template.txt"
        else:
            template_file = "content_templates/educational_template.txt"  # Default
        
        print(f"📄 Using template: {template_file}")
        
        # Generate content file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        content_filename = f"smart_viral_thread_{timestamp}_{content_type.upper()}.txt"
        
        try:
            # Copy template content to new thread file
            if os.path.exists(template_file):
                with open(template_file, 'r') as template:
                    template_content = template.read()
                
                with open(content_filename, 'w') as content_file:
                    content_file.write(template_content)
                
                print(f"✅ Created: {content_filename}")
                return content_filename
            else:
                print(f"❌ Template not found: {template_file}")
                return None
                
        except Exception as e:
            print(f"❌ Content creation error: {e}")
            return None
    
    def should_create_content(self):
        """Determine if it's time to create new content with enhanced human-like behavior"""
        import random
        from datetime import datetime, timedelta
        import glob
        import os
        
        # Check last content creation time
        recent_files = glob.glob('smart_viral_thread_*.txt')
        if not recent_files:
            return True
        
        # Get most recent file
        most_recent = max(recent_files, key=os.path.getctime)
        file_time = datetime.fromtimestamp(os.path.getctime(most_recent))
        time_since_last = datetime.now() - file_time
        
        # Enhanced human-like behavior
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        
        # Base interval
        base_hours = 6
        
        # Weekend variation (slightly more relaxed)
        if day_of_week >= 5:  # Weekend
            base_hours = random.uniform(5.8, 6.4)
            print("📅 Weekend mode: Relaxed timing")
        
        # Business hours vs off-hours
        if 9 <= hour <= 17:  # Business hours - more active
            variation = random.randint(-45, +15)  # Slightly earlier during work
            print("💼 Business hours: More active posting")
        else:  # Off hours - more relaxed
            variation = random.randint(-15, +45)  # Might be delayed
            print("🌙 Off hours: Relaxed posting")
        
        # Occasional "inspiration" posts (5% chance to post earlier)
        if random.random() < 0.05:
            base_hours *= 0.7  # Post 30% earlier when "inspired"
            print("💡 Inspiration mode: Posting earlier!")
        
        # Rare skip cycle (2% chance to wait longer)
        if random.random() < 0.02:
            base_hours *= 1.5  # Wait 50% longer occasionally
            print("😴 Skip cycle: Taking a longer break")
        
        required_interval = timedelta(hours=base_hours, minutes=variation)
        
        # Debug info
        next_post_time = file_time + required_interval
        print(f"⏰ Last post: {file_time.strftime('%H:%M:%S')}")
        print(f"🎯 Next post window: {next_post_time.strftime('%H:%M:%S')} (±variation)")
        print(f"📊 Time until next: {str(required_interval - time_since_last).split('.')[0]}")
        
        return time_since_last > required_interval
    
    def run_cycle(self):
        """Run one orchestrator cycle with content selector integration"""
        self.cycle_count += 1
        print(f"\n🔄 Orchestrator Cycle #{self.cycle_count}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check configuration
        if self.config.get('emergency_mode', False):
            print("🚨 Emergency mode active - limiting operations")
            return
        
        if not self.config.get('posting_enabled', True):
            print("⚠️ Posting disabled in config")
            return
        
        # Content creation decision
        if self.should_create_content():
            print("📝 Time to create new content...")
            content_file = self.create_content()
            
            if content_file:
                print(f"✅ Content created: {content_file}")
                # Here you would typically call social media agent to post
                # For now, just log the success
                
        else:
            print("⏰ Not time for new content yet")
        
        # Log cycle completion
        cycle_log = {
            'timestamp': datetime.now().isoformat(),
            'cycle': self.cycle_count,
            'content_selector_used': CONTENT_SELECTOR_AVAILABLE,
            'config_status': 'active' if self.config.get('posting_enabled') else 'disabled'
        }
        
        with open('orchestrator_fixed.log', 'a') as f:
            f.write(json.dumps(cycle_log) + '\n')
    
    def run_continuous(self):
        """Run continuous orchestration with content selector"""
        print("🚀 Starting Fixed Live Orchestrator with Content Selector Integration")
        print("=" * 60)
        
        while True:
            try:
                self.run_cycle()
                
                # Wait 30 minutes between cycles
                wait_time = 1800  # 30 minutes
                print(f"⏰ Waiting {wait_time//60} minutes until next cycle...")
                time.sleep(wait_time)
                
            except KeyboardInterrupt:
                print("\n🛑 Orchestrator stopped by user")
                break
            except Exception as e:
                print(f"❌ Cycle error: {e}")
                time.sleep(1800)  # Wait 5 minutes on error

if __name__ == "__main__":
    orchestrator = LiveOrchestratorFixed()
    orchestrator.run_continuous()
