#!/usr/bin/env python3
"""
Twitter API Monitor - Track usage and prevent freezes
"""
import json
import os
from datetime import datetime, timedelta

class TwitterAPIMonitor:
    def __init__(self):
        self.log_file = "twitter_api_usage.json"
        self.load_usage_log()
    
    def load_usage_log(self):
        """Load existing usage log"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                self.usage_log = json.load(f)
        else:
            self.usage_log = {
                "posts_today": 0,
                "posts_this_hour": 0,
                "last_post_time": None,
                "daily_reset": datetime.now().date().isoformat(),
                "hourly_reset": datetime.now().replace(minute=0, second=0).isoformat()
            }
    
    def can_post_safely(self):
        """Check if it's safe to post"""
        now = datetime.now()
        
        # Check daily limit (conservative: 50 posts per day)
        if self.usage_log["posts_today"] >= 50:
            return False, "Daily limit reached (50 posts)"
        
        # Check hourly limit (conservative: 10 posts per hour)  
        if self.usage_log["posts_this_hour"] >= 10:
            return False, "Hourly limit reached (10 posts)"
        
        # Check minimum time between posts (60 seconds)
        if self.usage_log["last_post_time"]:
            last_post = datetime.fromisoformat(self.usage_log["last_post_time"])
            if (now - last_post).seconds < 60:
                return False, "Must wait 60 seconds between posts"
        
        return True, "Safe to post"
    
    def log_post_attempt(self, success=True):
        """Log a posting attempt"""
        now = datetime.now()
        
        # Reset counters if needed
        if now.date().isoformat() != self.usage_log["daily_reset"]:
            self.usage_log["posts_today"] = 0
            self.usage_log["daily_reset"] = now.date().isoformat()
        
        if now.replace(minute=0, second=0).isoformat() != self.usage_log["hourly_reset"]:
            self.usage_log["posts_this_hour"] = 0
            self.usage_log["hourly_reset"] = now.replace(minute=0, second=0).isoformat()
        
        # Increment counters
        if success:
            self.usage_log["posts_today"] += 1
            self.usage_log["posts_this_hour"] += 1
            self.usage_log["last_post_time"] = now.isoformat()
        
        # Save log
        with open(self.log_file, 'w') as f:
            json.dump(self.usage_log, f, indent=2)
    
    def get_status(self):
        """Get current API usage status"""
        return {
            "posts_today": self.usage_log["posts_today"],
            "posts_this_hour": self.usage_log["posts_this_hour"],
            "daily_limit_remaining": 50 - self.usage_log["posts_today"],
            "hourly_limit_remaining": 10 - self.usage_log["posts_this_hour"],
            "last_post": self.usage_log["last_post_time"]
        }

if __name__ == "__main__":
    monitor = TwitterAPIMonitor()
    print("🛡️ Twitter API Monitor")
    print("=" * 25)
    
    status = monitor.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    can_post, reason = monitor.can_post_safely()
    print(f"\n🚦 Can post now: {can_post}")
    print(f"Reason: {reason}")
