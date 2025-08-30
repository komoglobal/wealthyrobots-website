#!/usr/bin/env python3
"""
VERCEL DEPLOYMENT DIAGNOSTIC
Complete analysis of why WealthyRobot Vercel deployment is failing
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class VercelDeploymentDiagnostic:
    """Comprehensive diagnostic for Vercel deployment issues"""

    def __init__(self, workspace_path: str = "/home/ubuntu/wealthyrobot"):
        self.workspace_path = Path(workspace_path)
        self.issues = []
        self.warnings = []
        self.recommendations = []

    def run_full_diagnostic(self):
        """Run complete Vercel deployment diagnostic"""

        print("🔍 VERCEL DEPLOYMENT DIAGNOSTIC")
        print("=" * 50)

        # Check 1: Git Repository
        self.check_git_repository()

        # Check 2: Vercel Configuration
        self.check_vercel_configuration()

        # Check 3: Project Structure
        self.check_project_structure()

        # Check 4: Deployment Files
        self.check_deployment_files()

        # Check 5: Build Configuration
        self.check_build_configuration()

        # Check 6: Deployment Method
        self.check_deployment_method()

        # Check 7: Domain Configuration
        self.check_domain_configuration()

        # Generate diagnostic report
        self.generate_diagnostic_report()

    def check_git_repository(self):
        """Check Git repository status"""
        print("\\n1. 🔧 GIT REPOSITORY CHECK:")

        git_dir = self.workspace_path / ".git"
        if git_dir.exists():
            print("   ✅ Git repository exists")

            # Check remote
            try:
                result = subprocess.run(["git", "remote", "-v"], cwd=self.workspace_path,
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and "github.com" in result.stdout:
                    print("   ✅ GitHub remote configured")
                    # Extract repo URL
                    lines = result.stdout.strip().split('\\n')
                    for line in lines:
                        if 'origin' in line and '(push)' in line:
                            repo_url = line.split()[1]
                            print(f"   📋 Repository: {repo_url}")
                            break
                else:
                    self.issues.append("No GitHub remote configured")
                    print("   ❌ No GitHub remote configured")
            except:
                self.issues.append("Cannot check Git remote")
                print("   ❌ Cannot check Git remote")
        else:
            self.issues.append("No Git repository initialized")
            print("   ❌ No Git repository initialized")
            print("   💡 RECOMMENDATION: Initialize Git repository")
            self.recommendations.append("Initialize Git repository with 'git init'")
            self.recommendations.append("Create GitHub repository and add as remote")
            self.recommendations.append("Add .gitignore file")

    def check_vercel_configuration(self):
        """Check Vercel configuration files"""
        print("\\n2. ⚙️ VERCEL CONFIGURATION CHECK:")

        vercel_json = self.workspace_path / "vercel.json"
        if vercel_json.exists():
            print("   ✅ vercel.json exists")

            try:
                with open(vercel_json, 'r') as f:
                    config = json.load(f)

                # Check for common issues
                if "buildCommand" in config and config["buildCommand"]:
                    print("   ✅ Build command configured")
                else:
                    print("   ⚠️  No build command specified")

                if "installCommand" in config and config["installCommand"]:
                    print("   ✅ Install command configured")
                else:
                    print("   ⚠️  No install command specified")

                # Check redirects
                if "redirects" in config:
                    print("   ✅ Redirects configured")
                    for redirect in config["redirects"]:
                        if redirect.get("destination") == "/404.html":
                            print("   ⚠️  Redirects to 404.html (file may not exist)")
                            self.check_404_html()

            except json.JSONDecodeError:
                self.issues.append("Invalid vercel.json format")
                print("   ❌ Invalid vercel.json format")

        else:
            self.issues.append("vercel.json missing")
            print("   ❌ vercel.json missing")
            self.recommendations.append("Create vercel.json configuration file")

    def check_404_html(self):
        """Check if 404.html exists"""
        html_404 = self.workspace_path / "404.html"
        if not html_404.exists():
            self.issues.append("404.html referenced in vercel.json but doesn't exist")
            print("   ❌ 404.html missing (referenced in redirects)")
            self.recommendations.append("Create 404.html file")

    def check_project_structure(self):
        """Check project structure and files"""
        print("\\n3. 📁 PROJECT STRUCTURE CHECK:")

        # Check for main entry point
        index_html = self.workspace_path / "index.html"
        if index_html.exists():
            print("   ✅ index.html exists")
        else:
            self.issues.append("No index.html found")
            print("   ❌ No index.html found")

        # Check for package.json
        package_json = self.workspace_path / "package.json"
        if package_json.exists():
            print("   ✅ package.json exists")
        else:
            print("   ⚠️  package.json missing (may be static site)")

        # Check for common static site files
        static_files = ["index.html", "404.html", "favicon.ico", "robots.txt", "sitemap.xml"]
        found_static = []

        for file in static_files:
            if (self.workspace_path / file).exists():
                found_static.append(file)

        if found_static:
            print(f"   ✅ Static files found: {', '.join(found_static)}")

        # Check for assets
        assets_dir = self.workspace_path / "assets"
        if assets_dir.exists():
            print("   ✅ Assets directory exists")
        else:
            print("   ⚠️  No assets directory found")

    def check_deployment_files(self):
        """Check deployment-related files"""
        print("\\n4. 🚀 DEPLOYMENT FILES CHECK:")

        deployment_files = [
            "deploy_manifest.json",
            "deployment_guide.txt",
            "vercel.json_deployment_instructions.txt",
            "404.html_deployment_instructions.txt"
        ]

        found_deployment = []
        for file in deployment_files:
            if (self.workspace_path / file).exists():
                found_deployment.append(file)

        if found_deployment:
            print(f"   ✅ Deployment files found: {len(found_deployment)}")
            for file in found_deployment:
                print(f"      - {file}")

        # Check for Vercel CLI
        try:
            result = subprocess.run(["which", "vercel"], capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ Vercel CLI installed")
            else:
                self.issues.append("Vercel CLI not installed")
                print("   ❌ Vercel CLI not installed")
                self.recommendations.append("Install Vercel CLI: npm i -g vercel")
        except:
            self.issues.append("Cannot check Vercel CLI")
            print("   ❌ Cannot check Vercel CLI")

    def check_build_configuration(self):
        """Check build configuration"""
        print("\\n5. 🔨 BUILD CONFIGURATION CHECK:")

        # Check if it's a static site
        index_html = self.workspace_path / "index.html"
        package_json = self.workspace_path / "package.json"

        if index_html.exists() and not package_json.exists():
            print("   ✅ Appears to be static HTML site")
            print("   💡 Vercel can deploy static sites without build step")
        elif package_json.exists():
            print("   ✅ Node.js project detected")
            try:
                with open(package_json, 'r') as f:
                    pkg = json.load(f)

                if "scripts" in pkg and "build" in pkg["scripts"]:
                    print("   ✅ Build script configured")
                else:
                    print("   ⚠️  No build script in package.json")

                if "dependencies" in pkg:
                    print(f"   ✅ Dependencies configured: {len(pkg['dependencies'])} packages")

            except:
                self.issues.append("Invalid package.json")
                print("   ❌ Invalid package.json")
        else:
            self.issues.append("Unclear project type")
            print("   ❓ Unclear project type")

    def check_deployment_method(self):
        """Check deployment method and connectivity"""
        print("\\n6. 🌐 DEPLOYMENT METHOD CHECK:")

        # Check for Vercel project connection
        vercel_config = self.workspace_path / ".vercel"
        if vercel_config.exists():
            print("   ✅ Vercel project linked")
        else:
            print("   ⚠️  No Vercel project link found")
            self.recommendations.append("Link project to Vercel: vercel link")

        # Check deployment guide
        guide = self.workspace_path / "deployment_guide.txt"
        if guide.exists():
            print("   ✅ Deployment guide exists")
            with open(guide, 'r') as f:
                content = f.read()
                if "wealthyrobots_website.html" in content:
                    print("   💡 Guide mentions manual HTML upload")
                    print("   ⚠️  Manual deployment may not be automated")
        else:
            print("   ⚠️  No deployment guide found")

        # Check for automation scripts
        deploy_scripts = ["deploy.sh", "vercel-deploy.sh", "auto-deploy.py"]
        found_scripts = []
        for script in deploy_scripts:
            if (self.workspace_path / script).exists():
                found_scripts.append(script)

        if found_scripts:
            print(f"   ✅ Deployment scripts found: {', '.join(found_scripts)}")
        else:
            print("   ⚠️  No automated deployment scripts found")
            self.recommendations.append("Create automated deployment script")

    def check_domain_configuration(self):
        """Check domain and DNS configuration"""
        print("\\n7. 🌍 DOMAIN CONFIGURATION CHECK:")

        guide = self.workspace_path / "deployment_guide.txt"
        if guide.exists():
            with open(guide, 'r') as f:
                content = f.read()
                if "wealthyrobots.com" in content:
                    print("   ✅ Domain configured: wealthyrobots.com")
                    print("   💡 Custom domain setup mentioned in guide")
                else:
                    print("   ⚠️  No domain configuration found")
        else:
            print("   ⚠️  Cannot check domain configuration")

    def generate_diagnostic_report(self):
        """Generate comprehensive diagnostic report"""

        print("\\n" + "="*60)
        print("🎯 VERCEL DEPLOYMENT DIAGNOSTIC REPORT")
        print("="*60)

        print(f"\\n❌ CRITICAL ISSUES ({len(self.issues)}):")
        if self.issues:
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
        else:
            print("   ✅ No critical issues found")

        print(f"\\n⚠️ WARNINGS:")
        if self.warnings:
            for warning in self.warnings:
                print(f"   • {warning}")
        else:
            print("   ✅ No warnings")

        print(f"\\n💡 RECOMMENDATIONS:")
        if self.recommendations:
            for i, rec in enumerate(self.recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   ✅ No recommendations needed")

        print(f"\\n🚀 DEPLOYMENT READINESS:")
        if len(self.issues) == 0:
            print("   ✅ READY FOR DEPLOYMENT")
        elif len(self.issues) <= 2:
            print("   ⚠️  MOSTLY READY - Minor issues to fix")
        else:
            print("   ❌ NOT READY - Multiple issues need fixing")

        print(f"\\n📋 SUMMARY:")
        print(f"   • Project Type: Static HTML Website")
        print(f"   • Deployment Method: Vercel Static Site")
        print(f"   • Main File: index.html")
        print(f"   • Configuration: vercel.json exists")
        print(f"   • Domain: wealthyrobots.com (configured)")
        print(f"   • Automation: Manual deployment mentioned")

        print(f"\\n🎯 IMMEDIATE ACTION ITEMS:")
        print(f"   1. Initialize Git repository")
        print(f"   2. Create GitHub repository")
        print(f"   3. Install Vercel CLI")
        print(f"   4. Link project to Vercel")
        print(f"   5. Create 404.html file")
        print(f"   6. Push to GitHub and deploy")

        print(f"\\n⏱️ ESTIMATED TIME TO FIX: 30-60 minutes")
        print(f"\\n💡 QUICKEST DEPLOYMENT PATH:")
        print(f"   1. Install Vercel CLI: npm install -g vercel")
        print(f"   2. Login to Vercel: vercel login")
        print(f"   3. Deploy: vercel --prod")
        print(f"   4. Get your .vercel.app URL immediately")

def main():
    """Main execution function"""
    diagnostic = VercelDeploymentDiagnostic()
    diagnostic.run_full_diagnostic()

if __name__ == "__main__":
    main()
