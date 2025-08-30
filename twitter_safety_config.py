#!/usr/bin/env python3
"""
Master Twitter Safety Configuration
Prevents API freezes across your entire empire
"""

import os
import time

# SAFE POSTING LIMITS (Conservative)
SAFE_LIMITS = {
    "posts_per_hour": 10,        # Well under Twitter's limits
    "posts_per_3_hours": 50,     # Well under 300 limit
    "min_seconds_between_posts": 60,  # 1 minute minimum
    "retry_wait_seconds": 300,   # 5 minutes on 429 error
    "max_retries": 3
}

# POSTING SCHEDULE (Safe times)
SAFE_POSTING_TIMES = [9, 13, 17, 21]  # 4x daily max

# REQUIRED ERROR HANDLING
def handle_twitter_error(error_code, error_message):
    """Standard error handling for all Twitter agents"""
    if error_code == 429:
        print(f"🚨 Rate limited - waiting {SAFE_LIMITS['retry_wait_seconds']} seconds")
        time.sleep(SAFE_LIMITS['retry_wait_seconds'])
        return True
    else:
        print(f"❌ Twitter error {error_code}: {error_message}")
        return False

# SAFE POSTING WRAPPER
def safe_twitter_post(content, agent_name="Unknown"):
    """Post a tweet safely. Honors TWITTER_DRY_RUN=1 to simulate posting."""
    if os.getenv("TWITTER_DRY_RUN", "1") == "1":
        fake_id = f"dryrun-{int(time.time())}"
        print(f"🧪 DRY RUN - {agent_name}: would post tweet: {content[:70]}…")
        return True, f"Success (dry run) - Tweet ID: {fake_id}"

    # Real posting path
    from twitter_api_working import TwitterAPIWorking
    twitter = TwitterAPIWorking()
    success, message = twitter.safe_post_tweet(content)
    print(f"🐦 {agent_name}: {message}")
    return success, message

if __name__ == "__main__":
    print("🛡️ Twitter Safety Configuration Loaded")
    print(f"📊 Safe limits: {SAFE_LIMITS}")
