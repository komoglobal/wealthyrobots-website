#!/usr/bin/env python3
"""
Twitter Empire Manager - Unified control of all Twitter operations
Coordinates CEO decisions, content generation, visuals, and posting
"""
import os
import time
import random
from datetime import datetime
from twitter_safety_config import safe_twitter_post

class TwitterEmpireManager:
    def __init__(self):
        self.ceo_decision_weights = {
            'audience_building': 0.7,  # 70% audience building
            'revenue_generation': 0.3   # 30% revenue posts
        }
        
        self.content_types = {
            'educational': ['tips', 'tutorials', 'insights', 'strategies'],
            'viral': ['threads', 'controversial', 'trending', 'stories'],
            'promotional': ['affiliate', 'product', 'service', 'offer']
        }
        
        self.posting_schedule = {
            'peak_hours': [9, 13, 17, 21],  # 4 optimal posting times
            'max_daily_posts': 12,
            'min_hours_between': 2
        }
    
    def ceo_content_decision(self):
        """CEO decides content strategy based on current goals"""
        
        # Simulate CEO decision making
        current_hour = datetime.now().hour
        
        # Morning: Build audience (educational)
        if 6 <= current_hour <= 12:
            return 'educational', 0.8  # 80% educational
            
        # Afternoon: Mixed strategy
        elif 13 <= current_hour <= 17:
            return 'viral', 0.7  # 70% viral content
            
        # Evening: Revenue focus
        elif 18 <= current_hour <= 22:
            return 'promotional', 0.3  # 30% promotional
            
        # Late night: Audience building
        else:
            return 'educational', 0.9  # 90% educational
    
    def generate_viral_content(self, content_type, educational_ratio):
        """Generate viral content based on CEO decision"""
        
        if content_type == 'educational':
            templates = [
                "🧠 5 AI productivity secrets that changed my workflow:\n\n1️⃣ {tip1}\n2️⃣ {tip2}\n3️⃣ {tip3}\n4️⃣ {tip4}\n5️⃣ {tip5}\n\n{cta}",
                "⚡ The biggest AI mistakes I see entrepreneurs make:\n\n❌ {mistake1}\n❌ {mistake2}\n❌ {mistake3}\n\n✅ {solution}\n\n{cta}",
                "🚀 How AI transformed my business in 30 days:\n\n📈 Before: {before}\n📈 After: {after}\n📈 Method: {method}\n\n{cta}"
            ]
        elif content_type == 'viral':
            templates = [
                "🧵 THREAD: Why everyone is talking about AI but missing the point...\n\n👇 The real opportunity (and how to seize it):\n\n{content}\n\n{cta}",
                "🔥 Unpopular opinion: AI won't replace humans...\n\nIt will replace humans who don't use AI.\n\n{content}\n\n{cta}",
                "💡 I spent 100 hours testing AI tools so you don't have to:\n\n{content}\n\n{cta}"
            ]
        else:  # promotional
            templates = [
                "🎯 Ready to master AI and boost your income?\n\n{content}\n\n📚 Start here: {affiliate_link}\n\n{hashtags}",
                "💰 The AI revolution is creating millionaires daily.\n\n{content}\n\n🚀 Join them: {affiliate_link}\n\n{hashtags}"
            ]
        
        template = random.choice(templates)
        
        # Add affiliate link based on educational ratio
        if educational_ratio < 0.7:  # Less than 70% educational = add affiliate
            cta = "📚 Master AI strategies: https://amzn.to/ai-advantage"
        else:
            cta = "What's your experience with AI? Drop a comment! 👇"
        
        hashtags = "#AI #Automation #Productivity #WealthyRobot"
        
        return template.format(
            tip1="Automate repetitive tasks first",
            tip2="Use AI for research and analysis", 
            tip3="Create content 10x faster",
            tip4="Build AI-powered workflows",
            tip5="Scale with AI assistants",
            mistake1="Using AI like Google search",
            mistake2="Not training it properly",
            mistake3="Ignoring automation potential",
            solution="Think systems, not tasks",
            before="Manual processes, long hours",
            after="Automated workflows, 3x output",
            method="Strategic AI integration",
            content="Here's what I learned...",
            cta=cta,
            affiliate_link="https://amzn.to/ai-advantage",
            hashtags=hashtags
        )
    
    def coordinate_posting(self):
        """Coordinate all posting to avoid API conflicts"""
        
        # Check if it's a good time to post
        current_hour = datetime.now().hour
        if current_hour not in self.posting_schedule['peak_hours']:
            return False, "Not optimal posting time"
        
        # Get CEO decision
        content_type, educational_ratio = self.ceo_content_decision()
        
        # Generate content
        content = self.generate_viral_content(content_type, educational_ratio)
        
        # Post safely
        success, message = safe_twitter_post(content, f"Empire_Manager_{content_type}")
        
        if success:
            print(f"✅ Posted {content_type} content (edu ratio: {educational_ratio})")
            return True, content
        else:
            print(f"❌ Posting failed: {message}")
            return False, content

if __name__ == "__main__":
    manager = TwitterEmpireManager()
    success, content = manager.coordinate_posting()
    
    if success:
        print("\n📝 Content posted:")
        print("-" * 50)
        print(content)
        print("-" * 50)
    else:
        print(f"Posting blocked: {content}")
