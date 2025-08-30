import openai
import json
import os
import sqlite3
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class AdvancedCEOAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conn = sqlite3.connect('company_data.db', check_same_thread=False)
        
        self.available_agents = {
            'video_content_agent': {'cost': 500, 'revenue_potential': 2000, 'requirements': ['>5k followers']},
            'email_marketing_agent': {'cost': 300, 'revenue_potential': 1500, 'requirements': ['>100 subscribers']},
            'product_creation_agent': {'cost': 1000, 'revenue_potential': 5000, 'requirements': ['>$2000 monthly']},
            'seo_content_agent': {'cost': 400, 'revenue_potential': 1800, 'requirements': ['>$500 monthly']},
            'linkedin_agent': {'cost': 350, 'revenue_potential': 2500, 'requirements': ['LinkedIn account']},
            'podcast_agent': {'cost': 800, 'revenue_potential': 3000, 'requirements': ['>20k followers']}
        }
    
    def simulate_market_scenarios(self):
        print("🎮 CEO: Running market simulation...")
        
        scenarios = [
            {'name': 'AI Regulation Changes', 'probability': 0.3, 'impact': -0.2},
            {'name': 'Twitter Algorithm Update', 'probability': 0.4, 'impact': 0.1},
            {'name': 'Economic Recession', 'probability': 0.25, 'impact': -0.3},
            {'name': 'AI Tool Boom', 'probability': 0.6, 'impact': 0.4},
            {'name': 'Competitor Launch', 'probability': 0.5, 'impact': -0.15}
        ]
        
        active_scenarios = [s for s in scenarios if random.random() < s['probability']]
        
        prompt = f"""
        As CEO, analyze these market scenarios and create strategic responses:
        
        Active Scenarios: {json.dumps(active_scenarios, indent=2)}
        
        For each scenario, provide:
        1. Strategic response plan
        2. Resource allocation changes
        3. New agent requirements
        4. Risk mitigation strategies
        
        Think like a business strategy game - maximize long-term profit.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        
        return response.choices[0].message.content, active_scenarios
    
    def decide_agent_expansion(self):
        print("🤔 CEO: Evaluating agent expansion...")
        
        # Get current revenue
        cursor = self.conn.cursor()
        cursor.execute('SELECT SUM(amount) FROM revenue_streams WHERE date_earned > date("now", "-30 days")')
        monthly_revenue = cursor.fetchone()[0] or 0
        
        viable_agents = []
        for agent_name, info in self.available_agents.items():
            can_afford = monthly_revenue >= info['cost']
            roi = info['revenue_potential'] / info['cost']
            
            if can_afford:
                viable_agents.append({
                    'name': agent_name,
                    'cost': info['cost'],
                    'potential': info['revenue_potential'],
                    'roi': roi
                })
        
        viable_agents.sort(key=lambda x: x['roi'], reverse=True)
        
        if viable_agents:
            prompt = f"""
            As CEO, decide which agents to hire:
            
            Monthly Revenue: ${monthly_revenue:.2f}
            Viable Agents: {json.dumps(viable_agents, indent=2)}
            
            Recommend:
            1. Which agents to hire immediately
            2. Priority order for hiring
            3. Expected outcomes
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return viable_agents, response.choices[0].message.content
        
        return [], "No viable expansions at current revenue level"
    
    def run_strategic_ceo_cycle(self):
        print("=" * 60)
        print("🏢 ADVANCED CEO AGENT - STRATEGIC ANALYSIS")
        print("=" * 60)
        
        # Market simulation
        simulation_results, scenarios = self.simulate_market_scenarios()
        
        # Agent expansion analysis
        viable_agents, expansion_decision = self.decide_agent_expansion()
        
        # Save strategic report
        strategic_report = {
            'timestamp': datetime.now().isoformat(),
            'market_scenarios': scenarios,
            'simulation_results': simulation_results,
            'viable_agents': viable_agents,
            'expansion_decisions': expansion_decision
        }
        
        with open('ceo_strategic_report.json', 'w') as f:
            json.dump(strategic_report, f, indent=2)
        
        print(f"\n🎯 STRATEGIC ANALYSIS COMPLETE")
        print(f"📊 Market Scenarios: {len(scenarios)} analyzed")
        print(f"🤖 Viable Expansions: {len(viable_agents)}")
        print(f"📁 Report saved: ceo_strategic_report.json")
        
        return strategic_report

if __name__ == "__main__":
    ceo = AdvancedCEOAgent()
    ceo.run_strategic_ceo_cycle()
