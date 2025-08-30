import openai
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DataAnalyticsAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.reports_generated = 0
        
    def analyze_business_performance(self):
        """Analyze business performance and generate insights"""
        print("📊 Data Analytics Agent: Analyzing business performance...")
        
        try:
            prompt = """Analyze business performance for an autonomous AI company:
            
            Generate a comprehensive business analytics report including:
            - Revenue trends and projections
            - Agent performance metrics
            - Growth opportunities
            - Risk assessment
            - Recommended actions
            
            Format as a professional business report."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            report = response.choices[0].message.content
            self.reports_generated += 1
            
            # Save report
            filename = f"business_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report)
            
            print("✅ Business analytics report generated!")
            print(f"📊 Total reports: {self.reports_generated}")
            print(f"📄 Saved as: {filename}")
            
            # Extract key metrics (simulate)
            metrics = {
                "revenue_trend": "increasing",
                "agent_efficiency": "85%",
                "growth_rate": "12%",
                "risk_level": "low"
            }
            
            print("📈 Key Insights:")
            for key, value in metrics.items():
                print(f"   {key.replace('_', ' ').title()}: {value}")
            
            return {
                "status": "success",
                "filename": filename,
                "metrics": metrics,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Analytics error: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_cycle(self):
        """Main cycle for data analytics agent"""
        return self.analyze_business_performance()

if __name__ == "__main__":
    agent = DataAnalyticsAgent()
    result = agent.run_cycle()
    print(f"Analytics result: {result['status']}")
