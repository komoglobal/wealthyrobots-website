import openai
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CompetitorAnalysisAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.analyses_completed = 0
        
    def analyze_competitors(self):
        """Analyze competitors in the AI automation space"""
        print("🥊 Competitor Analysis Agent: Analyzing competition...")
        
        try:
            prompt = """Analyze competitors in the AI business automation market:
            
            Research and analyze:
            - Major competitors and their offerings
            - Pricing strategies and business models
            - Strengths and weaknesses of key players
            - Market positioning and differentiation
            - Competitive advantages and gaps
            - Opportunities for competitive advantage
            
            Focus on actionable competitive intelligence."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            analysis = response.choices[0].message.content
            self.analyses_completed += 1
            
            # Save analysis
            filename = f"competitor_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(analysis)
            
            print("✅ Competitor analysis completed!")
            print(f"📊 Analyses completed: {self.analyses_completed}")
            print(f"📄 Saved as: {filename}")
            
            return {
                "status": "success",
                "filename": filename,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Competitor analysis error: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_cycle(self):
        """Main cycle for competitor analysis agent"""
        return self.analyze_competitors()

if __name__ == "__main__":
    agent = CompetitorAnalysisAgent()
    result = agent.run_cycle()
    print(f"Analysis result: {result['status']}")
