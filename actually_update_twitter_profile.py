import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterProfileUpdater:
    def __init__(self):
        print("🐦 TWITTER PROFILE UPDATER - Actually changing @WealthyRobot...")
        
        # Initialize Twitter API v1.1 (needed for profile updates)
        try:
            auth = tweepy.OAuthHandler(
                os.getenv('TWITTER_API_KEY'),
                os.getenv('TWITTER_API_SECRET')
            )
            auth.set_access_token(
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_SECRET')
            )
            
            self.api_v1 = tweepy.API(auth)
            
            # Test connection
            me = self.api_v1.verify_credentials()
            print(f"✅ Connected to Twitter as: @{me.screen_name}")
            self.connected = True
            
        except Exception as e:
            print(f"❌ Twitter API connection failed: {e}")
            self.connected = False
    
    def update_profile_bio(self):
        """Actually update the Twitter bio"""
        if not self.connected:
            print("❌ Can't update - not connected to Twitter")
            return False
        
        new_bio = "🤖 AI Business Automation Expert | 💰 Generating $165+ daily with autonomous agents | 🚀 Building wealth through smart automation | Transparent affiliate links ⬇️"
        
        try:
            print("📝 Updating Twitter bio...")
            self.api_v1.update_profile(description=new_bio)
            print("✅ Twitter bio updated successfully!")
            print(f"📄 New bio: {new_bio}")
            return True
            
        except Exception as e:
            print(f"❌ Bio update failed: {e}")
            return False
    
    def update_profile_name(self):
        """Update the display name"""
        if not self.connected:
            return False
            
        new_name = "WealthyRobot 🤖💰"
        
        try:
            print("📝 Updating display name...")
            self.api_v1.update_profile(name=new_name)
            print("✅ Display name updated!")
            print(f"👤 New name: {new_name}")
            return True
            
        except Exception as e:
            print(f"❌ Name update failed: {e}")
            return False
    
    def update_profile_location(self):
        """Update the location field"""
        if not self.connected:
            return False
            
        new_location = "🌐 Autonomous AI Empire"
        
        try:
            print("📍 Updating location...")
            self.api_v1.update_profile(location=new_location)
            print("✅ Location updated!")
            print(f"📍 New location: {new_location}")
            return True
            
        except Exception as e:
            print(f"❌ Location update failed: {e}")
            return False
    
    def create_pinned_tweet(self):
        """Create and pin a branded tweet"""
        if not self.connected:
            return False
        
        pinned_tweet_content = """🧵 THREAD: How I built an autonomous AI business generating $165+ daily

1/ Started with zero automation knowledge 6 months ago
2/ Built 20+ AI agents working together 24/7
3/ Now earning while I sleep through smart automation

Full breakdown of my system below 👇

#AIBusiness #Automation #PassiveIncome"""

        try:
            print("📌 Creating pinned tweet...")
            
            # Post the tweet
            tweet = self.api_v1.update_status(pinned_tweet_content)
            tweet_id = tweet.id
            
            print(f"✅ Tweet created with ID: {tweet_id}")
            
            # Pin the tweet (Note: Pinning requires manual action or Twitter API v2)
            print("📌 Tweet created! You'll need to manually pin it:")
            print("1. Go to https://twitter.com/WealthyRobot")
            print(f"2. Find the tweet that starts with '🧵 THREAD: How I built...'")
            print("3. Click the 3 dots and select 'Pin to profile'")
            
            return True
            
        except Exception as e:
            print(f"❌ Tweet creation failed: {e}")
            return False
    
    def update_complete_profile(self):
        """Update the complete profile"""
        print("🚀 UPDATING COMPLETE @WealthyRobot PROFILE...")
        print("=" * 50)
        
        results = {
            'bio_updated': self.update_profile_bio(),
            'name_updated': self.update_profile_name(),
            'location_updated': self.update_profile_location(),
            'pinned_tweet_created': self.create_pinned_tweet()
        }
        
        successful_updates = sum(results.values())
        total_updates = len(results)
        
        print(f"\n📊 PROFILE UPDATE RESULTS:")
        print(f"✅ Successfully updated: {successful_updates}/{total_updates} elements")
        
        for update, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {update.replace('_', ' ').title()}")
        
        if successful_updates > 0:
            print(f"\n🎯 Your @WealthyRobot profile has been updated!")
            print("🐦 Check: https://twitter.com/WealthyRobot")
        
        return results

if __name__ == "__main__":
    updater = TwitterProfileUpdater()
    
    if updater.connected:
        results = updater.update_complete_profile()
    else:
        print("❌ Cannot update profile - Twitter API connection failed")
        print("💡 You can update manually at: https://twitter.com/settings/profile")
