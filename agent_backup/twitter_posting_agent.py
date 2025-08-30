import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class TwitterPostingAgent:
    def __init__(self):
        """Initialize Twitter API connection"""
        print("🐦 Twitter Posting Agent: Initializing API connection...")
        
        # Set up Twitter API credentials
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # Initialize Twitter API v2
        try:
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_secret,
                wait_on_rate_limit=True
            )
            
            # Test connection
            me = self.client.get_me()
            print(f"✅ Connected to Twitter as: @{me.data.username}")
            self.posts_sent = 0
            
        except Exception as e:
            print(f"❌ Twitter API connection failed: {e}")
            self.client = None
    
    def post_tweet(self, content):
        """Post a tweet to Twitter"""
        if not self.client:
            print("❌ Twitter API not connected")
            return {"status": "error", "error": "API not connected"}
        
        try:
            # Ensure content fits Twitter's character limit
            if len(content) > 280:
                content = content[:277] + "..."
            
            print(f"🐦 Posting tweet: {content[:50]}...")
            
            # Post the tweet
            response = self.client.create_tweet(text=content)
            self.posts_sent += 1
            
            print(f"✅ Tweet posted successfully!")
            print(f"🔗 Tweet ID: {response.data['id']}")
            print(f"📊 Total tweets sent: {self.posts_sent}")
            
            return {
                "status": "success",
                "tweet_id": response.data['id'],
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Failed to post tweet: {e}")
            return {"status": "error", "error": str(e)}
    
    def post_thread(self, thread_content):
        """Post a Twitter thread"""
        if not self.client:
            print("❌ Twitter API not connected")
            return {"status": "error", "error": "API not connected"}
        
        print("🧵 Posting Twitter thread...")
        
        # Split content into individual tweets
        tweets = []
        if isinstance(thread_content, str):
            # Split by numbered lines (1/, 2/, etc.)
            lines = thread_content.split('\n')
            current_tweet = ""
            
            for line in lines:
                if line.strip() and ('/' in line[:5] or len(current_tweet) > 200):
                    if current_tweet.strip():
                        tweets.append(current_tweet.strip())
                    current_tweet = line
                else:
                    current_tweet += "\n" + line
            
            if current_tweet.strip():
                tweets.append(current_tweet.strip())
        else:
            tweets = thread_content
        
        # Post thread
        posted_tweets = []
        reply_to = None
        
        try:
            for i, tweet in enumerate(tweets[:10]):  # Max 10 tweets per thread
                if len(tweet) > 280:
                    tweet = tweet[:277] + "..."
                
                print(f"🐦 Posting tweet {i+1}/{len(tweets)}: {tweet[:30]}...")
                
                if reply_to:
                    response = self.client.create_tweet(
                        text=tweet,
                        in_reply_to_tweet_id=reply_to
                    )
                else:
                    response = self.client.create_tweet(text=tweet)
                
                reply_to = response.data['id']
                posted_tweets.append({
                    "tweet_id": response.data['id'],
                    "content": tweet
                })
                
                self.posts_sent += 1
            
            print(f"✅ Thread posted successfully! {len(posted_tweets)} tweets")
            print(f"📊 Total tweets sent: {self.posts_sent}")
            
            return {
                "status": "success",
                "thread_id": posted_tweets[0]["tweet_id"],
                "tweets_posted": len(posted_tweets),
                "tweets": posted_tweets
            }
            
        except Exception as e:
            print(f"❌ Failed to post thread: {e}")
            return {"status": "error", "error": str(e), "partial_posts": posted_tweets}
    
    def run_cycle(self):
        """Main cycle - post latest content"""
        print("🐦 Twitter Posting Agent: Looking for content to post...")
        
        # Look for latest viral thread from money agent
        import glob
        thread_files = glob.glob("smart_viral_thread_*.txt")
        
        if thread_files:
            latest_file = sorted(thread_files)[-1]
            print(f"📄 Found content: {latest_file}")
            
            with open(latest_file, 'r') as f:
                content = f.read()
            
            # Extract the thread part
            if "YOUR VIRAL THREAD" in content:
                thread_start = content.find("YOUR VIRAL THREAD")
                thread_content = content[thread_start:].split("============================================================")[0]
                
                return self.post_thread(thread_content)
            else:
                # Post as single tweet
                preview = content[:200] + "..." if len(content) > 200 else content
                return self.post_tweet(preview)
        else:
            print("📄 No content found to post")
            return {"status": "no_content"}

if __name__ == "__main__":
    agent = TwitterPostingAgent()
    if agent.client:
        result = agent.run_cycle()
        print(f"Twitter result: {result.get('status', 'unknown')}")
