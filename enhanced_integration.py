#!/usr/bin/env python3
"""
Enhanced Integration Bridge - Connects all WealthyRobot systems
"""

import json
import time
import os
import subprocess
from datetime import datetime

class EnhancedIntegration:
    def __init__(self):
        self.orchestrator_file = "live_orchestrator.py"
        self.visual_agent_file = "visual_affiliate_agent.py"
        self.scheduler_file = "clean_empire_scheduler.py"
        self.ceo_file = "ultimate_ceo_agent.py"
        
    def check_system_status(self):
        """Check status of all key systems"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'systems': {}
        }
        
        # Check if orchestrator is running
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            status['systems']['orchestrator_running'] = 'live_orchestrator.py' in result.stdout
            status['systems']['scheduler_running'] = any(scheduler in result.stdout for scheduler in ['clean_empire', 'scheduler'])
        except:
            status['systems']['orchestrator_running'] = False
            status['systems']['scheduler_running'] = False
            
        # Check visual assets
        status['systems']['visual_ready'] = (
            os.path.exists('visual_affiliate_agent.py') and
            len([f for f in os.listdir('.') if f.endswith('_203409.png') or f.endswith('_203410.png')]) > 0
        )
        
        # Check affiliate content
        import glob
        affiliate_threads = []
        for file in glob.glob("smart_viral_thread*.txt"):
            try:
                with open(file, 'r') as f:
                    if 'wealthyrobot-20' in f.read():
                        affiliate_threads.append(file)
            except:
                continue
        status['systems']['affiliate_content_ready'] = len(affiliate_threads) > 0
        status['systems']['affiliate_thread_count'] = len(affiliate_threads)
        
        return status
        
    def create_integration_config(self):
        """Create configuration for integrated system"""
        config = {
            "integration_mode": "enhanced",
            "visual_automation": True,
            "affiliate_priority": True,
            "posting_schedule": {
                "visual_content_interval": 120,  # 2 hours
                "regular_content_interval": 60,   # 1 hour
                "peak_hours": ["09:00", "12:00", "15:00", "18:00", "21:00"]
            },
            "revenue_optimization": {
                "affiliate_link_density": "medium",
                "visual_to_text_ratio": "3:1",
                "engagement_tracking": True
            }
        }
        
        with open('integration_config.json', 'w') as f:
            json.dump(config, f, indent=2)
            
        return config
        
    def generate_master_command(self):
        """Generate command to run integrated system"""
        
        # Create master integration script
        master_script = '''#!/usr/bin/env python3
import os
import sys
import threading
import time
from datetime import datetime

# Import all key agents
sys.path.append('.')
from live_orchestrator import *
from visual_affiliate_agent import VisualAffiliateAgent
from clean_empire_scheduler import CleanEmpireScheduler

class MasterIntegration:
    def __init__(self):
        print("🚀 STARTING MASTER INTEGRATION")
        self.visual_agent = VisualAffiliateAgent()
        
    def run_integrated_cycle(self):
        """Run one complete integrated cycle"""
        print("🔄 INTEGRATED CYCLE STARTING...")
        
        # 1. Check for new affiliate content
        # 2. Create visual packages if needed
        # 3. Coordinate with orchestrator
        # 4. Schedule optimal posting times
        
        try:
            # Create visual package for latest content
            package = self.visual_agent.create_complete_affiliate_package()
            if package:
                print("✅ Visual package created")
                return True
        except Exception as e:
            print(f"⚠️ Visual creation issue: {e}")
            
        return False
        
    def start_integration(self):
        """Start the complete integrated system"""
        print("🎯 MASTER INTEGRATION ACTIVE")
        
        while True:
            try:
                self.run_integrated_cycle()
                time.sleep(3600)  # 1 hour cycles
            except KeyboardInterrupt:
                print("🛑 Integration stopped by user")
                break
            except Exception as e:
                print(f"🔥 Integration error: {e}")
                time.sleep(300)  # 5 minute recovery

if __name__ == "__main__":
    master = MasterIntegration()
    master.start_integration()
'''

        with open('master_integration.py', 'w') as f:
            f.write(master_script)
            
        os.chmod('master_integration.py', 0o755)
        
        return "master_integration.py"

if __name__ == "__main__":
    integration = EnhancedIntegration()
    
    print("🔍 SYSTEM STATUS CHECK:")
    status = integration.check_system_status()
    
    print(f"🤖 Orchestrator Running: {status['systems']['orchestrator_running']}")
    print(f"⏰ Scheduler Running: {status['systems']['scheduler_running']}")  
    print(f"🎨 Visual Ready: {status['systems']['visual_ready']}")
    print(f"💰 Affiliate Content: {status['systems']['affiliate_content_ready']} ({status['systems']['affiliate_thread_count']} threads)")
    
    print("\n📋 CREATING INTEGRATION CONFIG...")
    config = integration.create_integration_config()
    print("✅ Config saved: integration_config.json")
    
    print("\n🚀 GENERATING MASTER INTEGRATION...")
    master_file = integration.generate_master_command()
    print(f"✅ Master script created: {master_file}")
    
    print("\n🎯 NEXT STEPS:")
    if status['systems']['affiliate_content_ready'] and status['systems']['visual_ready']:
        print("1. 🚀 POST VISUAL CONTENT MANUALLY NOW (immediate revenue)")
        print("2. 🤖 python3 master_integration.py (automated scaling)")
        print("3. 📊 Monitor both for optimization")
    else:
        print("1. ⚠️ Fix missing components first")
        print("2. 🔄 Re-run this integration check")
