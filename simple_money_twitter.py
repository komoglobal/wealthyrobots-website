from twitter_posting_agent import TwitterPostingAgent
import subprocess
import glob
import os

class SimpleMoneyTwitter:
    def __init__(self):
        print("💰🐦 Simple Money + Twitter Agent: Starting...")
        self.twitter_agent = TwitterPostingAgent()
        
    def run_cycle(self):
        """Run money agent then post to Twitter"""
        print("🚀 Running complete cycle...")
        
        # 1. Run the money agent directly
        print("💰 Running money agent...")
        try:
            result = subprocess.run(['python3', 'real_money_agent.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Money agent completed successfully!")
                print("🔍 Looking for generated content...")
                
                # 2. Find the latest thread file
                thread_files = glob.glob("smart_viral_thread_*.txt")
                
                if thread_files:
                    latest_file = sorted(thread_files)[-1]
                    print(f"📄 Found: {latest_file}")
                    
                    # 3. Read and post to Twitter
                    with open(latest_file, 'r') as f:
                        content = f.read()
                    
                    if "YOUR VIRAL THREAD" in content:
                        thread_start = content.find("YOUR VIRAL THREAD")
                        thread_content = content[thread_start:thread_start+2000]  # Limit content
                        
                        print("🐦 Posting to Twitter...")
                        twitter_result = self.twitter_agent.post_thread(thread_content)
                        
                        return {
                            "status": "success",
                            "twitter_result": twitter_result,
                            "tweets_posted": twitter_result.get("tweets_posted", 0),
                            "content_file": latest_file
                        }
                    else:
                        print("❌ No thread content found")
                        return {"status": "no_thread"}
                else:
                    print("❌ No thread files generated")
                    return {"status": "no_files"}
            else:
                print(f"❌ Money agent failed: {result.stderr}")
                return {"status": "money_failed", "error": result.stderr}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    agent = SimpleMoneyTwitter()
    result = agent.run_cycle()
    
    print(f"\n🎯 Result: {result['status']}")
    if result['status'] == 'success':
        print(f"🐦 Tweets Posted: {result['tweets_posted']}")
        print(f"📄 Content: {result['content_file']}")
        print("💰 Check @WealthyRobot on Twitter!")
