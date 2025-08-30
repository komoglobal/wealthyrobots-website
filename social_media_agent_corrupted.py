
# DEPRECATED: This agent has been merged into consolidated_agent
# Please use consolidated_agent instead
# This file will be removed in future updates

# DEPRECATED: This agent has been merged into smart_affiliate_agent.py
# Please use smart_affiliate_agent.py instead
# This file will be removed in future updates

# DEPRECATED: This agent has been merged into smart_affiliate_agent.py
# Please use smart_affiliate_agent.py instead
# This file will be removed in future updates

# DEPRECATED: This agent has been merged into visual_affiliate_agent.py
# Please use visual_affiliate_agent.py instead
# This file will be removed in future updates

# DEPRECATED: This agent has been merged into visual_affiliate_agent.py
# Please use visual_affiliate_agent.py instead
# This file will be removed in future updates

# DEPRECATED: This agent has been merged into visual_affiliate_agent.py
# Please use visual_affiliate_agent.py instead
# This file will be removed in future updates

# DEPRECATED: This agent has been merged into consolidated_agent
# Please use consolidated_agent instead
# This file will be removed in future updates
import time
from twitter_api_safe import TwitterAPISafe
"""
EMPIRE_AGENT_INFO:
NAME: Social Media Agent
PURPOSE: Posts educational threads to Twitter with professional graphics and affiliate links
CATEGORY: Content & Social Media
STATUS: Active
FREQUENCY: On-demand
"""


