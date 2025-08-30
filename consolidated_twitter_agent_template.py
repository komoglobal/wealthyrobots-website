#!/usr/bin/env python3
"""
Consolidated Twitter Agent - WealthyRobot
Handles all Twitter posting with smart content rotation and affiliate integration
Based on analysis of existing agents: social_media_agent.py, twitter_posting_agent.py, auto_twitter_empire.py, post_to_twitter.py, multi_platform_affiliate.py
"""

import json
import time
import random
from datetime import datetime, timedelta

class ConsolidatedTwitterAgent:
    def __init__(self):
        self.config = self.load_config()
        self.content_types = ["educational", "entertaining", "community", "affiliate"]
        self.last_post_times = {}
        self.daily_post_count = 0
        self.daily_affiliate_count = 0
        
    def load_config(self):
        """Load configuration"""
        try:
            with open('live_config.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def should_post_now(self):
        """Check if posting is allowed based on schedule"""
        posting_config = self.config.get('posting', {})
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
        affiliate_config = self.config.get('affiliate', {})
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
        affiliate_config = self.config.get('affiliate', {})
        
        # Educational content with affiliate CTA
        content = self.generate_educational_content()
        
        # Add affiliate link
        cta_templates = affiliate_config.get('cta_templates', [
            "📚 Master AI in business with '{product_name}': {product_url}"
        ])
        
        cta = random.choice(cta_templates).format(
            product_name=affiliate_config.get('product_name', 'The AI Advantage'),
            product_url=affiliate_config.get('product_url', '')
        )
        
        return content + "\n\n" + cta + "\n\n#AI #Business #WealthyRobot"
    
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
            print(f"Posting {content_type} content: {content[:100]}...")
            
            # Update tracking
            self.last_post_times['last_post'] = datetime.now()
            self.daily_post_count += 1
            
            if content_type == "affiliate":
                self.daily_affiliate_count += 1
            
            return True
            
        except Exception as e:
            print(f"Error posting: {e}")
            return False
    
    def run_posting_cycle(self):
        """Run one posting cycle"""
        can_post, reason = self.should_post_now()
        
        if not can_post:
            print(f"⏰ Skipping post: {reason}")
            return False
        
        # Determine content type
        content_type = self.determine_content_type()
        
        # Generate content
        content = self.generate_content(content_type)
        
        # Post to Twitter
        success = self.post_to_twitter(content, content_type)
        
        if success:
            print(f"✅ Successfully posted {content_type} content")
        
        return success

# Usage
if __name__ == "__main__":
    agent = ConsolidatedTwitterAgent()
    agent.run_posting_cycle()
