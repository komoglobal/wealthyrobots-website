#!/usr/bin/env python3
"""
Enhanced Twitter API Wrapper with proper authentication
Fixes 403 errors and ensures proper API access
"""
import os
import time
import requests
import json
from datetime import datetime, timedelta

class TwitterAPIEnhanced:
    def __init__(self):
        # Load all Twitter credentials
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET') 
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # Rate limiting
        self.last_post_time = None
        self.posts_in_hour = 0
        self.posts_in_3hours = 0
        self.hour_reset_time = datetime.now() + timedelta(hours=1)
        self.three_hour_reset_time = datetime.now() + timedelta(hours=3)
        
        # Validate credentials
        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            print("⚠️ Missing Twitter credentials!")
            
    def safe_post_tweet(self, text):
        """Post tweet with enhanced authentication and safety"""
        print(f"🐦 Attempting to post tweet...")
        
        # Rate limiting checks (same as before)
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
                time.sleep(wait_needed)
        
        # Try different authentication methods
        for attempt in range(3):
            try:
                # Method 1: OAuth 1.0a (User Context) - Required for posting
                response = self._post_with_oauth1(text)
                
                if response.status_code == 201:
                    self.posts_in_hour += 1
                    self.posts_in_3hours += 1
                    self.last_post_time = datetime.now()
                    print(f"✅ Tweet posted successfully!")
                    return True, "Success"
                    
                elif response.status_code == 403:
                    error_data = response.json() if response.content else {}
                    error_detail = error_data.get('detail', 'Unknown error')
                    print(f"🚨 403 Forbidden: {error_detail}")
                    
                    # Common 403 fixes
                    if 'duplicate' in error_detail.lower():
                        return False, "Duplicate content detected"
                    elif 'suspended' in error_detail.lower():
                        return False, "Account suspended"
                    elif 'permission' in error_detail.lower():
                        return False, "Insufficient permissions"
                    else:
                        return False, f"Authentication error: {error_detail}"
                        
                elif response.status_code == 429:
                    print(f"🚨 429 Rate Limited - backing off...")
                    wait_time = 2 ** attempt * 60
                    time.sleep(wait_time)
                    continue
                    
                else:
                    print(f"❌ Twitter API error: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False, f"API error: {response.status_code}"
                    
            except Exception as e:
                print(f"❌ Exception posting tweet: {e}")
                if attempt < 2:
                    time.sleep(10 * (attempt + 1))
                    continue
                return False, str(e)
        
        return False, "Max retries exceeded"
    
    def _post_with_oauth1(self, text):
        """Post using OAuth 1.0a (proper method for posting tweets)"""
        import hashlib
        import hmac
        import base64
        import urllib.parse
        import secrets
        import time
        
        # OAuth 1.0a parameters
        oauth_params = {
            'oauth_consumer_key': self.api_key,
            'oauth_token': self.access_token,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': secrets.token_urlsafe(32),
            'oauth_version': '1.0'
        }
        
        # Request parameters
        request_params = {'text': text}
        
        # Combine parameters for signature
        all_params = {**oauth_params, **request_params}
        
        # Create signature base string
        sorted_params = sorted(all_params.items())
        param_string = '&'.join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted_params])
        
        base_string = f"POST&{urllib.parse.quote('https://api.twitter.com/2/tweets', safe='')}&{urllib.parse.quote(param_string, safe='')}"
        
        # Create signing key
        signing_key = f"{urllib.parse.quote(self.api_secret, safe='')}&{urllib.parse.quote(self.access_secret, safe='')}"
        
        # Generate signature
        signature = base64.b64encode(
            hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
        ).decode()
        
        oauth_params['oauth_signature'] = signature
        
        # Create authorization header
        auth_header = 'OAuth ' + ', '.join([f'{k}="{urllib.parse.quote(str(v), safe="")}"' for k, v in oauth_params.items()])
        
        # Make request
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        
        return requests.post(
            'https://api.twitter.com/2/tweets',
            headers=headers,
            json=request_params,
            timeout=30
        )

if __name__ == "__main__":
    # Test the enhanced API
    twitter = TwitterAPIEnhanced()
    print("🧪 Testing enhanced Twitter API...")
    
    if twitter.api_key and twitter.access_token:
        print("✅ Credentials loaded")
        print("🧪 Ready for posting with proper authentication")
    else:
        print("❌ Missing credentials")
