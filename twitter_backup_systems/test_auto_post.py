import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# Create Twitter client
client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    wait_on_rate_limit=True
)

# Test post
try:
    response = client.create_tweet(text="🤖 Testing my automated AI business system! This tweet was posted automatically by my AI agents. #AIAutomation #Testing")
    print(f"✅ Tweet posted successfully!")
    print(f"🔗 https://twitter.com/user/status/{response.data['id']}")
except Exception as e:
    print(f"❌ Error: {e}")
