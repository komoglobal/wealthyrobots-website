import openai
import os
import subprocess
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ImprovedCoderAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.projects_completed = 0
        
    def generate_working_agent(self, agent_name, purpose):
        """Generate a complete, working agent"""
        print(f"🛠️ Improved Coder: Building {agent_name}...")
        
        prompt = f"""Create a complete, working Python agent class for: {agent_name}

Purpose: {purpose}

Requirements:
- Complete working Python class with proper imports
- Use OpenAI API with proper error handling
- Include meaningful print statements showing progress
- Save results to files when appropriate
- Have a working if __name__ == "__main__" block
- No TODO comments or placeholders
- Make it actually functional and useful

Build a COMPLETE, WORKING agent - no placeholders!"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2500
            )
            
            code = response.choices[0].message.content
            
            # Clean up code formatting
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].strip()
            
            # Save and test
            filename = f"{agent_name}.py"
            with open(filename, 'w') as f:
                f.write(code)
            
            print(f"✅ Generated {filename}")
            
            # Test syntax
            result = subprocess.run(['python3', '-m', 'py_compile', filename], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {agent_name} syntax check passed!")
                self.projects_completed += 1
                return {"status": "success", "filename": filename}
            else:
                print(f"❌ Syntax error: {result.stderr}")
                return {"status": "syntax_error", "error": result.stderr}
                
        except Exception as e:
            print(f"❌ Generation error: {e}")
            return {"status": "error", "error": str(e)}
    
    def build_agent_suite(self):
        """Build a suite of useful agents"""
        print("🏗️ Improved Coder: Building agent suite...")
        
        agents_to_build = [
            ("market_research_agent", "Research market trends and opportunities"),
            ("competitor_analysis_agent", "Analyze competitors and market positioning"),
            ("content_optimizer_agent", "Optimize content for SEO and engagement")
        ]
        
        successful_builds = 0
        
        for agent_name, purpose in agents_to_build:
            result = self.generate_working_agent(agent_name, purpose)
            if result["status"] == "success":
                successful_builds += 1
                print(f"🎯 Built: {agent_name}")
        
        print(f"✅ Agent suite complete: {successful_builds}/{len(agents_to_build)} agents built")
        return successful_builds

if __name__ == "__main__":
    coder = ImprovedCoderAgent()
    result = coder.build_agent_suite()
    print(f"Build result: {result} agents completed")
