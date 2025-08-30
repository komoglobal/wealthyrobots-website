import openai
import os
import subprocess
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CoderAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.projects_completed = 0
        self.code_files_created = 0
        
    def analyze_business_needs(self, business_requirements):
        """Analyze what code needs to be built"""
        print("💻 Coder Agent: Analyzing business requirements...")
        
        prompt = f"""As an expert Python developer, analyze these business requirements:
        {business_requirements}
        
        Provide:
        1. What code/agents need to be built
        2. Priority order (1-10)
        3. Estimated development time
        4. Technical approach
        5. Required libraries/APIs
        
        Format as JSON with clear recommendations."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            
            analysis = response.choices[0].message.content
            print("✅ Business analysis complete!")
            
            return {"status": "success", "analysis": analysis}
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return {"status": "error", "error": str(e)}
    
    def generate_agent_code(self, agent_spec):
        """Generate complete Python agent code"""
        print(f"🛠️ Coder Agent: Building {agent_spec.get('name', 'Custom Agent')}...")
        
        prompt = f"""Build a complete Python agent with these specifications:
        {json.dumps(agent_spec, indent=2)}
        
        Requirements:
        - Complete working Python class
        - Error handling
        - Logging and status updates  
        - Integration with OpenAI API
        - Main execution block
        - Professional code comments
        - Follow the pattern of other agents in the system
        
        Make it production-ready and autonomous."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            
            code = response.choices[0].message.content
            
            # Clean up the code (remove markdown formatting if present)
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].strip()
            
            self.code_files_created += 1
            print("✅ Agent code generated!")
            
            return {"status": "success", "code": code}
            
        except Exception as e:
            print(f"❌ Code generation error: {e}")
            return {"status": "error", "error": str(e)}
    
    def deploy_agent(self, agent_name, agent_code):
        """Deploy and test the generated agent"""
        print(f"🚀 Coder Agent: Deploying {agent_name}...")
        
        try:
            filename = f"{agent_name}.py"
            
            # Save the code
            with open(filename, 'w') as f:
                f.write(agent_code)
            
            # Test syntax
            result = subprocess.run(['python3', '-m', 'py_compile', filename], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {agent_name} deployed successfully!")
                print(f"📁 Saved as: {filename}")
                
                # Test import
                try:
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(agent_name, filename)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print(f"✅ {agent_name} imports successfully!")
                    
                except Exception as e:
                    print(f"⚠️ Import warning: {e}")
                
                self.projects_completed += 1
                
                return {
                    "status": "deployed",
                    "filename": filename,
                    "size": os.path.getsize(filename),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                print(f"❌ Syntax error in {agent_name}")
                print(f"Error: {result.stderr}")
                return {"status": "syntax_error", "error": result.stderr}
                
        except Exception as e:
            print(f"❌ Deployment error: {e}")
            return {"status": "error", "error": str(e)}
    
    def build_custom_solution(self, requirements):
        """Build a custom solution based on CEO requirements"""
        print("🏗️ Coder Agent: Building custom solution...")
        
        # Analyze requirements
        analysis = self.analyze_business_needs(requirements)
        if analysis["status"] != "success":
            return analysis
        
        # Generate the code
        agent_spec = {
            "name": requirements.get("agent_name", "custom_agent"),
            "purpose": requirements.get("purpose", "Custom business automation"),
            "features": requirements.get("features", []),
            "integrations": requirements.get("integrations", [])
        }
        
        code_result = self.generate_agent_code(agent_spec)
        if code_result["status"] != "success":
            return code_result
        
        # Deploy the agent
        deploy_result = self.deploy_agent(agent_spec["name"], code_result["code"])
        
        if deploy_result["status"] == "deployed":
            print("🎯 Custom solution built and deployed!")
            
            # Log the project
            project_log = {
                "project_name": agent_spec["name"],
                "requirements": requirements,
                "completion_date": datetime.now().isoformat(),
                "file_created": deploy_result["filename"],
                "status": "completed"
            }
            
            with open('coder_projects.json', 'a') as f:
                f.write(json.dumps(project_log) + "\n")
        
        return deploy_result
    
    def run_coder_cycle(self):
        """Main cycle for coder agent"""
        print("💻 Coder Agent: Ready for development tasks!")
        print(f"📊 Projects completed: {self.projects_completed}")
        print(f"📁 Code files created: {self.code_files_created}")
        
        # Example auto-task (you can integrate with CEO decisions)
        auto_requirements = {
            "agent_name": "data_analytics_agent",
            "purpose": "Analyze business performance and generate insights",
            "features": ["data collection", "trend analysis", "report generation"],
            "integrations": ["OpenAI API", "JSON logging"]
        }
        
        return self.build_custom_solution(auto_requirements)

if __name__ == "__main__":
    coder = CoderAgent()
    result = coder.run_coder_cycle()
    print(f"Coder result: {result.get('status', 'unknown')}")
