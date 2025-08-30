#!/usr/bin/env python3
"""
Twitter Visual Verification Agent
Visually checks the @WealthyRobot Twitter page to confirm posts are live and properly formatted
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import base64
from io import BytesIO
from PIL import Image

class TwitterVisualVerifier:
    def __init__(self):
        self.username = "WealthyRobot"
        self.twitter_url = f"https://twitter.com/{self.username}"
        self.driver = None
        self.verification_log = []
        
    def setup_browser(self):
        """Setup headless Chrome browser for Twitter scraping"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"❌ Failed to setup browser: {e}")
            return False
    
    def navigate_to_twitter(self):
        """Navigate to the Twitter profile"""
        try:
            self.driver.get(self.twitter_url)
            time.sleep(3)  # Wait for page load
            
            # Wait for tweets to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
            )
            return True
        except TimeoutException:
            print(f"❌ Timeout loading Twitter page: {self.twitter_url}")
            return False
        except Exception as e:
            print(f"❌ Error navigating to Twitter: {e}")
            return False
    
    def get_recent_tweets(self, count=5):
        """Extract recent tweets and their details"""
        tweets = []
        
        try:
            # Find all tweet elements
            tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            
            for i, tweet_elem in enumerate(tweet_elements[:count]):
                tweet_data = self.analyze_tweet_element(tweet_elem, i)
                if tweet_data:
                    tweets.append(tweet_data)
                    
        except Exception as e:
            print(f"❌ Error extracting tweets: {e}")
            
        return tweets
    
    def analyze_tweet_element(self, tweet_elem, index):
        """Analyze individual tweet element for all components"""
        tweet_data = {
            'index': index,
            'timestamp': None,
            'text_content': None,
            'has_image': False,
            'has_link': False,
            'affiliate_link_found': False,
            'engagement': {},
            'verification_status': 'unknown'
        }
        
        try:
            # Extract tweet text
            text_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            tweet_data['text_content'] = text_elem.text
            
            # Check for images
            try:
                images = tweet_elem.find_elements(By.CSS_SELECTOR, '[data-testid="tweetPhoto"] img')
                tweet_data['has_image'] = len(images) > 0
                tweet_data['image_count'] = len(images)
            except:
                pass
            
            # Check for links
            try:
                links = tweet_elem.find_elements(By.CSS_SELECTOR, 'a[href*="amazon.com"], a[href*="amzn.to"]')
                tweet_data['has_link'] = len(links) > 0
                
                # Check specifically for affiliate links
                for link in links:
                    href = link.get_attribute('href')
                    if 'wealthyrobot-20' in href or 'tag=wealthyrobot-20' in href:
                        tweet_data['affiliate_link_found'] = True
                        break
                        
            except:
                pass
            
            # Extract timestamp
            try:
                time_elem = tweet_elem.find_element(By.CSS_SELECTOR, 'time')
                tweet_data['timestamp'] = time_elem.get_attribute('datetime')
            except:
                pass
            
            # Extract engagement metrics
            try:
                # Replies
                reply_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="reply"]')
                tweet_data['engagement']['replies'] = self.extract_metric_count(reply_elem)
                
                # Retweets
                retweet_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
                tweet_data['engagement']['retweets'] = self.extract_metric_count(retweet_elem)
                
                # Likes
                like_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
                tweet_data['engagement']['likes'] = self.extract_metric_count(like_elem)
                
            except:
                pass
            
            # Determine verification status
            tweet_data['verification_status'] = self.determine_verification_status(tweet_data)
            
        except Exception as e:
            print(f"❌ Error analyzing tweet {index}: {e}")
            
        return tweet_data
    
    def extract_metric_count(self, element):
        """Extract engagement count from element"""
        try:
            count_text = element.get_attribute('aria-label')
            if count_text:
                # Extract number from text like "5 replies" or "12 retweets"
                import re
                numbers = re.findall(r'\d+', count_text)
                return int(numbers[0]) if numbers else 0
        except:
            pass
        return 0
    
    def determine_verification_status(self, tweet_data):
        """Determine if tweet meets all requirements"""
        issues = []
        
        if not tweet_data['text_content']:
            issues.append("No text content")
        
        if not tweet_data['has_image']:
            issues.append("No image attached")
        
        if not tweet_data['has_link']:
            issues.append("No links found")
        
        if tweet_data['has_link'] and not tweet_data['affiliate_link_found']:
            issues.append("Link found but no affiliate tag")
        
        if not issues:
            return "✅ VERIFIED"
        else:
            return f"❌ ISSUES: {', '.join(issues)}"
    
    def take_screenshot(self, filename=None):
        """Take screenshot of current page"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"twitter_verification_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Failed to take screenshot: {e}")
            return None
    
    def verify_latest_posts(self, expected_posts=None):
        """Main verification function"""
        verification_report = {
            'timestamp': datetime.now().isoformat(),
            'twitter_url': self.twitter_url,
            'verification_results': [],
            'overall_status': 'unknown',
            'issues_found': [],
            'recommendations': []
        }
        
        print(f"🔍 Starting visual verification of @{self.username}...")
        
        if not self.setup_browser():
            verification_report['overall_status'] = 'browser_setup_failed'
            return verification_report
        
        try:
            if not self.navigate_to_twitter():
                verification_report['overall_status'] = 'navigation_failed'
                return verification_report
            
            # Take screenshot for record
            screenshot_file = self.take_screenshot()
            verification_report['screenshot'] = screenshot_file
            
            # Get recent tweets
            tweets = self.get_recent_tweets(count=5)
            verification_report['verification_results'] = tweets
            
            # Analyze results
            verified_count = 0
            total_issues = []
            
            for tweet in tweets:
                if "✅ VERIFIED" in tweet['verification_status']:
                    verified_count += 1
                else:
                    issues = tweet['verification_status'].replace("❌ ISSUES: ", "")
                    total_issues.extend(issues.split(", "))
            
            verification_report['verified_posts'] = verified_count
            verification_report['total_posts_checked'] = len(tweets)
            verification_report['issues_found'] = list(set(total_issues))
            
            # Determine overall status
            if verified_count == len(tweets) and len(tweets) > 0:
                verification_report['overall_status'] = '✅ ALL_VERIFIED'
            elif verified_count > 0:
                verification_report['overall_status'] = '⚠️ PARTIAL_VERIFICATION'
            else:
                verification_report['overall_status'] = '❌ VERIFICATION_FAILED'
            
            # Generate recommendations
            verification_report['recommendations'] = self.generate_recommendations(verification_report)
            
        finally:
            if self.driver:
                self.driver.quit()
        
        return verification_report
    
    def generate_recommendations(self, report):
        """Generate actionable recommendations based on verification results"""
        recommendations = []
        
        issues = report.get('issues_found', [])
        
        if 'No image attached' in issues:
            recommendations.append("🖼️ Ensure visual_affiliate_agent.py is running and generating images")
        
        if 'No links found' in issues:
            recommendations.append("🔗 Check that affiliate links are being properly inserted in content")
        
        if 'Link found but no affiliate tag' in issues:
            recommendations.append("💰 Verify affiliate tag 'wealthyrobot-20' is being added to Amazon URLs")
        
        if 'No text content' in issues:
            recommendations.append("📝 Check social_media_agent.py is generating tweet content properly")
        
        if report['verified_posts'] == 0:
            recommendations.append("🚨 URGENT: No posts are properly formatted - check live_orchestrator.py")
        
        return recommendations
    
    def save_verification_report(self, report):
        """Save verification report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"twitter_verification_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📊 Verification report saved: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
            return None
    
    def print_verification_summary(self, report):
        """Print a formatted summary of verification results"""
        print("\n" + "="*60)
        print(f"🔍 TWITTER VERIFICATION REPORT - @{self.username}")
        print("="*60)
        print(f"⏰ Timestamp: {report['timestamp']}")
        print(f"📊 Status: {report['overall_status']}")
        print(f"✅ Verified Posts: {report.get('verified_posts', 0)}/{report.get('total_posts_checked', 0)}")
        
        if report.get('issues_found'):
            print(f"\n❌ Issues Found:")
            for issue in report['issues_found']:
                print(f"   • {issue}")
        
        if report.get('recommendations'):
            print(f"\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"   • {rec}")
        
        print(f"\n📸 Screenshot: {report.get('screenshot', 'Not taken')}")
        
        print("\n📝 Individual Tweet Analysis:")
        for i, tweet in enumerate(report.get('verification_results', [])):
            print(f"\n   Tweet {i+1}:")
            print(f"   Status: {tweet['verification_status']}")
            print(f"   Has Image: {'✅' if tweet['has_image'] else '❌'}")
            print(f"   Has Link: {'✅' if tweet['has_link'] else '❌'}")
            print(f"   Affiliate Tag: {'✅' if tweet['affiliate_link_found'] else '❌'}")
            if tweet.get('text_content'):
                preview = tweet['text_content'][:100] + "..." if len(tweet['text_content']) > 100 else tweet['text_content']
                print(f"   Preview: {preview}")
        
        print("\n" + "="*60)

def main():


    def analyze_visual_quality(self, tweet_elem):
        """Analyze visual quality of posted graphics"""
        try:
            # Look for images in the tweet
            images = tweet_elem.find_elements('css selector', 'img')
            quality_score = 5  # Base score
            issues = []
            
            for img in images:
                alt_text = img.get_attribute('alt') or ''
                src = img.get_attribute('src') or ''
                
                # Quality indicators
                if any(word in alt_text.lower() for word in ['gradient', 'professional', 'branded']):
                    quality_score += 1
                elif any(word in alt_text.lower() for word in ['basic', 'simple', 'plain']):
                    quality_score -= 1
                    issues.append('Basic design detected')
                
                # Check for overused elements
                if 'blue' in alt_text.lower() and 'gradient' in alt_text.lower():
                    quality_score -= 1
                    issues.append('Overused blue gradient')
                
                # Viral potential indicators
                if any(word in alt_text.lower() for word in ['dynamic', 'bold', 'eye-catching']):
                    quality_score += 1
                
            return {
                'quality_score': max(1, min(10, quality_score)),
                'issues': issues,
                'has_visuals': len(images) > 0,
                'visual_count': len(images)
            }
        except Exception as e:
            return {'error': str(e), 'quality_score': 0}
    
    def detect_duplicate_content(self, current_tweet_text, recent_tweets):
        """Detect if current tweet is duplicate of recent ones"""
        import difflib
        
        duplicates_found = []
        similarity_threshold = 0.7
        
        for recent_tweet in recent_tweets:
            similarity = difflib.SequenceMatcher(None, 
                current_tweet_text.lower(), 
                recent_tweet.lower()
            ).ratio()
            
            if similarity > similarity_threshold:
                duplicates_found.append({
                    'similarity': similarity,
                    'duplicate_text': recent_tweet[:100]
                })
        
        return {
            'is_duplicate': len(duplicates_found) > 0,
            'duplicates': duplicates_found,
            'similarity_scores': [d['similarity'] for d in duplicates_found]
        }
    
    def assess_viral_potential(self, tweet_elem):
        """Assess viral potential of posted content"""
        try:
            tweet_text = tweet_elem.text.lower()
            viral_score = 5
            viral_factors = []
            
            # Positive viral indicators
            viral_keywords = ['ai', 'breaking', 'thread', 'tips', 'secrets', 'reality', 'truth']
            for keyword in viral_keywords:
                if keyword in tweet_text:
                    viral_score += 1
                    viral_factors.append(f'Contains viral keyword: {keyword}')
            
            # Engagement hooks
            hooks = ['did you know', 'here's what', 'the truth about', 'reality check']
            for hook in hooks:
                if hook in tweet_text:
                    viral_score += 2
                    viral_factors.append(f'Strong engagement hook: {hook}')
            
            # Visual enhancement
            has_media = len(tweet_elem.find_elements('css selector', 'img, video')) > 0
            if has_media:
                viral_score += 1
                viral_factors.append('Has visual content')
            
            # Thread format (higher viral potential)
            if 'tweet' in tweet_text and any(str(i) in tweet_text for i in range(1, 6)):
                viral_score += 1
                viral_factors.append('Thread format detected')
            
            return {
                'viral_score': max(1, min(10, viral_score)),
                'factors': viral_factors,
                'recommendation': 'high_potential' if viral_score >= 7 else 'medium_potential' if viral_score >= 5 else 'low_potential'
            }
        except Exception as e:
            return {'error': str(e), 'viral_score': 0}
    
    def generate_improvement_recommendations(self, quality_analysis, viral_analysis, duplicate_analysis):

    def analyze_visual_quality(self, tweet_elem):
        """Analyze visual quality of posted graphics"""
        try:
            # Look for images in the tweet
            images = tweet_elem.find_elements('css selector', 'img')
            quality_score = 5  # Base score
            issues = []
            
            for img in images:
                alt_text = img.get_attribute('alt') or ''
                
                # Quality indicators
                if any(word in alt_text.lower() for word in ['gradient', 'professional', 'branded']):
                    quality_score += 1
                elif any(word in alt_text.lower() for word in ['basic', 'simple', 'plain']):
                    quality_score -= 1
                    issues.append('Basic design detected')
                
                # Check for overused elements
                if 'blue' in alt_text.lower() and 'gradient' in alt_text.lower():
                    quality_score -= 1
                    issues.append('Overused blue gradient')
                
            return {
                'quality_score': max(1, min(10, quality_score)),
                'issues': issues,
                'has_visuals': len(images) > 0
            }
        except Exception as e:
            return {'error': str(e), 'quality_score': 0}
    
    def detect_duplicate_content(self, current_text, recent_tweets):
        """Detect duplicate content"""
        import difflib
        
        duplicates = []
        for recent in recent_tweets:
            similarity = difflib.SequenceMatcher(None, current_text.lower(), recent.lower()).ratio()
            if similarity > 0.7:
                duplicates.append({'similarity': similarity, 'text': recent[:50]})
        
        return {
            'is_duplicate': len(duplicates) > 0,
            'duplicates': duplicates
        }
    
    def assess_viral_potential(self, tweet_text):
        """Assess viral potential"""
        viral_score = 5
        factors = []
        
        # Viral keywords
        viral_words = ['ai', 'thread', 'reality', 'truth', 'secret']
        for word in viral_words:
            if word in tweet_text.lower():
                viral_score += 1
                factors.append(f'Contains: {word}')
        
        # Engagement hooks
        hooks = ['did you know', 'reality check', 'thread:']
        for hook in hooks:
            if hook in tweet_text.lower():
                viral_score += 2
                factors.append(f'Hook: {hook}')
        
        return {
            'viral_score': max(1, min(10, viral_score)),
            'factors': factors,
            'potential': 'high' if viral_score >= 7 else 'medium' if viral_score >= 5 else 'low'
        }
    
    def generate_recommendations(self, quality_analysis, viral_analysis, duplicate_analysis):
        """Generate improvement recommendations"""
        recommendations = []
        
        if quality_analysis.get('quality_score', 0) < 7:
            recommendations.append('UPGRADE VISUALS: Use more professional, dynamic graphics')
        
        if 'Basic design' in str(quality_analysis.get('issues', [])):
            recommendations.append('DESIGN BOOST: Replace basic elements with engaging visuals')
        
        if viral_analysis.get('viral_score', 0) < 6:
            recommendations.append('VIRAL BOOST: Add trending topics or stronger hooks')
        
        if duplicate_analysis.get('is_duplicate', False):
            recommendations.append('CONTENT VARIETY: Create fresh, unique content')
        
        return recommendations

        """Generate specific recommendations for improvement"""
        recommendations = []
        
        # Quality improvements
        if quality_analysis.get('quality_score', 0) < 7:
            recommendations.append('🎨 VISUAL QUALITY: Upgrade to more professional, dynamic graphics')
            
        if 'Basic design detected' in quality_analysis.get('issues', []):
            recommendations.append('🚀 DESIGN UPGRADE: Replace basic elements with engaging visuals')
            
        if 'Overused blue gradient' in quality_analysis.get('issues', []):
            recommendations.append('🌈 COLOR VARIETY: Try different color schemes and backgrounds')
        
        # Viral potential improvements  
        if viral_analysis.get('viral_score', 0) < 6:
            recommendations.append('📈 VIRAL BOOST: Add trending topics, stronger hooks, or timely content')
            
        # Duplicate prevention
        if duplicate_analysis.get('is_duplicate', False):
            recommendations.append('🔄 CONTENT VARIETY: Detected duplicates - create fresh, unique content')
        
        # Strategic recommendations
        if not quality_analysis.get('has_visuals', False):
            recommendations.append('📸 ADD VISUALS: Posts without graphics get lower engagement')
        
        return recommendations


    """Run the Twitter visual verification"""
    verifier = TwitterVisualVerifier()
    
    print("🚀 Starting Twitter Visual Verification Agent...")
    
    # Run verification
    report = verifier.verify_latest_posts()
    
    # Save and display results
    verifier.save_verification_report(report)
    verifier.print_verification_summary(report)
    
    # Return status code for automation
    if report['overall_status'] == '✅ ALL_VERIFIED':
        return 0  # Success
    elif report['overall_status'] == '⚠️ PARTIAL_VERIFICATION':
        return 1  # Warning
    else:
        return 2  # Error

if __name__ == "__main__":
    exit(main())
