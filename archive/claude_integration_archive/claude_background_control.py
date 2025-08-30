#!/usr/bin/env python3
"""
Claude Background Control System
Control background Claude without interrupting manual work
"""

import os
import json
import subprocess
from datetime import datetime

class ClaudeBackgroundControl:
    def __init__(self):
        self.bg_process = None
        
    def start_background_claude(self):
        """Start Claude in background"""
        print("🚀 Starting Claude in background...")
        
        # Remove any existing stop flag
        if os.path.exists('claude_stop.flag'):
            os.remove('claude_stop.flag')
        
        # Start background process
        self.bg_process = subprocess.Popen(
            ['python3', 'claude_background_autonomous.py'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print(f"✅ Claude running in background (PID: {self.bg_process.pid})")
        print("🔄 Claude will operate autonomously every 10 minutes")
        print("💻 You can continue coding normally")
        
        return self.bg_process.pid
    
    def stop_background_claude(self):
        """Stop background Claude"""
        print("🛑 Stopping background Claude...")
        
        # Create stop flag
        with open('claude_stop.flag', 'w') as f:
            f.write(f"Stop requested at {datetime.now().isoformat()}")
        
        print("✅ Stop signal sent to background Claude")
        print("⏳ Claude will stop after current cycle")
    
    def status_background_claude(self):
        """Check background Claude status"""
        print("📊 BACKGROUND CLAUDE STATUS:")
        print("=" * 30)
        
        # Check if process is running
        if os.path.exists('claude_background.log'):
            print("✅ Background log exists")
            
            # Show recent activity
            with open('claude_background.log', 'r') as f:
                lines = f.readlines()
            
            if lines:
                print("📋 Recent activity:")
                for line in lines[-3:]:
                    print(f"  {line.strip()}")
        else:
            print("❌ No background activity detected")
        
        # Check status file
        if os.path.exists('claude_background_status.json'):
            with open('claude_background_status.json', 'r') as f:
                status = json.load(f)
            
            print(f"\n📊 Latest status:")
            print(f"  ⏰ Last update: {status.get('timestamp', 'Unknown')}")
            print(f"  🔄 Background cycle: {status.get('background_cycle', 0)}")
            print(f"  🤖 Agents: {status.get('agent_count', 0)}")
        
        # Check for stop flag
        if os.path.exists('claude_stop.flag'):
            print("\n🛑 Stop flag present - Claude will shutdown")
        else:
            print("\n🔄 Claude background operation active")
    
    def claude_background_menu(self):
        """Interactive background Claude control"""
        while True:
            print("\n🎛️ CLAUDE BACKGROUND CONTROL")
            print("=" * 30)
            print("1. 🚀 Start background Claude")
            print("2. 🛑 Stop background Claude") 
            print("3. 📊 Check Claude status")
            print("4. 📋 View background log")
            print("5. 🔄 Restart Claude")
            print("6. ❌ Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                self.start_background_claude()
            elif choice == '2':
                self.stop_background_claude()
            elif choice == '3':
                self.status_background_claude()
            elif choice == '4':
                self.view_background_log()
            elif choice == '5':
                self.restart_background_claude()
            elif choice == '6':
                break
            else:
                print("❌ Invalid option")
    
    def view_background_log(self):
        """View background Claude activity log"""
        if os.path.exists('claude_background.log'):
            print("\n📋 CLAUDE BACKGROUND LOG:")
            print("=" * 25)
            with open('claude_background.log', 'r') as f:
                lines = f.readlines()
            
            # Show last 10 lines
            for line in lines[-10:]:
                print(line.strip())
        else:
            print("❌ No background log found")
    
    def restart_background_claude(self):
        """Restart background Claude"""
        print("🔄 Restarting background Claude...")
        self.stop_background_claude()
        import time
        time.sleep(2)
        self.start_background_claude()

if __name__ == "__main__":
    control = ClaudeBackgroundControl()
    control.claude_background_menu()
