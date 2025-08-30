#!/usr/bin/env python3
"""
FIX VERCEL DEPLOYMENT
Automatically fix all critical Vercel deployment issues
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class VercelDeploymentFixer:
    """Automatically fix all Vercel deployment issues"""

    def __init__(self, workspace_path: str = "/home/ubuntu/wealthyrobot"):
        self.workspace_path = Path(workspace_path)

    def fix_all_issues(self):
        """Fix all critical Vercel deployment issues"""

        print("🔧 FIXING VERCEL DEPLOYMENT ISSUES")
        print("=" * 50)

        fixes_applied = []

        # 1. Initialize Git repository
        if self.initialize_git_repo():
            fixes_applied.append("Git repository initialized")

        # 2. Create 404.html file
        if self.create_404_html():
            fixes_applied.append("404.html created")

        # 3. Create .gitignore
        if self.create_gitignore():
            fixes_applied.append(".gitignore created")

        # 4. Update vercel.json
        if self.update_vercel_config():
            fixes_applied.append("vercel.json updated")

        # 5. Create deployment script
        if self.create_deployment_script():
            fixes_applied.append("Deployment script created")

        # 6. Install Vercel CLI (if Node.js available)
        if self.check_and_install_vercel_cli():
            fixes_applied.append("Vercel CLI checked")

        print("\\n✅ FIXES APPLIED:")
        for fix in fixes_applied:
            print(f"   • {fix}")

        print("\\n🚀 READY FOR DEPLOYMENT!")
        print("\\n📋 NEXT STEPS:")
        print("   1. Create GitHub repository:")
        print("      - Go to https://github.com/new")
        print("      - Name: wealthyrobots-website")
        print("      - Make it public")
        print("   2. Connect to GitHub:")
        print("      git remote add origin https://github.com/YOUR_USERNAME/wealthyrobots-website.git")
        print("      git add .")
        print("      git commit -m 'Initial deployment'")
        print("      git push -u origin main")
        print("   3. Deploy to Vercel:")
        print("      vercel --prod")
        print("   4. Or use the deployment script:")
        print("      ./deploy.sh")

    def initialize_git_repo(self) -> bool:
        """Initialize Git repository"""
        print("\\n1. 📋 Initializing Git Repository...")

        try:
            # Check if already initialized
            if (self.workspace_path / ".git").exists():
                print("   ✅ Git repository already exists")
                return True

            # Initialize repository
            result = subprocess.run(["git", "init"], cwd=self.workspace_path,
                                  capture_output=True, text=True)

            if result.returncode == 0:
                print("   ✅ Git repository initialized")

                # Configure git user (basic)
                subprocess.run(["git", "config", "user.name", "AGI Deployment"],
                             cwd=self.workspace_path, capture_output=True)
                subprocess.run(["git", "config", "user.email", "agi@wealthyrobots.com"],
                             cwd=self.workspace_path, capture_output=True)

                return True
            else:
                print("   ❌ Failed to initialize Git repository")
                print(f"   Error: {result.stderr}")
                return False

        except Exception as e:
            print(f"   ❌ Error initializing Git: {e}")
            return False

    def create_404_html(self) -> bool:
        """Create 404.html file"""
        print("\\n2. 📄 Creating 404.html...")

        html_404 = self.workspace_path / "404.html"

        if html_404.exists():
            print("   ✅ 404.html already exists")
            return True

        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found - WealthyRobot Empire</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
        }
        h1 { font-size: 3rem; margin-bottom: 20px; }
        p { font-size: 1.2rem; margin-bottom: 30px; }
        a {
            color: #ffd700;
            text-decoration: none;
            font-weight: bold;
            padding: 10px 20px;
            border: 2px solid #ffd700;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        a:hover {
            background: #ffd700;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>404</h1>
    <h2>Page Not Found</h2>
    <p>The page you're looking for doesn't exist in the WealthyRobot Empire.</p>
    <a href="/">Return to Empire</a>
</body>
</html>"""

        try:
            with open(html_404, 'w') as f:
                f.write(html_content)
            print("   ✅ 404.html created successfully")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create 404.html: {e}")
            return False

    def create_gitignore(self) -> bool:
        """Create .gitignore file"""
        print("\\n3. 🚫 Creating .gitignore...")

        gitignore = self.workspace_path / ".gitignore"

        if gitignore.exists():
            print("   ✅ .gitignore already exists")
            return True

        gitignore_content = """# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Environment variables
.env
.env.local
.env.production

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Vercel
.vercel/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.temp
.cache/

# Build outputs
dist/
build/
.next/
.nuxt/

# Database
*.db
*.sqlite
*.sqlite3

# Sensitive files
secrets.json
config.local.json
private/
"""

        try:
            with open(gitignore, 'w') as f:
                f.write(gitignore_content)
            print("   ✅ .gitignore created successfully")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create .gitignore: {e}")
            return False

    def update_vercel_config(self) -> bool:
        """Update vercel.json configuration"""
        print("\\n4. ⚙️ Updating vercel.json...")

        vercel_json = self.workspace_path / "vercel.json"

        if not vercel_json.exists():
            print("   ❌ vercel.json doesn't exist")
            return False

        try:
            with open(vercel_json, 'r') as f:
                config = json.load(f)

            # Add build configuration for static site
            if "buildCommand" not in config:
                config["buildCommand"] = None  # No build needed for static HTML

            if "installCommand" not in config:
                config["installCommand"] = None  # No install needed for static HTML

            if "outputDirectory" not in config:
                config["outputDirectory"] = "."  # Serve from root directory

            # Ensure 404.html exists before keeping redirects
            if "redirects" in config:
                # Remove redirect to non-existent 404.html if file doesn't exist
                if not (self.workspace_path / "404.html").exists():
                    print("   ⚠️  Removing redirect to non-existent 404.html")
                    del config["redirects"]

            with open(vercel_json, 'w') as f:
                json.dump(config, f, indent=2)

            print("   ✅ vercel.json updated successfully")
            return True

        except Exception as e:
            print(f"   ❌ Failed to update vercel.json: {e}")
            return False

    def create_deployment_script(self) -> bool:
        """Create automated deployment script"""
        print("\\n5. 🚀 Creating Deployment Script...")

        deploy_script = self.workspace_path / "deploy.sh"

        if deploy_script.exists():
            print("   ✅ deploy.sh already exists")
            return True

        script_content = """#!/bin/bash

echo "🚀 WealthyRobot Vercel Deployment Script"
echo "====================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel:"
    vercel login
fi

# Check if project is linked
if [ ! -d ".vercel" ]; then
    echo "🔗 Linking project to Vercel..."
    vercel link
fi

# Deploy to production
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "🌐 Check your Vercel dashboard for the deployment URL"
"""

        try:
            with open(deploy_script, 'w') as f:
                f.write(script_content)

            # Make executable
            os.chmod(deploy_script, 0o755)

            print("   ✅ deploy.sh created and made executable")
            return True

        except Exception as e:
            print(f"   ❌ Failed to create deploy.sh: {e}")
            return False

    def check_and_install_vercel_cli(self) -> bool:
        """Check and install Vercel CLI"""
        print("\\n6. 🔧 Checking Vercel CLI...")

        try:
            # Check if Node.js/npm is available
            result = subprocess.run(["which", "npm"], capture_output=True, text=True)
            if result.returncode != 0:
                print("   ⚠️  npm not found - cannot install Vercel CLI automatically")
                print("   💡 Manual installation: npm install -g vercel")
                return False

            # Check if Vercel CLI is already installed
            result = subprocess.run(["which", "vercel"], capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ Vercel CLI already installed")
                return True

            print("   📦 Installing Vercel CLI...")
            result = subprocess.run(["npm", "install", "-g", "vercel"],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                print("   ✅ Vercel CLI installed successfully")
                return True
            else:
                print("   ❌ Failed to install Vercel CLI")
                print(f"   Error: {result.stderr}")
                return False

        except Exception as e:
            print(f"   ❌ Error checking Vercel CLI: {e}")
            return False

def main():
    """Main execution function"""
    fixer = VercelDeploymentFixer()
    fixer.fix_all_issues()

if __name__ == "__main__":
    main()
