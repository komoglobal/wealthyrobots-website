from real_money_agent import RealMoneyAgent
from twitter_posting_agent import TwitterPostingAgent

class MoneyTwitterAgent:
    def __init__(self):
        print("💰🐦 Money + Twitter Agent: Initializing...")
        self.money_agent = RealMoneyAgent()
        self.twitter_agent = TwitterPostingAgent()
        
    def run_complete_cycle(self):
        """Generate money-making content and post to Twitter"""
        print("🚀 Running complete money-making + Twitter cycle...")
        
        # 1. Generate viral money-making content (using correct method name)
        print("💰 Generating viral money-making content...")
        money_result = self.money_agent.create_viral_thread()  # Correct method name
        
        # 2. Post to Twitter if successful
        if money_result and money_result.get("status") == "success":
            print("💰 Content generated successfully, posting to Twitter...")
            
            # Find the latest thread file
            import glob
            thread_files = glob.glob("smart_viral_thread_*.txt")
            
            if thread_files:
                latest_file = sorted(thread_files)[-1]
                print(f"📄 Found content file: {latest_file}")
                
                with open(latest_file, 'r') as f:
                    content = f.read()
                
                # Extract and post thread
                if "YOUR VIRAL THREAD" in content:
                    thread_start = content.find("YOUR VIRAL THREAD")
                    thread_end = content.find("============================================================", thread_start)
                    if thread_end == -1:
                        thread_end = len(content)
                    
                    thread_content = content[thread_start:thread_end]
                    
                    print("🐦 Posting thread to Twitter...")
                    twitter_result = self.twitter_agent.post_thread(thread_content)
                    
                    return {
                        "status": "success",
                        "money_result": money_result,
                        "twitter_result": twitter_result,
                        "revenue_potential": money_result.get("session_revenue", 0),
                        "tweets_posted": twitter_result.get("tweets_posted", 0),
                        "thread_file": latest_file
                    }
                else:
                    print("❌ No thread content found in file")
                    return {"status": "no_thread", "money_result": money_result}
            else:
                print("❌ No thread files found")
                return {"status": "no_files", "money_result": money_result}
        else:
            print("❌ Money agent failed to generate content")
            return {"status": "money_failed", "money_result": money_result}

if __name__ == "__main__":
    agent = MoneyTwitterAgent()
    result = agent.run_complete_cycle()
    print(f"\n🎯 Final Result: {result['status']}")
    
    if result['status'] == 'success':
        print(f"💰 Revenue Potential: ${result['revenue_potential']}")
        print(f"🐦 Tweets Posted: {result['tweets_posted']}")
        print(f"📄 Content File: {result['thread_file']}")
    else:
        print(f"⚠️ Issue: {result.get('status', 'unknown')}")
        if 'money_result' in result:
            print(f"💰 Money Agent: {result['money_result']}")
