#!/usr/bin/env python3
"""
Master Twitter Controller - Single source of truth for all Twitter operations
Eliminates conflicts, integrates CEO decisions, content generation, and visuals
"""
import os
import time
import json
import random
from datetime import datetime, timedelta
from twitter_safety_config import safe_twitter_post

class MasterTwitterController:
    def __init__(self):
        self.last_post_time = None
        self.daily_posts = 0
        self.daily_reset = datetime.now().date()
        
        # CEO decision matrix
        self.ceo_strategy = {
            'morning': {'type': 'educational', 'affiliate_chance': 0.1},
            'afternoon': {'type': 'viral', 'affiliate_chance': 0.3}, 
            'evening': {'type': 'promotional', 'affiliate_chance': 0.7},
            'night': {'type': 'educational', 'affiliate_chance': 0.1}
        }
        
        # Content templates with viral elements
        self.viral_templates = {
            'educational': [
                "🧠 The AI productivity secret that changed everything:\n\n{content}\n\n{cta}",
                "⚡ 5 AI mistakes costing you time and money:\n\n❌ {mistake1}\n❌ {mistake2}\n❌ {mistake3}\n❌ {mistake4}\n❌ {mistake5}\n\n{solution}\n\n{cta}",
                "🚀 How I 10x'd my output with AI in 30 days:\n\n{before_after}\n\n{method}\n\n{cta}"
            ],
            'viral': [
                "🧵 THREAD: Unpopular AI opinion that will change your mind...\n\n{hook}\n\n{content}\n\n{cta}",
                "🔥 Everyone's using AI wrong. Here's the right way:\n\n{content}\n\n{revelation}\n\n{cta}",
                "💡 I tested 50 AI tools so you don't have to:\n\n{results}\n\n{top_picks}\n\n{cta}"
            ],
            'promotional': [
                "🎯 Ready to master AI and 10x your income?\n\n{value_prop}\n\n📚 Start here: {affiliate_link}\n\n{social_proof}",
                "💰 The AI revolution is creating millionaires daily.\n\n{opportunity}\n\n🚀 Join them: {affiliate_link}\n\n{urgency}"
            ]
        }
        
    def get_ceo_decision(self):
        """CEO decides content strategy based on time and goals"""
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 12:
            period = 'morning'
        elif 12 <= current_hour < 18:
            period = 'afternoon'
        elif 18 <= current_hour < 23:
            period = 'evening'
        else:
            period = 'night'
            
        strategy = self.ceo_strategy[period]
        
        # CEO decision: Should we include affiliate?
        include_affiliate = random.random() < strategy['affiliate_chance']
        
        return strategy['type'], include_affiliate
    
    def generate_viral_content(self, content_type, include_affiliate):
        """Generate viral content with proper 80/20 balance"""
        
        template = random.choice(self.viral_templates[content_type])
        
        # Dynamic content based on type
        if content_type == 'educational':
            content_data = {
                'content': "AI isn't just for tech companies anymore.\n\nSmart entrepreneurs are using it to:\n• Automate customer service\n• Create content in minutes\n• Analyze market trends\n• Scale without hiring",
                'mistake1': "Using AI like Google",
                'mistake2': "Not training it on your data", 
                'mistake3': "Ignoring automation opportunities",
                'mistake4': "Using basic prompts only",
                'mistake5': "Not integrating AI workflows",
                'solution': "✅ Think systems, not tools. Build AI-powered workflows that compound.",
                'before_after': "Before: 8 hours of manual work\nAfter: 45 minutes with AI\nResult: 10x more output, better quality",
                'method': "The secret: AI workflow automation + strategic prompting"
            }
        elif content_type == 'viral':
            content_data = {
                'hook': "AI won't replace humans... it will replace humans who don't use AI.",
                'content': "While others debate if AI is dangerous, smart people are building AI-powered businesses.\n\nThe opportunity is massive.\nThe window is closing.\nThe choice is yours.",
                'revelation': "💡 The real AI revolution isn't in the tools.\nIt's in the mindset shift.",
                'results': "🥇 Winners: Tools that save 5+ hours/week\n🥈 Good: Tools that automate specific tasks\n🥉 Meh: Basic AI assistants",
                'top_picks': "Top 3 game-changers:\n1️⃣ Claude (this conversation)\n2️⃣ Midjourney (visual content)\n3️⃣ Zapier (workflow automation)"
            }
        else:  # promotional
            content_data = {
                'value_prop': "The AI Advantage isn't just a book.\nIt's your blueprint for AI-powered wealth.",
                'opportunity': "Every day you wait, competitors gain ground.\nEvery day you learn, you pull ahead.",
                'social_proof': "Join 10,000+ entrepreneurs already winning with AI.",
                'urgency': "The AI opportunity window is closing fast."
            }
        
        # CTA based on affiliate inclusion
        if include_affiliate:
            content_data['cta'] = "📚 Master AI strategies: https://amzn.to/ai-advantage\n\n#AI #Automation #WealthyRobot"
            content_data['affiliate_link'] = "https://amzn.to/ai-advantage"
        else:
            content_data['cta'] = "What's your AI experience? Share below! 👇\n\n#AI #Automation #WealthyRobot"
            content_data['affiliate_link'] = ""
        
        return template.format(**content_data)
    
    def check_visual_integration(self):
        """Check if we should include visual content"""
        # Check for recent visual content files
        visual_files = []
        for file in os.listdir('.'):
            if any(term in file for term in ['graphic', 'infographic', 'visual', 'image']):
                if file.endswith(('.png', '.jpg', '.json')):
                    visual_files.append(file)
        
        return len(visual_files) > 0
    
    def post_coordinated_content(self):
        """Master posting coordination - single source of truth"""
        
        # Check timing constraints
        now = datetime.now()
        
        # Reset daily counter
        if now.date() > self.daily_reset:
            self.daily_posts = 0
            self.daily_reset = now.date()
        
        # Check daily limits
        if self.daily_posts >= 12:  # Conservative daily limit
            return False, "Daily posting limit reached"
        
        # Check time between posts
        if self.last_post_time:
            time_diff = (now - self.last_post_time).total_seconds()
            if time_diff < 7200:  # 2 hours minimum
                return False, f"Must wait {(7200 - time_diff)/60:.0f} more minutes"
        
        # Get CEO decision
        content_type, include_affiliate = self.get_ceo_decision()
        
        # Generate content
        content = self.generate_viral_content(content_type, include_affiliate)
        
        # Check for visual integration
        has_visuals = self.check_visual_integration()
        
        # Post safely
        success, message = safe_twitter_post(content, f"Master_Controller_{content_type}")
        
        if success:
            self.last_post_time = now
            self.daily_posts += 1
            
            # Log the decision
            log_entry = {
                'timestamp': now.isoformat(),
                'content_type': content_type,
                'include_affiliate': include_affiliate,
                'has_visuals': has_visuals,
                'daily_count': self.daily_posts,
                'success': True
            }
            
            with open('master_twitter_log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            print(f"✅ Posted {content_type} content (affiliate: {include_affiliate})")
            return True, content
        else:
            print(f"❌ Posting failed: {message}")
            return False, content

if __name__ == "__main__":
    controller = MasterTwitterController()
    success, content = controller.post_coordinated_content()
    
    if success:
        print("\n📝 Content posted:")
        print("-" * 50)
        print(content)
        print("-" * 50)
    else:
        print(f"Posting status: {content}")
