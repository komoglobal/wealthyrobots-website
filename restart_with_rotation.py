#!/usr/bin/env python3
import json
import os
import subprocess
import time

# Load rotation config
try:
    with open('claude_problem_rotation.json', 'r') as f:
        rotation_config = json.load(f)
    
    print("✅ Rotation config loaded:")
    print(f"   Next problem: {rotation_config['next_problem']}")
    
    # Force the new problem into the system
    force_config = {
        "force_problem": rotation_config['next_problem'],
        "skip_current": True,
        "rotation_active": True,
        "timestamp": rotation_config['timestamp']
    }
    
    with open('claude_force_problem.json', 'w') as f:
        json.dump(force_config, f, indent=2)
    
    print("✅ Force config created")
    
except Exception as e:
    print(f"Error: {e}")

# Start agents with rotation awareness
print("🚀 Starting agents with rotation...")
time.sleep(2)

# Start empire with forced problem rotation
subprocess.Popen(['python3', 'continuous_empire_optimizer.py'], 
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.Popen(['python3', 'empire_intelligence_agent.py'],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✅ Agents restarted with rotation config")
print("📊 Monitor: watch 'grep Problem claude_solution_*.py | tail -3'")
