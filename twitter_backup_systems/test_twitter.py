import time
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# Test Twitter connection
try:
    client = tweepy.Client(
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
    )
    
    # Test by posting a tweet
    response = client.create_tweet(text="🤖 My AI business automation system is now live! Testing automated posting... #AI #Automation")
        time.sleep(60)  # Safety: 1 minute between posts
    print("✅ Twitter connection successful!")
    print(f"Tweet posted: https://twitter.com/user/status/{response.data['id']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check your API keys in .env file")
