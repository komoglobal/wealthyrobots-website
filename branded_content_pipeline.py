from twitter_posting_agent import TwitterPostingAgent
from twitter_branding_system import TwitterBrandingSystem

class BrandedContentPipeline:
    def __init__(self):
        self.twitter_agent = TwitterPostingAgent()
        self.branding = TwitterBrandingSystem()
        
    def create_and_post_branded_content(self):
        """Create and post branded content"""
        print("🎨 Creating branded content pipeline...")
        
        # Create branded thread
        branded_thread = self.branding.create_branded_thread(
            "5 AI tools that 10x'd my productivity",
            ["Jasper AI ($29/mo)", "Notion ($10/mo)", "Zapier ($20/mo)"]
        )
        
        if branded_thread["status"] == "success":
            # Post to Twitter with branding
            if self.twitter_agent.client:
                result = self.twitter_agent.post_thread(branded_thread["content"])
                
                if result["status"] == "success":
                    print(f"✅ Branded content posted! {result['tweets_posted']} tweets")
                    print("🎯 Brand-consistent content now live on @WealthyRobot!")
                    return result
                else:
                    print(f"❌ Posting failed: {result}")
                    return result
            else:
                print("❌ Twitter not connected")
        else:
            print("❌ Branded content creation failed")

if __name__ == "__main__":
    pipeline = BrandedContentPipeline()
    result = pipeline.create_and_post_branded_content()
    print(f"🎨 Branded pipeline result: {result.get('status', 'unknown')}")
