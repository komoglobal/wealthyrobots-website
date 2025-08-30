#!/usr/bin/env python3
"""
Quick status check for Data Management Agent
"""

import json
import os
from datetime import datetime

def check_status():
    print("🧹 DATA MANAGEMENT AGENT STATUS CHECK")
    print("=" * 40)
    
    # Check if cleanup log exists
    if os.path.exists("data_cleanup_log.json"):
        try:
            with open("data_cleanup_log.json", "r") as f:
                history = json.load(f)
            
            print(f"📊 Cleanup History:")
            print(f"   Total files removed: {history.get('files_removed', 0):,}")
            print(f"   Total space saved: {history.get('space_saved', 0):,} bytes")
            print(f"   Space saved: {round(history.get('space_saved', 0) / (1024*1024), 2)} MB")
            
            if history.get('last_cleanup'):
                last_cleanup = datetime.fromisoformat(history['last_cleanup'])
                time_since = datetime.now() - last_cleanup
                print(f"   Last cleanup: {last_cleanup.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Time since: {time_since}")
            
            if history.get('cleanup_sessions'):
                print(f"   Cleanup sessions: {len(history['cleanup_sessions'])}")
                
                # Show recent sessions
                recent = history['cleanup_sessions'][-3:]  # Last 3
                print(f"\n📅 Recent Cleanup Sessions:")
                for session in recent:
                    timestamp = datetime.fromisoformat(session['timestamp'])
                    print(f"   {timestamp.strftime('%Y-%m-%d %H:%M')}: {session['files_removed']} files, {session['space_saved']} bytes")
            
        except Exception as e:
            print(f"❌ Error reading cleanup log: {e}")
    else:
        print("📝 No cleanup history found - agent hasn't run yet")
    
    # Check cron job
    print(f"\n⏰ Cron Job Status:")
    try:
        import subprocess
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if 'data_management_agent.py' in result.stdout:
            print("   ✅ Cron job is active")
            for line in result.stdout.split('\n'):
                if 'data_management_agent.py' in line:
                    print(f"   📅 Schedule: {line.strip()}")
        else:
            print("   ❌ Cron job not found")
    except Exception as e:
        print(f"   ❓ Could not check cron: {e}")
    
    # Check current file count
    print(f"\n📁 Current System Status:")
    try:
        file_count = len([f for f in os.listdir('.') if os.path.isfile(f)])
        print(f"   Files in workspace: {file_count:,}")
        
        # Check for any remaining duplicate patterns
        duplicate_patterns = [
            "logging_optimization_*.json",
            "trading_dashboard_*.json",
            "risk_dashboard_*.json",
            "firm_dashboard_*.json",
            "performance_dashboard_*.json",
            "claude_solution_*.py"
        ]
        
        total_duplicates = 0
        for pattern in duplicate_patterns:
            import glob
            matches = glob.glob(pattern)
            if matches:
                print(f"   {pattern}: {len(matches)} files")
                total_duplicates += len(matches)
        
        if total_duplicates == 0:
            print("   ✨ No duplicate patterns detected")
        else:
            print(f"   🚨 Total potential duplicates: {total_duplicates}")
            
    except Exception as e:
        print(f"   ❓ Could not check file count: {e}")
    
    print(f"\n💡 Next scheduled cleanup: Every 6 hours (0:00, 6:00, 12:00, 18:00 UTC)")
    print(f"🔧 Manual run: python3 data_management_agent.py")

if __name__ == "__main__":
    check_status()
