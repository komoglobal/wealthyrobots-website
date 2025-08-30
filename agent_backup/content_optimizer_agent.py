import openai
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ContentOptimizerAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.optimizations_completed = 0
        
    def optimize_content(self):
        """Optimize content for SEO and engagement"""
        print("📝 Content Optimizer Agent: Optimizing content...")
        
        try:
            prompt = """Create an optimized content strategy for AI business automation:
            
            Provide:
            - SEO-optimized blog post topics
            - Keyword strategies for AI automation
            - Content optimization best practices
            - Engagement improvement techniques
            - Social media content ideas
            - Email marketing content optimization
            
            Focus on actionable content recommendations."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            optimization = response.choices[0].message.content
            self.optimizations_completed += 1
            
            # Save optimization
            filename = f"content_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(optimization)
            
            print("✅ Content optimization completed!")
            print(f"📊 Optimizations completed: {self.optimizations_completed}")
            print(f"📄 Saved as: {filename}")
            
            return {
                "status": "success",
                "filename": filename,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Content optimization error: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_cycle(self):
        """Main cycle for content optimizer agent"""
        return self.optimize_content()

if __name__ == "__main__":
    agent = ContentOptimizerAgent()
    result = agent.run_cycle()
    print(f"Optimization result: {result['status']}")
