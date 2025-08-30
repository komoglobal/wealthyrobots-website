#!/usr/bin/env python3
"""
Coordination between functional Claude and CEO agents
"""

import subprocess
import json
from datetime import datetime

def run_coordinated_cycle():
    """Run both agents in coordination"""
    print("🤝 RUNNING COORDINATED AGENT CYCLE")
    print("=" * 40)
    
    # Run CEO analysis first
    print("1️⃣ CEO Strategic Analysis...")
    ceo_result = subprocess.run(['python3', 'functional_ceo_agent.py'], 
                               capture_output=True, text=True)
    
    # Run Claude optimization
    print("2️⃣ Claude Technical Optimization...")
    claude_result = subprocess.run(['python3', 'functional_claude_agent.py'],
                                  capture_output=True, text=True)
    
    # Combine results
    coordination_results = {
        'timestamp': datetime.now().isoformat(),
        'ceo_output': ceo_result.stdout,
        'claude_output': claude_result.stdout,
        'coordination_success': ceo_result.returncode == 0 and claude_result.returncode == 0
    }
    
    with open('coordination_results.json', 'w') as f:
        json.dump(coordination_results, f, indent=2)
    
    print(f"🎯 Coordination Status: {'✅ Success' if coordination_results['coordination_success'] else '❌ Failed'}")
    
    return coordination_results

if __name__ == "__main__":
    run_coordinated_cycle()
