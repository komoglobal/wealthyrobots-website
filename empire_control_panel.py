import subprocess
import os
import time
from datetime import datetime

class EmpireControlPanel:
    def __init__(self):
        print("🎮 AUTONOMOUS EMPIRE CONTROL PANEL")
        print("=" * 45)
        
    def start_empire(self):
        """Start the continuous operations"""
        print("🚀 Starting continuous autonomous operations...")
        
        # Start operations manager in background
        subprocess.Popen([
            'nohup', 'python3', 'autonomous_operations_manager.py'
        ], stdout=open('operations_empire.log', 'w'), 
           stderr=subprocess.STDOUT)
        
        time.sleep(3)  # Give it time to start
        
        if self.is_empire_running():
            print("✅ Empire is now running continuously!")
            print("📊 Monitor: tail -f operations_empire.log")
            return True
        else:
            print("❌ Failed to start empire")
            return False
    
    def stop_empire(self):
        """Stop the continuous operations"""
        print("🛑 Stopping autonomous empire...")
        
        try:
            subprocess.run(['pkill', '-f', 'autonomous_operations_manager'], check=False)
            print("✅ Empire operations stopped")
            return True
        except:
            print("⚠️ No empire processes found to stop")
            return False
    
    def empire_status(self):
        """Check empire status"""
        print("📊 EMPIRE STATUS CHECK:")
        print("-" * 25)
        
        # Check if operations manager is running
        running = self.is_empire_running()
        print(f"⚡ Operations Manager: {'🟢 RUNNING' if running else '🔴 STOPPED'}")
        
        # Check log file
        if os.path.exists('operations_empire.log'):
            log_size = os.path.getsize('operations_empire.log')
            print(f"📄 Operations Log: {log_size} bytes")
            
            # Show last few lines
            try:
                with open('operations_empire.log', 'r') as f:
                    lines = f.readlines()
                    if lines:
                        print("📋 Latest Activity:")
                        for line in lines[-3:]:
                            print(f"   {line.strip()}")
            except:
                pass
        else:
            print("📄 Operations Log: Not found")
        
        # Check recent content generation
        content_files = [f for f in os.listdir('.') if f.startswith('smart_viral_thread_')]
        print(f"📝 Content Files: {len(content_files)} generated")
        
        # Check agent files
        agent_files = len([f for f in os.listdir('.') if f.endswith('_agent.py')])
        print(f"🤖 Available Agents: {agent_files}")
        
        return running
    
    def is_empire_running(self):
        """Check if empire is currently running"""
        try:
            result = subprocess.run(['pgrep', '-f', 'autonomous_operations_manager'], 
                                  capture_output=True, text=True)
            return len(result.stdout.strip()) > 0
        except:
            return False
    
    def restart_empire(self):
        """Restart the empire operations"""
        print("🔄 Restarting autonomous empire...")
        
        self.stop_empire()
        time.sleep(2)
        return self.start_empire()
    
    def show_live_monitoring(self):
        """Show live monitoring commands"""
        print("👀 LIVE MONITORING COMMANDS:")
        print("-" * 30)
        print("📊 Watch operations: tail -f operations_empire.log")
        print("🔄 Watch real-time: watch -n 30 'tail -5 operations_empire.log'")
        print("📈 Monitor files: watch -n 60 'ls -la smart_viral_thread_*.txt | wc -l'")
        print("🐦 Check Twitter: visit https://twitter.com/WealthyRobot")
    
    def run_control_panel(self):
        """Interactive control panel"""
        while True:
            print(f"\n🎮 EMPIRE CONTROL PANEL - {datetime.now().strftime('%H:%M:%S')}")
            print("=" * 40)
            print("1. 🚀 Start Empire")
            print("2. 🛑 Stop Empire") 
            print("3. 📊 Check Status")
            print("4. 🔄 Restart Empire")
            print("5. 👀 Show Monitoring")
            print("6. ❌ Exit")
            
            choice = input("\n🎯 Select option (1-6): ").strip()
            
            if choice == '1':
                self.start_empire()
            elif choice == '2':
                self.stop_empire()
            elif choice == '3':
                self.empire_status()
            elif choice == '4':
                self.restart_empire()
            elif choice == '5':
                self.show_live_monitoring()
            elif choice == '6':
                print("👋 Exiting control panel...")
                break
            else:
                print("❌ Invalid option, try again")
            
            input("\n⏸️ Press Enter to continue...")

if __name__ == "__main__":
    control = EmpireControlPanel()
    
    print("🎯 Quick Actions:")
    print("  python3 empire_control_panel.py  # Interactive control")
    print("  python3 -c 'from empire_control_panel import EmpireControlPanel; EmpireControlPanel().start_empire()'  # Quick start")
    print("  python3 -c 'from empire_control_panel import EmpireControlPanel; EmpireControlPanel().empire_status()'  # Quick status")
    
    # Run interactive control panel
    control.run_control_panel()
