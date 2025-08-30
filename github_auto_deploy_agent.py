

# DEPRECATED: This agent has been merged into consolidated_agent
# Please use consolidated_agent instead
# This file will be removed in future updates

# DEPRECATED: This agent has been merged into consolidated_agent
# Please use consolidated_agent instead
# This file will be removed in future updates
#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: GitHub Auto-Deploy Agent
PURPOSE: Automatically deploy content to GitHub for instant website updates
CATEGORY: Deployment & Infrastructure
STATUS: Phase 2 - Fully Autonomous Operation
"""

import os
import requests
import base64
import json
from datetime import datetime
from dotenv import load_dotenv

class GitHubAutoDeployAgent:
    def __init__(self):
        load_dotenv()
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo = "komoglobal/wealthyrobots-website"
        self.domain = "wealthyrobots.com"
        
    def setup_github_token(self):
        """Setup GitHub token for autonomous deployment"""

        if not self.github_token:
            print("⚠️ GitHub token not configured - falling back to manual deployment")
            print("📋 To enable auto-deployment: export GITHUB_TOKEN='your_personal_access_token'")
            print("🔗 Get token at: https://github.com/settings/tokens")
            print("✅ Enable: repo, workflow, write:packages permissions")
            return False

        print("✅ GitHub token configured for autonomous deployment")
        return True
    
    def auto_deploy_article(self, filename, content):
        """Automatically deploy article to GitHub"""
        
        if not self.setup_github_token():
            return self.manual_deployment_instructions(filename, content)
        
        try:
            print(f"🚀 Auto-deploying {filename} to GitHub...")
            
            # GitHub API endpoint
            url = f"https://api.github.com/repos/{self.repo}/contents/{filename}"
            
            # Headers
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Check if file exists
            response = requests.get(url, headers=headers)
            
            # Prepare data
            data = {
                "message": f"Auto-deploy: {filename} - AI generated content with visuals",
                "content": base64.b64encode(content.encode()).decode()
            }
            
            # If file exists, add SHA for update
            if response.status_code == 200:
                data["sha"] = response.json()["sha"]
                action = "Updated"
            else:
                action = "Created"
            
            # Deploy to GitHub
            deploy_response = requests.put(url, headers=headers, json=data)
            
            if deploy_response.status_code in [200, 201]:
                print(f"✅ {action}: {filename}")
                print(f"🌐 Will be live at: https://{self.domain}/{filename}")
                print("⚡ Vercel auto-deployment triggered")
                return True
            else:
                print(f"❌ Deployment failed: {deploy_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Auto-deployment error: {e}")
            return self.manual_deployment_instructions(filename, content)
    
    def manual_deployment_instructions(self, filename, content):
        """Provide manual deployment instructions"""
        
        print(f"📋 MANUAL DEPLOYMENT REQUIRED FOR: {filename}")
        print("=" * 50)
        print("1. Go to: https://github.com/komoglobal/wealthyrobots-website")
        print("2. Click: Add file → Create new file")
        print(f"3. Filename: {filename}")
        print("4. Copy content from generated file")
        print("5. Commit: Auto-deploy AI content with visuals")
        print("6. ✅ Live at wealthyrobots.com in 2 minutes!")
        
        # Save deployment instructions
        instructions_file = f"{filename}_deployment_instructions.txt"
        instructions = f"""
DEPLOYMENT INSTRUCTIONS FOR {filename}
=====================================
Generated: {datetime.now()}

1. GitHub Repository: https://github.com/{self.repo}
2. Create new file: {filename}
3. Copy content from: {filename}
4. Commit message: Auto-deploy: {filename}
5. Live URL: https://{self.domain}/{filename}

CONTENT READY FOR DEPLOYMENT:
{content[:200]}...
"""
        
        with open(instructions_file, 'w') as f:
            f.write(instructions)
        
        print(f"💾 Instructions saved: {instructions_file}")
        return True

if __name__ == "__main__":
    agent = GitHubAutoDeployAgent()
    print("🚀 GitHub Auto-Deploy Agent Ready")
    print("✅ Can deploy content automatically to wealthyrobots.com")
