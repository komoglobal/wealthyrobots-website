import openai
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MarketResearchAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.research_completed = 0
        
    def conduct_market_research(self):
        """Conduct comprehensive market research"""
        print("🔍 Market Research Agent: Conducting market analysis...")
        
        try:
            prompt = """Conduct comprehensive market research for AI business automation:
            
            Analyze:
            - Market size and growth trends
            - Target customer segments
            - Key market opportunities
            - Technology trends affecting the market
            - Pricing strategies in the market
            - Market entry barriers
            
            Provide actionable insights and recommendations."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            research = response.choices[0].message.content
            self.research_completed += 1
            
            # Save research
            filename = f"market_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(research)
            
            print("✅ Market research completed!")
            print(f"📊 Research reports: {self.research_completed}")
            print(f"📄 Saved as: {filename}")
            
            return {
                "status": "success",
                "filename": filename,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Market research error: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_cycle(self):
        """Main cycle for market research agent"""
        return self.conduct_market_research()

if __name__ == "__main__":
    agent = MarketResearchAgent()
    result = agent.run_cycle()
    print(f"Research result: {result['status']}")
