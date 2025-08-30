import openai
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SEOContentAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.articles_created = 0
        
    def create_seo_content(self):
        """Create SEO-optimized content"""
        print("🔍 SEO Content Agent: Creating optimized content...")
        
        try:
            prompt = """Create SEO-optimized blog post about autonomous business systems:
            
            Topic: "How AI-Powered Autonomous Agents Are Revolutionizing Business Operations"
            
            Include:
            - SEO-optimized title and meta description
            - Target keywords: autonomous business, AI agents, business automation
            - 800-1000 words
            - Clear headers (H2, H3)
            - Call-to-action
            - Benefits for business owners
            
            Make it engaging and informative."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.choices[0].message.content
            self.articles_created += 1
            
            # Save content
            filename = f"seo_article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(filename, 'w') as f:
                f.write(content)
            
            print("✅ SEO content created!")
            print(f"📊 Total articles: {self.articles_created}")
            print(f"📄 Saved as: {filename}")
            print(f"📝 Word count: {len(content.split())} words")
            
            return {
                "status": "success",
                "filename": filename,
                "word_count": len(content.split()),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ SEO content error: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_cycle(self):
        """Main cycle for SEO content agent"""
        return self.create_seo_content()

if __name__ == "__main__":
    agent = SEOContentAgent()
    result = agent.run_cycle()
    print(f"SEO result: {result['status']}")
