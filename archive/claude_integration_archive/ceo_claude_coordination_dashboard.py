#!/usr/bin/env python3
"""
CEO-CLAUDE coordination monitoring dashboard
"""

import json
import time
import os
from datetime import datetime

def monitor_ceo_claude_coordination():
   """Monitor CEO-CLAUDE coordination in real-time"""
   print("🤝 CEO-CLAUDE COORDINATION DASHBOARD")
   print("=" * 50)
   
   iteration = 0
   while iteration < 15:  # Monitor for 15 iterations
       try:
           iteration += 1
           print(f"📊 Coordination Check #{iteration} - {datetime.now().strftime('%H:%M:%S')}")
           
           # Check CEO strategic status
           if os.path.exists('strategic_business_log.json'):
               with open('strategic_business_log.json', 'r') as f:
                   logs = f.readlines()
               if logs:
                   latest_log = json.loads(logs[-1])
                   state = latest_log.get('business_intelligence_state', 'unknown')
                   print(f"  👑 CEO Strategic State: {state}")
                   impl_count = len(latest_log.get('implementations', []))
                   print(f"  📈 Strategic Implementations: {impl_count}")
           else:
               print("  👑 CEO Strategic State: No logs yet")
           
           # Check CLAUDE meta-cognitive status
           if os.path.exists('meta_cognitive_log.json'):
               with open('meta_cognitive_log.json', 'r') as f:
                   logs = f.readlines()
               if logs:
                   latest_log = json.loads(logs[-1])
                   state = latest_log.get('meta_cognitive_state', 'unknown')
                   print(f"  🧠 CLAUDE Meta-Cognitive: {state}")
           else:
               print("  🧠 CLAUDE Meta-Cognitive: No logs yet")
           
           # Check coordination status
           if os.path.exists('ceo_claude_coordination.json'):
               with open('ceo_claude_coordination.json', 'r') as f:
                   coordination = json.load(f)
               status = coordination.get('coordination_status', 'unknown')
               print(f"  🤝 Coordination Status: {status}")
           else:
               print("  🤝 Coordination Status: Not established")
           
           # Check strategic directives
           if os.path.exists('strategic_directives_for_claude.json'):
               with open('strategic_directives_for_claude.json', 'r') as f:
                   directives = json.load(f)
               directive_count = len(directives.get('directives', []))
               print(f"  📋 Active Directives: {directive_count}")
           else:
               print("  📋 Active Directives: None")
           
           # Check business strategy files
           strategy_files = [
               'market_expansion_strategy.json',
               'product_innovation_plan.json', 
               'business_model_transformation.json'
           ]
           
           active_strategies = sum(1 for f in strategy_files if os.path.exists(f))
           print(f"  🚀 Active Strategies: {active_strategies}/3")
           
           print("  " + "-" * 40)
           time.sleep(10)
           
       except KeyboardInterrupt:
           print("\n👋 Coordination monitoring stopped")
           break
       except Exception as e:
           print(f"  ❌ Monitoring error: {e}")
           time.sleep(5)
   
   print("📊 Coordination monitoring session completed")

if __name__ == "__main__":
   monitor_ceo_claude_coordination()
