#!/usr/bin/env python3
"""
CLAUDE Auto-Deployment Framework v1.0
Automatically deploy successful blackbox tests to production
"""

import os
import sys
import json
import time
import shutil
import subprocess
from datetime import datetime
from claude_testing_blackbox import ClaudeTestingBlackbox

class ClaudeAutoDeployment:
    def __init__(self, production_dir="production_agents"):
        print("🚀 CLAUDE Auto-Deployment Framework v1.0 initialized")
        self.blackbox = ClaudeTestingBlackbox()
        self.production_dir = production_dir
        self.backup_dir = "deployment_backups"
        self.deployment_log = "deployment_history.json"
        
        # Create directories
        os.makedirs(self.production_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        print(f"📁 Production directory: {production_dir}")
        print("🔒 Auto-deployment safety: ACTIVE")
    
    def meets_deployment_criteria(self, test_result, criteria=None):
        """Check if test result meets deployment criteria"""
        if criteria is None:
            criteria = {
                "success": True,
                "min_execution_time": 0.0,
                "max_execution_time": 10.0,
                "no_stderr": True
            }
        
        # Basic success check
        if not test_result.get("success", False):
            return False, "Test failed"
        
        # Execution time check
        exec_time = test_result.get("execution_time", 0)
        if exec_time > criteria.get("max_execution_time", 30):
            return False, f"Execution too slow: {exec_time}s"
        
        # Error output check
        if criteria.get("no_stderr", True) and test_result.get("stderr", "").strip():
            return False, f"Has error output: {test_result.get('stderr')}"
        
        # Custom validation hook
        if "stdout" in test_result:
            stdout = test_result["stdout"]
            # Success indicators
            if any(word in stdout.lower() for word in ["error", "failed", "exception"]):
                return False, "Output contains error indicators"
        
        return True, "All criteria met"
    
    def backup_current_production(self, agent_name):
        """Backup current production version before deployment"""
        prod_file = os.path.join(self.production_dir, f"{agent_name}.py")
        
        if os.path.exists(prod_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"{agent_name}_backup_{timestamp}.py")
            shutil.copy2(prod_file, backup_file)
            print(f"💾 Backed up current version: {backup_file}")
            return backup_file
        return None
    
    def deploy_to_production(self, code, agent_name, test_result):
        """Deploy tested code to production"""
        try:
            # Backup current version
            backup_file = self.backup_current_production(agent_name)
            
            # Deploy new version
            prod_file = os.path.join(self.production_dir, f"{agent_name}.py")
            with open(prod_file, 'w') as f:
                f.write(code)
            
            # Log deployment
            deployment_record = {
                "timestamp": datetime.now().isoformat(),
                "agent_name": agent_name,
                "test_result": test_result,
                "backup_file": backup_file,
                "production_file": prod_file,
                "status": "deployed"
            }
            
            self.log_deployment(deployment_record)
            print(f"✅ Deployed {agent_name} to production: {prod_file}")
            return True, deployment_record
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False, str(e)
    
    def log_deployment(self, record):
        """Log deployment history"""
        history = []
        if os.path.exists(self.deployment_log):
            with open(self.deployment_log, 'r') as f:
                history = json.load(f)
        
        history.append(record)
        
        with open(self.deployment_log, 'w') as f:
            json.dump(history, f, indent=2)
    
    def test_and_deploy(self, code, agent_name, test_name=None, criteria=None):
        """Complete test and deploy pipeline"""
        if test_name is None:
            test_name = f"{agent_name}_deployment_test"
        
        print(f"\n🧪 TESTING AND DEPLOYMENT PIPELINE: {agent_name}")
        print("=" * 50)
        
        # Step 1: Test the code
        print("1️⃣ Testing code in blackbox...")
        test_result = self.blackbox.test_code_execution(code, test_name)
        
        # Step 2: Validate results
        print("2️⃣ Validating test results...")
        meets_criteria, reason = self.meets_deployment_criteria(test_result, criteria)
        
        if not meets_criteria:
            print(f"❌ DEPLOYMENT BLOCKED: {reason}")
            return False, test_result
        
        print("✅ Test validation passed!")
        
        # Step 3: Deploy to production
        print("3️⃣ Deploying to production...")
        deployed, deploy_result = self.deploy_to_production(code, agent_name, test_result)
        
        if deployed:
            print(f"🚀 DEPLOYMENT SUCCESS: {agent_name} is now live!")
            
            # Step 4: Post-deployment validation
            print("4️⃣ Running post-deployment validation...")
            self.post_deployment_check(agent_name)
            
            return True, deploy_result
        else:
            print(f"❌ DEPLOYMENT FAILED: {deploy_result}")
            return False, deploy_result
    
    def post_deployment_check(self, agent_name):
        """Validate deployed agent works correctly"""
        try:
            prod_file = os.path.join(self.production_dir, f"{agent_name}.py")
            
            # Syntax check
            with open(prod_file, 'r') as f:
                compile(f.read(), prod_file, 'exec')
            
            print("✅ Post-deployment syntax check passed")
            
            # Basic import test
            result = subprocess.run([
                'python3', '-c', f'exec(open("{prod_file}").read())'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Post-deployment execution check passed")
            else:
                print(f"⚠️ Post-deployment warning: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️ Post-deployment check failed: {e}")
    
    def rollback_deployment(self, agent_name):
        """Rollback to previous version"""
        # Find latest backup
        backups = [f for f in os.listdir(self.backup_dir) if f.startswith(f"{agent_name}_backup_")]
        if not backups:
            print(f"❌ No backup found for {agent_name}")
            return False
        
        latest_backup = sorted(backups)[-1]
        backup_path = os.path.join(self.backup_dir, latest_backup)
        prod_path = os.path.join(self.production_dir, f"{agent_name}.py")
        
        shutil.copy2(backup_path, prod_path)
        print(f"↩️ Rolled back {agent_name} to {latest_backup}")
        return True

# Usage examples for your WealthyRobot agents
def example_content_agent_deployment():
    """Example: Deploy improved content generation agent"""
    deployer = ClaudeAutoDeployment()
    
    # New content agent code
    improved_content_code = '''
# WealthyRobot Content Agent v2.0 - Improved Viral Thread Generator
import random

def generate_viral_thread():
    """Generate engaging AI-focused content"""
    topics = [
        "AI automation will change everything",
        "The future of work is AI-powered",
        "Productivity hacks using AI tools"
    ]
    
    thread_parts = []
    for i, topic in enumerate(topics, 1):
        thread_parts.append(f"{i}/{len(topics)} {topic.upper()}")
    
    thread_parts.append("🔥 Ready to join the AI revolution?")
    thread_parts.append("📚 Get 'The AI Advantage' → https://amzn.to/ai-advantage")
    
    return "\\n\\n".join(thread_parts)

if __name__ == "__main__":
    content = generate_viral_thread()
    print("Generated viral thread:")
    print(content)
'''
    
    # Test and deploy
    success, result = deployer.test_and_deploy(
        improved_content_code, 
        "content_agent_v2",
        "viral_thread_test"
    )
    
    return success

def example_engagement_optimizer_deployment():
    """Example: Deploy engagement optimization algorithm"""
    deployer = ClaudeAutoDeployment()
    
    # Engagement optimizer code
    optimizer_code = '''
# WealthyRobot Engagement Optimizer v1.0
def calculate_engagement_score(post_text):
    """Calculate predicted engagement score"""
    score = 0
    
    # Keyword scoring
    viral_keywords = ["AI", "automation", "future", "revolution", "hack"]
    score += sum(5 for keyword in viral_keywords if keyword.lower() in post_text.lower())
    
    # Emoji bonus
    score += post_text.count("🔥") * 3
    score += post_text.count("🚀") * 3
    
    # Length optimization (150-280 chars is sweet spot)
    length = len(post_text)
    if 150 <= length <= 280:
        score += 10
    
    return min(score, 100)  # Cap at 100

if __name__ == "__main__":
    test_post = "AI automation will revolutionize your workflow 🚀 The future is here!"
    score = calculate_engagement_score(test_post)
    print(f"Engagement score: {score}/100")
'''
    
    # Custom deployment criteria for algorithms
    criteria = {
        "success": True,
        "max_execution_time": 2.0,  # Algorithms should be fast
        "no_stderr": True
    }
    
    success, result = deployer.test_and_deploy(
        optimizer_code,
        "engagement_optimizer",
        "algorithm_test",
        criteria
    )
    
    return success

if __name__ == "__main__":
    print("🤖 WEALTHYROBOT AUTO-DEPLOYMENT SYSTEM")
    print("=" * 45)
    
    # Run example deployments
    print("\n📝 Deploying Content Agent v2.0...")
    content_success = example_content_agent_deployment()
    
    print("\n⚡ Deploying Engagement Optimizer...")
    optimizer_success = example_engagement_optimizer_deployment()
    
    if content_success and optimizer_success:
        print("\n🎉 ALL DEPLOYMENTS SUCCESSFUL!")
        print("Your WealthyRobot empire is now running improved AI agents!")
    else:
        print("\n⚠️ Some deployments failed - check logs for details")
    
    print(f"\n📊 Check deployment history: deployment_history.json")
    print(f"📁 Production agents: production_agents/")
    print(f"💾 Backups available: deployment_backups/")
