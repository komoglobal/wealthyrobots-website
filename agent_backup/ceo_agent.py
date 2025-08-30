import openai
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CEOAgent:
    def __init__(self):
        # Set your OpenAI API key here or in .env file
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY") or "your-openai-api-key-here"
        )
        self.company_state = {
            "active_opportunities": [],
            "active_agents": [],
            "revenue_streams": [],
            "decisions_made": []
        }
        
    def scan_market_opportunities(self):
        """Scan for current profitable opportunities"""
        print("🔍 CEO Agent: Scanning market opportunities...")
        
        prompt = """
        You are an AI CEO with unlimited potential. Analyze the current market (July 2025) and identify 3-5 highly profitable online business opportunities that can be automated.

        Focus on opportunities that:
        - Can start with minimal capital ($0-$500)
        - Have high profit margins (50%+)
        - Can be largely automated with AI
        - Have quick time to revenue (30-90 days)

        Consider: affiliate marketing, AI-generated content, dropshipping, digital products, SaaS tools, online courses, social media monetization, AI services.

        Return your analysis in this JSON format:
        {
            "opportunities": [
                {
                    "name": "opportunity name",
                    "description": "brief description",
                    "startup_cost": "$amount",
                    "profit_potential": "$amount/month",
                    "automation_level": "1-10 scale",
                    "time_to_revenue": "days",
                    "difficulty": "1-10 scale",
                    "required_agents": ["agent1", "agent2"]
                }
            ]
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error scanning opportunities: {str(e)}"
    
    def evaluate_and_decide(self, opportunities_text):
        """Make executive decision on which opportunity to pursue"""
        print("🧠 CEO Agent: Evaluating opportunities and making decision...")
        
        prompt = f"""
        As the CEO, analyze these opportunities: {opportunities_text}
        
        Make an executive decision:
        1. Which opportunity should we pursue FIRST?
        2. Why is this the best choice right now?
        3. What specific agents do I need to create immediately?
        4. What's the 30-day execution plan?
        5. What resources do I need to allocate?
        
        Be decisive and actionable. This decision will determine our company's next moves.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            decision = response.choices[0].message.content
            
            # Log decision
            self.company_state["decisions_made"].append({
                "timestamp": datetime.now().isoformat(),
                "decision": decision,
                "type": "opportunity_selection"
            })
            
            return decision
            
        except Exception as e:
            return f"Error making decision: {str(e)}"
    
    def create_agent_blueprint(self, decision):
        """Create detailed blueprint for required agents"""
        print("📋 CEO Agent: Creating agent blueprints...")
        
        prompt = f"""
        Based on this decision: {decision}
        
        Create detailed blueprints for each agent I need to build:
        
        For each agent, specify:
        - Agent name and role
        - Primary responsibilities  
        - Required capabilities/APIs
        - Success metrics
        - Integration points with other agents
        - Resource requirements
        
        Make this actionable - I need to know exactly what to build.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error creating blueprints: {str(e)}"
    
    def run_ceo_cycle(self):
        """Execute one complete CEO decision cycle"""
        print("=" * 60)
        print("🤖 AUTONOMOUS CEO AGENT - STARTING DECISION CYCLE")
        print("=" * 60)
        
        # Step 1: Market Analysis
        opportunities = self.scan_market_opportunities()
        print("\n📊 MARKET OPPORTUNITIES IDENTIFIED:")
        print(opportunities)
        
        # Step 2: Executive Decision
        decision = self.evaluate_and_decide(opportunities)
        print("\n⚡ CEO DECISION:")
        print(decision)
        
        # Step 3: Agent Planning
        blueprints = self.create_agent_blueprint(decision)
        print("\n🛠️ AGENT BLUEPRINTS:")
        print(blueprints)
        
        # Step 4: Save state
        with open('ceo_decisions.json', 'w') as f:
            json.dump(self.company_state, f, indent=2)
        
        print("\n" + "=" * 60)
        print("✅ CEO CYCLE COMPLETE - Ready for implementation!")
        print("📁 Decisions saved to ceo_decisions.json")
        print("=" * 60)
        
        return {
            "opportunities": opportunities,
            "decision": decision,
            "blueprints": blueprints
        }

if __name__ == "__main__":
    # Initialize and run CEO
    ceo = CEOAgent()
    results = ceo.run_ceo_cycle()





