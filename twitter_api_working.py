#!/usr/bin/env python3
"""
Working Twitter API with Tweepy - Fixes OAuth signature issues
"""
import os
import time
import tweepy
from datetime import datetime, timedelta

class TwitterAPIWorking:
    def __init__(self):
        # Load credentials
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET') 
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        
        # Rate limiting
        self.last_post_time = None
        self.posts_in_hour = 0
        self.posts_in_3hours = 0
        self.hour_reset_time = datetime.now() + timedelta(hours=1)
        self.three_hour_reset_time = datetime.now() + timedelta(hours=3)
        
        try:
            # Initialize Tweepy client (handles OAuth automatically)
            self.client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_secret,
                wait_on_rate_limit=True
            )
            print("✅ Twitter client initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize Twitter client: {e}")
            self.client = None
    
    def safe_post_tweet(self, text):
        """Post tweet with working OAuth via Tweepy"""
        if not self.client:
            return False, "Twitter client not initialized"
            
        print(f"🐦 Attempting to post tweet...")
        
        # Rate limiting checks
        now = datetime.now()
        if now > self.hour_reset_time:
            self.posts_in_hour = 0
            self.hour_reset_time = now + timedelta(hours=1)
            
        if now > self.three_hour_reset_time:
            self.posts_in_3hours = 0
            self.three_hour_reset_time = now + timedelta(hours=3)
            
        if self.posts_in_3hours >= 290:
            wait_time = (self.three_hour_reset_time - now).total_seconds()
            return False, f"3-hour limit reached. Wait {wait_time/60:.1f} minutes"
            
        if self.posts_in_hour >= 30:
            wait_time = (self.hour_reset_time - now).total_seconds()
            return False, f"Hourly limit reached. Wait {wait_time/60:.1f} minutes"
            
        if self.last_post_time:
            time_since_last = (now - self.last_post_time).total_seconds()
            if time_since_last < 60:
                wait_needed = 60 - time_since_last
                print(f"⏳ Waiting {wait_needed:.1f} seconds...")
                time.sleep(wait_needed)
        
        # Attempt to post
        try:
            response = self.client.create_tweet(text=text)
            
            # Success!
            self.posts_in_hour += 1
            self.posts_in_3hours += 1
            self.last_post_time = datetime.now()
            
            tweet_id = response.data['id']
            print(f"✅ Tweet posted successfully! ID: {tweet_id}")
            return True, f"Success - Tweet ID: {tweet_id}"
            
        except tweepy.Unauthorized as e:
            print(f"🚨 401 Unauthorized: {e}")
            return False, f"Authentication failed: {e}"
            
        except tweepy.Forbidden as e:
            print(f"🚨 403 Forbidden: {e}")
            return False, f"Permission denied: {e}"
            
        except tweepy.TooManyRequests as e:
            print(f"🚨 429 Rate Limited: {e}")
            return False, f"Rate limited: {e}"
            
        except Exception as e:
            print(f"❌ Error posting tweet: {e}")
            return False, str(e)

if __name__ == "__main__":
    # Test the working API
    twitter = TwitterAPIWorking()
    if twitter.client:
        print("🧪 Twitter API ready for testing")
    else:
        print("❌ Twitter API initialization failed")
