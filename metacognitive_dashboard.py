#!/usr/bin/env python3
"""
Meta-cognitive monitoring dashboard for CLAUDE agent
"""

import json
import time
import os
from datetime import datetime

def monitor_metacognitive_health():
   """Monitor meta-cognitive health in real-time"""
   print("🧠 META-COGNITIVE MONITORING DASHBOARD")
   print("=" * 50)
   
   iteration = 0
   while iteration < 20:  # Limit to 20 iterations for demo
       try:
           iteration += 1
           print(f"🔍 Check #{iteration} - {datetime.now().strftime('%H:%M:%S')}")
           
           # Check for meta-cognitive logs
           if os.path.exists('meta_cognitive_log.json'):
               with open('meta_cognitive_log.json', 'r') as f:
                   logs = f.readlines()
               
               if logs:
                   latest_log = json.loads(logs[-1])
                   state = latest_log.get('meta_cognitive_state', 'unknown')
                   print(f"  Meta-cognitive state: {state}")
                   
                   if 'implementations' in latest_log:
                       impl_count = len(latest_log['implementations'])
                       print(f"  Recent implementations: {impl_count}")
           else:
               print("  No meta-cognitive logs yet")
           
           # Check for problem rotation
           if os.path.exists('intelligent_problem_rotation.json'):
               print("  🔄 Problem rotation: ACTIVE")
           else:
               print("  ❌ Problem rotation: NOT CONFIGURED")
           
           # Check for creative solutions
           if os.path.exists('cognitive_diversity_toolkit.json'):
               print("  🎭 Creative problem solving: READY")
           else:
               print("  ❌ Creative toolkit: NOT AVAILABLE")
           
           # Check recent solution files
           import glob
           recent_solutions = glob.glob("claude_solution_*.py")
           if recent_solutions:
               latest_solution = max(recent_solutions, key=os.path.getmtime)
               mod_time = os.path.getmtime(latest_solution)
               age_minutes = (time.time() - mod_time) / 60
               print(f"  📄 Latest solution: {latest_solution} ({age_minutes:.1f}m ago)")
           
           print("  " + "-" * 40)
           time.sleep(10)
           
       except KeyboardInterrupt:
           print("\n👋 Monitoring stopped by user")
           break
       except Exception as e:
           print(f"  ❌ Monitoring error: {e}")
           time.sleep(5)
   
   print("📊 Monitoring session completed")

if __name__ == "__main__":
   monitor_metacognitive_health()
