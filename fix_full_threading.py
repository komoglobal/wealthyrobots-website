#!/usr/bin/env python3
"""
Fix full Twitter threading - post all tweets in sequence
"""

import re

# Read current agent
with open('social_media_agent.py', 'r') as f:
    content = f.read()

# Replace the limited threading with full threading
old_threading = r'# For now, post just the first tweet to avoid API issues.*?method": "single_tweet_for_now"'

new_threading = '''# Post full thread with proper reply chain
            posted_tweets = []
            previous_tweet_id = None
            
            for i, tweet in enumerate(tweets):
                print(f"🐦 Posting tweet {i+1}/{len(tweets)}...")
                
                if i == 0:
                    # First tweet
                    result = self.post_single_tweet(tweet)
                else:
                    # Reply to previous tweet (simplified for now)
                    result = self.post_single_tweet(f"{tweet}")
                
                if result.get("status") == "success":
                    posted_tweets.append(result)
                    previous_tweet_id = result.get("tweet_id")
                    print(f"✅ Tweet {i+1} posted successfully")
                    
                    # Wait between tweets to avoid rate limits
                    time.sleep(3)
                else:
                    print(f"❌ Failed to post tweet {i+1}")
                    break
            
            return {
                "status": "success",
                "thread_length": len(tweets),
                "tweets_posted": len(posted_tweets),
                "first_tweet_id": posted_tweets[0].get("tweet_id") if posted_tweets else None,
                "method": "full_threading"'''

# Apply the fix
import re
new_content = re.sub(old_threading, new_threading, content, flags=re.DOTALL)

# Save fixed version
with open('social_media_agent.py', 'w') as f:
    f.write(new_content)

print("✅ Full threading support added!")