import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SocialMediaAgent:
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
        time.sleep(60)  # Safety: 1 minute between posts
        except Exception as e:
            print(f"Error in social media agent: {e}")
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
            response = self.twitter_safe.safe_post_tweet(tweet_text)
            time.sleep(60)  # Safety: 1 minute between posts
        except Exception as e:
            print(f"Error in social media agent: {e}")
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
        """Post proper Twitter thread - SEPARATE tweets"""
        if not self.client:
            print("❌ Twitter API not connected")
            return {"status": "error", "error": "API not connected"}
        
        print("🧵 Creating REAL Twitter thread (separate tweets)...")
        
        # Extract individual tweets
        tweets = []
        if isinstance(thread_content, str):
            # Split by TWEET markers
            parts = thread_content.split('TWEET ')
            for part in parts[1:]:  # Skip first empty part
                if ':' in part:
                    # Get content after the colon, clean it up
                    tweet_text = part.split(':', 1)[1].strip()
                    # Take first meaningful line only
                    lines = tweet_text.split('\n')
                    clean_tweet = lines[0].strip()
                    if clean_tweet and len(clean_tweet) > 10:
                        tweets.append(clean_tweet[:280])  # Twitter limit
        
        if not tweets:
            print("⚠️ No valid tweets found, posting as single tweet")
            clean_content = thread_content.replace('TWEET 1:', '').replace('TWEET 2:', '').strip()
            return self.post_single_tweet(clean_content[:280])
        
        print(f"📝 Posting {len(tweets)} SEPARATE tweets as thread...")
        
        try:
            # Post first tweet
            first_response = self.twitter_safe.safe_post_tweet(tweet_text)
        time.sleep(60)  # Safety: 1 minute between posts
        except Exception as e:
            print(f"Error in social media agent: {e}")
            first_id = first_response.data['id']
            print(f"✅ Tweet 1/{len(tweets)}: {tweets[0][:50]}...")
            
            # Post replies to create thread
            previous_id = first_id
            for i, tweet in enumerate(tweets[1:], 2):
                reply_response = self.twitter_safe.safe_post_tweet(tweet_text)
        time.sleep(60)  # Safety: 1 minute between posts
                previous_id = reply_response.data['id']
                print(f"✅ Tweet {i}/{len(tweets)}: {tweet[:50]}...")
            
            return {"status": "success", "thread_length": len(tweets), "method": "proper_threading"}
            
        except Exception as e:
            print(f"❌ Threading error: {e}")
            return {"status": "error", "error": str(e)}
    
    def post_single_tweet(self, text):
        """Fallback single tweet method"""
        try:
            response = self.twitter_safe.safe_post_tweet(tweet_text)
        time.sleep(60)  # Safety: 1 minute between posts
        except Exception as e:
            print(f"Error in social media agent: {e}")
            return {"status": "success", "single_tweet": True}
        except Exception as e:
            return {"status": "error", "error": str(e)}
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
        time.sleep(60)  # Safety: 1 minute between posts
        else:
            print("📄 No content found to post")
            return {"status": "no_content"}


    
    
    
    def create_smart_affiliate_tweets(self, thread_content):
        """Create tweets with smart affiliate link placement"""
        affiliate_links = self.extract_affiliate_links(thread_content)
        
        if not affiliate_links:
            return thread_content
            
        link = affiliate_links[0]
        
        # Strategy: Create dedicated affiliate tweets instead of adding to existing ones
        if "COPY/PASTE THESE TWEETS" in thread_content:
            tweets_section = thread_content.split("COPY/PASTE THESE TWEETS")[1]
            
            # Create affiliate CTA tweets
            affiliate_tweet_1 = f"💰 Get 'The AI Advantage' (8% edge): {link}"
            affiliate_tweet_2 = f"🔗 Ready to dominate AI in 2025? Start here: {link}"
            
            # Add affiliate tweets strategically in the thread
            enhanced_content = f"""🎨 VISUAL THREAD WITH PROFESSIONAL GRAPHICS 🎨

{tweets_section}

{affiliate_tweet_1}

{affiliate_tweet_2}

🎯 Don't miss out - limited time pricing!"""
            
            return enhanced_content
        
        return thread_content

    def extract_affiliate_links(self, thread_content):
        """Extract real affiliate links from thread content"""
        import re
        
        links = []
        # Find all Amazon affiliate links
        amazon_pattern = r'https://amazon\.com/dp/[A-Z0-9]+\?tag=wealthyrobot-20'
        found_links = re.findall(amazon_pattern, thread_content)
        
        if found_links:
            print(f"💰 Found {len(found_links)} real affiliate links")
            return found_links
        else:
            print("⚠️ No real affiliate links found in content")
            return []
    
    def clean_tweet_content(self, tweet_text):
        """Clean and ensure tweet fits Twitter limits"""
        # Remove extra whitespace and formatting
        clean_text = ' '.join(tweet_text.split())
        
        # If too long, truncate smartly
        if len(clean_text) > 280:
            clean_text = clean_text[:270] + "..."
            
        return clean_text
    
    def enhance_tweets_with_links(self, tweet_content, affiliate_links):
        """Add affiliate links to appropriate tweets"""
        if not affiliate_links:
            return tweet_content
            
        # Add the first affiliate link to relevant tweets
        link = affiliate_links[0]
        
        # If tweet mentions the product, add the link
        if 'AI Advantage' in tweet_content and len(tweet_content) + len(link) + 5 < 280:
            return tweet_content + f" {link}"
        
        return tweet_content

    
    def upload_media(self, image_path):
        """Upload media to Twitter"""
        try:
            import tweepy
            
            # Use the API v1.1 for media upload (more reliable)
            auth = tweepy.OAuth1UserHandler(
                self.api_key, self.api_secret,
                self.access_token, self.access_secret
            )
            api = tweepy.API(auth)
            
            # Upload the media
            media = api.media_upload(image_path)
            print(f"✅ Media uploaded: {media.media_id}")
            return media.media_id
            
        except Exception as e:
            print(f"❌ Media upload failed: {e}")
            return None
    
    def post_tweet_with_image(self, text, image_path):
        time.sleep(60)  # Safety: 1 minute between posts
        except Exception as e:
            print(f"Error in social media agent: {e}")
        """Post a single tweet with an image"""
        try:
            # Upload the image first
            media_id = self.upload_media(image_path)
            
            if media_id:
                # Post tweet with media
                response = self.twitter_safe.safe_post_tweet(tweet_text)
        time.sleep(60)  # Safety: 1 minute between posts
        except Exception as e:
            print(f"Error in social media agent: {e}")
                print(f"✅ Tweet with image posted: {response.data['id']}")
                return response
            else:
                # Fallback to text-only
                return self.post_tweet(text)
        time.sleep(60)  # Safety: 1 minute between posts
                
        except Exception as e:
            print(f"❌ Tweet with image failed: {e}")
            return self.post_tweet(text)
        time.sleep(60)  # Safety: 1 minute between posts
    
    def post_thread_with_real_images(self, thread_content):
        """Post thread with actual images attached"""
        try:
            import glob
            import os
            
            # Find available images
            images = []
            for pattern in ['quote_card_203410.png', 'graphic_ai_business_203409.png', 'stats_infographic_203409.png']:
                found = glob.glob(pattern)
                images.extend(found)
            
            print(f"🖼️ Found {len(images)} images for upload")
            
            if images and len(images) >= 1:
                # Use smart affiliate integration
                enhanced_content = self.create_smart_affiliate_tweets(thread_content)
                
                # Split into tweets
                tweets = self.split_into_tweets(enhanced_content)
                
                if tweets:
                    # Post first tweet with image
                    first_image = images[0]
                    print(f"📸 Posting first tweet with image: {first_image}")
                    
                    first_response = self.post_tweet_with_image(tweets[0], first_image)
        time.sleep(60)  # Safety: 1 minute between posts
        except Exception as e:
            print(f"Error in social media agent: {e}")
                    if not first_response:
                        return {"status": "error", "error": "Failed to post first tweet"}
                    
                    previous_tweet_id = first_response.data['id']
                    posted_count = 1
                    
                    # Post remaining tweets as replies
                    for i, tweet in enumerate(tweets[1:], 1):
                        try:
                            # Add image to strategic tweets (e.g., affiliate CTAs)
                            use_image = None
                            if ('💰 Get' in tweet or '🔗 Ready' in tweet) and i-1 < len(images):
                                use_image = images[min(i-1, len(images)-1)]
                            
                            if use_image:
                                response = self.post_tweet_with_image(tweet, use_image)
        time.sleep(60)  # Safety: 1 minute between posts
                        except Exception as e:
                            print(f"Error in social media agent: {e}")
                            else:
                                response = self.twitter_safe.safe_post_tweet(tweet_text)
        time.sleep(60)  # Safety: 1 minute between posts
                            
                            if response:
                                previous_tweet_id = response.data['id']
                                posted_count += 1
                                print(f"🐦 Posted tweet {posted_count}")
                            
                        except Exception as e:
                            print(f"❌ Error posting tweet {i}: {e}")
                            break
                    
                    return {"status": "success", "tweets_posted": posted_count}
                
            else:
                print("📝 No images found, using text-only posting")
                return self.post_thread_with_visuals(thread_content)
                
        except Exception as e:
            print(f"❌ Image posting error: {e}")
            return self.post_thread_with_visuals(thread_content)
    
    def split_into_tweets(self, content):
        """Split content into individual tweets"""
        tweets = []
        lines = content.split('\n')
        current_tweet = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this starts a new tweet or is a continuation
            if len(current_tweet) + len(line) + 1 > 280:
                if current_tweet:
                    tweets.append(current_tweet.strip())
                current_tweet = line
            else:
                current_tweet += ("\n" if current_tweet else "") + line
        
        if current_tweet:
            tweets.append(current_tweet.strip())
            
        return tweets

    def post_thread_with_visuals(self, thread_content):
        """Enhanced thread posting with visual assets"""
        try:
            print("🎨 Preparing visual thread posting...")
            
            # Check for available visual assets
            import glob
            import os
            
            images = []
            for pattern in ['quote_card_203410.png', 'graphic_ai_business_203409.png', 'stats_infographic_203409.png']:
                found = glob.glob(pattern)
                images.extend(found)
            
            print(f"🖼️ Found {len(images)} visual assets: {[os.path.basename(img) for img in images]}")
            
            if images:
                print("📝 Note: Image upload requires Twitter API v2 media endpoint")
                print("🔄 Posting text content for now (images ready for manual posting)")
                
                # Use smart affiliate link integration
                enhanced_content = self.create_smart_affiliate_tweets(thread_content)
                return self.post_thread(enhanced_content)
            else:
                print("📝 No visual assets found, posting standard content")
                return self.post_thread(thread_content)
                
        except Exception as e:
            print(f"❌ Visual posting error: {e}")
            return self.post_thread(thread_content)

    
    def get_dynamic_content(self):
        """Get content using dynamic selection strategy"""
        try:
            from dynamic_content_selector import DynamicContentSelector
            
            selector = DynamicContentSelector()
            selected_file = selector.get_optimized_content()
            
            print(f"🎯 Dynamic selector chose: {selected_file}")
            
            # Read the selected content
            with open(selected_file, 'r') as f:
                content = f.read()
                
            return content
            
        except Exception as e:
            print(f"❌ Dynamic selection failed: {e}")
            # Fallback to existing method
            return self.get_fallback_content()
            
    def get_fallback_content(self):
        """Fallback content selection method"""
        # Original method: find affiliate threads
        import glob
        import os
        
        threads = []
        for file in glob.glob("smart_viral_thread*.txt"):
            try:
                with open(file, 'r') as f:
                    file_content = f.read()
                    if 'amazon.com' in file_content and 'wealthyrobot-20' in file_content:
                        threads.append(file)
            except:
                continue
        
        if threads:
            latest = max(threads, key=os.path.getctime)
            with open(latest, 'r') as f:
                return f.read()
        
        return "Default AI content thread here..."

    def create_social_media_posts(self, content=None):
        """Orchestrator-compatible method for posting content"""
        try:
            print("📱 Social Media Agent: Creating posts...")
            
            # If no content provided, try to find recent affiliate content
            if not content:
                # Use dynamic content selection
                content = self.get_dynamic_content()
                
            if not content or len(content) < 50:
                import glob
                import os
                
                # Find latest thread with REAL affiliate links
                threads = []
                for file in glob.glob("smart_viral_thread*.txt"):
                    with open(file, 'r') as f:
                        file_content = f.read()
                        if 'amazon.com' in file_content and 'wealthyrobot-20' in file_content:
                            threads.append(file)
                
                if threads:
                    latest = max(threads, key=os.path.getctime)
                    print(f"📝 Using REAL affiliate thread: {latest}")
                    with open(latest, 'r') as f:
                        content = f.read()
                    print(f"📝 Using content from: {latest}")
                else:
                    print("⚠️ No content found to post")
                    return {"status": "no_content"}
            
            # Post using existing post_thread method
            result = self.post_thread_with_real_images(content)
            print("✅ Social media posting complete!")
            return result
            
        except Exception as e:
            print(f"❌ Social media posting error: {e}")
            return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    agent = TwitterPostingAgent()
    if agent.client:
        result = agent.run_cycle()
        print(f"Twitter result: {result.get('status', 'unknown')}")
