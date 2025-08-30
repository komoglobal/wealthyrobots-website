#!/usr/bin/env python3
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
