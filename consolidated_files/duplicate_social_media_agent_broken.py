#!/usr/bin/env python3
"""
CLEAN Social Media Agent - Fixed all syntax errors
Posts to Twitter with proper error handling
"""

import os
import json
import time
from datetime import datetime
import random

class SocialMediaAgent:
    def __init__(self):
        """Initialize social media agent with Twitter API"""
        try:
            # Import Twitter safety module
            from twitter_safety_config import safe_twitter_post
            self.safe_post = safe_twitter_post
            print("✅ Twitter safety config loaded")
            self.posts_sent = 0
            
        except Exception as e:
            print(f"❌ Failed to initialize Twitter API: {e}")
            self.safe_post = None
    
    def post_tweet(self, content):
        """Post a tweet to Twitter with safety measures"""
        try:
            if not self.safe_post:
                print("❌ Twitter API not available")
                return {"status": "error", "error": "API not available"}
            
            print(f"🐦 Posting tweet: {content[:50]}...")
            
            # Use the safe posting function
            result = self.safe_post(content)
            
            if result:
                self.posts_sent += 1
                print(f"✅ Tweet posted successfully!")
                time.sleep(60)  # Safety: 1 minute between posts
                
                return {
                    "status": "success",
                    "posts_sent": self.posts_sent,
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"status": "error", "error": "Post failed"}
                
        except Exception as e:
            print(f"❌ Failed to post tweet: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_latest_content(self):
        """Get the latest content to post"""
        try:
            # Look for recent content files
            content_files = []
            for file in os.listdir('.'):
                if file.startswith('smart_viral_thread_') and file.endswith('.txt'):
                    content_files.append(file)
            
            if content_files:
                # Get the most recent file
                latest_file = max(content_files, key=os.path.getctime)
                
                with open(latest_file, 'r') as f:
                    content = f.read()
                
                print(f"📄 Found content: {latest_file}")
                return content
            else:
                print("📝 No content files found")
                return self.get_fallback_content()
                
        except Exception as e:
            print(f"❌ Error getting content: {e}")
            return self.get_fallback_content()
    
    def get_fallback_content(self):
        """Fallback content when no files available"""
        fallback_tweets = [
            "🤖 AI automation is transforming how entrepreneurs scale their businesses. What's your biggest automation challenge?",
            "💡 The secret to passive income? Automate the right processes at the right time. Here's what most people get wrong...",
            "🚀 Building wealth with AI: Start with one automated workflow, then compound the results. Which process should you automate first?",
            "📚 Every successful entrepreneur I know has one thing in common: they systematize everything. AI just makes it 10x faster."
        ]
        
        return random.choice(fallback_tweets)
    
    def run_cycle(self):
        """Main posting cycle"""
        try:
            print("🐦 Social Media Agent: Starting posting cycle...")
            
            # Get content to post
            content = self.get_latest_content()
            
            if content:
                # Post the content
                result = self.post_tweet(content)
                print("✅ Social media cycle complete!")
                return result
            else:
                print("❌ No content available for posting")
                return {"status": "error", "error": "No content"}
                
        except Exception as e:
            print(f"❌ Cycle error: {e}")
            return {"status": "error", "error": str(e)}

def main():
    """Test the social media agent"""
    agent = SocialMediaAgent()
    result = agent.run_cycle()
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
