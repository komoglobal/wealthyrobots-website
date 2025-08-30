#!/usr/bin/env python3
"""
Autonomous Deployment Script for WealthyRobot Website
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(command, cwd="/home/ubuntu/wealthyrobot"):
    """Execute shell command"""
    print(f"🔄 Executing: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        print(f"Error: {result.stderr}")
        return False, result.stderr
    print(f"✅ Command successful: {command}")
    return True, result.stdout

def main():
    print("🚀 Starting Autonomous Deployment Process...")
    print(f"📅 Time: {datetime.now()}")

    # Step 1: Ensure we're in the right directory
    os.chdir("/home/ubuntu/wealthyrobot")

    # Step 2: Check Git status
    print("\n📋 Checking Git status...")
    success, output = run_command("git status --porcelain")
    if output.strip():
        print("📝 Committing changes...")
        run_command("git add .")
        run_command("git commit -m 'Automated deployment'")
    else:
        print("✅ Git repository is clean")

    # Step 3: Push to GitHub
    print("\n⬆️ Pushing to GitHub...")
    success, output = run_command("git push origin main")
    if not success:
        print("⚠️ Push failed, trying to set upstream...")
        run_command("git push -u origin main")

    # Step 4: Deploy to Vercel
    print("\n🚀 Deploying to Vercel...")
    success, output = run_command("vercel --prod --yes")
    if not success:
        print("⚠️ First deployment failed, trying login...")
        run_command("vercel login")
        run_command("vercel --prod --yes")

    print("\n🎉 Deployment process completed!")
    print("🌐 Website should be live at: https://wealthyrobots.com")

if __name__ == "__main__":
    main()
