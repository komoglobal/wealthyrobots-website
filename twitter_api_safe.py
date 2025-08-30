#!/usr/bin/env python3
"""
Twitter API Safe Wrapper - Prevents API freezes
Handles all rate limiting, 429 errors, and safe posting
"""
import time
import requests
import random
from datetime import datetime, timedelta

class TwitterAPISafe:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.last_post_time = None
        self.posts_in_hour = 0
        self.posts_in_3hours = 0
        self.hour_reset_time = datetime.now() + timedelta(hours=1)
        self.three_hour_reset_time = datetime.now() + timedelta(hours=3)
        self.min_delay_between_posts = 30  # 30 seconds minimum
        
    def safe_post_tweet(self, text):
        """Safely post a tweet with full rate limit protection"""
        print(f"🐦 Attempting to post tweet...")
        
        # Check if we need to reset counters
        now = datetime.now()
        if now > self.hour_reset_time:
            self.posts_in_hour = 0
            self.hour_reset_time = now + timedelta(hours=1)
            
        if now > self.three_hour_reset_time:
            self.posts_in_3hours = 0
            self.three_hour_reset_time = now + timedelta(hours=3)
        
        # Check 3-hour limit (Twitter's hardest limit)
        if self.posts_in_3hours >= 290:  # Stay under 300 limit
            wait_time = (self.three_hour_reset_time - now).total_seconds()
            print(f"⏳ Hit 3-hour limit. Waiting {wait_time/60:.1f} minutes...")
            return False, "3-hour limit reached"
        
        # Check hourly limit (be conservative)
        if self.posts_in_hour >= 30:  # Conservative hourly limit
            wait_time = (self.hour_reset_time - now).total_seconds()
            print(f"⏳ Hit hourly limit. Waiting {wait_time/60:.1f} minutes...")
            return False, "Hourly limit reached"
        
        # Check minimum delay between posts
        if self.last_post_time:
            time_since_last = (now - self.last_post_time).total_seconds()
            if time_since_last < self.min_delay_between_posts:
                wait_needed = self.min_delay_between_posts - time_since_last
                print(f"⏳ Waiting {wait_needed:.1f} seconds between posts...")
                time.sleep(wait_needed)
        
        # Attempt to post with retry logic
        for attempt in range(3):
            try:
                response = self._make_twitter_request(text)
                
                if response.status_code == 201:  # Success
                    self.posts_in_hour += 1
                    self.posts_in_3hours += 1
                    self.last_post_time = datetime.now()
                    print(f"✅ Tweet posted successfully!")
                    return True, "Success"
                
                elif response.status_code == 429:  # Rate limited
                    print(f"🚨 429 Rate Limited - backing off...")
                    wait_time = 2 ** attempt * 60  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                
                else:
                    print(f"❌ Twitter API error: {response.status_code}")
                    return False, f"API error: {response.status_code}"
                    
            except Exception as e:
                print(f"❌ Exception posting tweet: {e}")
                if attempt < 2:
                    time.sleep(10 * (attempt + 1))  # Wait before retry
                    continue
                return False, str(e)
        
        return False, "Max retries exceeded"
    
    def _make_twitter_request(self, text):
        """Make actual Twitter API request"""
        url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        data = {"text": text}
        
        return requests.post(url, headers=headers, json=data, timeout=30)
    
    def get_posting_stats(self):
        """Get current posting statistics"""
        return {
            "posts_in_hour": self.posts_in_hour,
            "posts_in_3hours": self.posts_in_3hours,
            "next_hour_reset": self.hour_reset_time.isoformat(),
            "next_3hour_reset": self.three_hour_reset_time.isoformat(),
            "last_post": self.last_post_time.isoformat() if self.last_post_time else None
        }

# Usage example for your agents
if __name__ == "__main__":
    # Example usage
    twitter = TwitterAPISafe("your_bearer_token_here")
    
    # Safe posting
    success, message = twitter.safe_post_tweet("Test tweet from safe wrapper!")
    print(f"Result: {success} - {message}")
    
    # Check stats
    stats = twitter.get_posting_stats()
    print(f"Stats: {stats}")
