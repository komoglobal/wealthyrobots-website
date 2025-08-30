import openai
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EmailMarketingAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.campaigns_sent = 0
        
    def create_email_campaign(self):
        """Create and send email marketing campaign"""
        print("📧 Email Marketing Agent: Creating campaign...")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Create a short professional email about AI business automation benefits"}]
            )
            
            content = response.choices[0].message.content
            self.campaigns_sent += 1
            
            print("✅ Email campaign created!")
            print(f"📊 Total campaigns: {self.campaigns_sent}")
            print(f"📝 Content preview: {content[:100]}...")
            
            return {"status": "success", "content": content}
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error"}

    def run_cycle(self):
        """Main cycle for email marketing agent"""
        return self.create_email_campaign()

if __name__ == "__main__":
    agent = EmailMarketingAgent()
    result = agent.create_email_campaign()
    print(f"Campaign result: {result['status']}")
