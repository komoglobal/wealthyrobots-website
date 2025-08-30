#!/usr/bin/env python3
"""
Automated Twitter Revenue Generation - Posts profit-focused content
"""
import time
import random
from datetime import datetime
from twitter_safety_config import safe_twitter_post

# Revenue-focused content templates
REVENUE_TEMPLATES = [
    "🤖 AI automation is creating wealth faster than ever. Here are 5 ways to profit from the AI revolution... 🧵",
    "💰 While others debate AI, smart people are building AI businesses. Here's how to start... 🧵",
    "🚀 The AI gold rush is happening NOW. Don't miss these 5 opportunities... 🧵",
    "⚡ AI tools that can 10x your productivity and income... 🧵",
    "🎯 How to build passive income with AI automation... 🧵"
]

AFFILIATE_PROMOTION = "📚 Master AI: https://amzn.to/ai-advantage #AI #WealthyRobot"

def generate_revenue_post():
    """Generate revenue-focused Twitter content"""
    template = random.choice(REVENUE_TEMPLATES)
    return f"{template}\n\n{AFFILIATE_PROMOTION}"

def run_automated_posting():
    """Run automated revenue posting every 2 hours"""
    print("🤖 AUTOMATED TWITTER REVENUE GENERATOR")
    print("=" * 40)
    
    post_count = 0
    
    while True:
        try:
            # Generate content
            content = generate_revenue_post()
            
            # Post safely
            success, message = safe_twitter_post(content, f"Auto_Revenue_{post_count}")
            
            if success:
                post_count += 1
                print(f"✅ Revenue post #{post_count} successful!")
                print(f"💰 Promoting: The AI Advantage book")
            else:
                print(f"⚠️ Post blocked: {message}")
            
            # Wait 2 hours (7200 seconds) - well within safe limits
            print(f"⏳ Waiting 2 hours until next revenue post...")
            time.sleep(7200)
            
        except KeyboardInterrupt:
            print("\n🛑 Automated posting stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("⏳ Waiting 10 minutes before retry...")
            time.sleep(600)

if __name__ == "__main__":
    run_automated_posting()
