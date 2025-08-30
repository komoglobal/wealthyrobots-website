#!/usr/bin/env python3
"""
Monitoring dashboard for CLAUDE testing blackbox
"""

import os
import json
import time
from datetime import datetime

def monitor_blackbox_activity():
    """Monitor blackbox testing activity"""
    print("🧪 CLAUDE BLACKBOX MONITORING DASHBOARD")
    print("=" * 50)
    
    blackbox_root = "claude_blackbox_tests"
    results_dir = os.path.join(blackbox_root, "results")
    
    if not os.path.exists(results_dir):
        print("❌ Blackbox not initialized yet")
        return
    
    iteration = 0
    while iteration < 20:
        try:
            iteration += 1
            print(f"🔍 Monitor Check #{iteration} - {datetime.now().strftime('%H:%M:%S')}")
            
            # Count test results
            result_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
            print(f"  📊 Total test results: {len(result_files)}")
            
            # Show recent tests
            if result_files:
                recent_files = sorted(result_files)[-3:]
                print("  🕐 Recent tests:")
                for file in recent_files:
                    filepath = os.path.join(results_dir, file)
                    try:
                        with open(filepath, 'r') as f:
                            result = json.load(f)
                        test_name = result.get('test_name', 'unknown')
                        success = result.get('success', False)
                        status = "✅" if success else "❌"
                        print(f"    {status} {test_name}")
                    except:
                        print(f"    ❓ {file}")
            
            # Check sandbox activity
            sandbox_dir = os.path.join(blackbox_root, "sandbox")
            if os.path.exists(sandbox_dir):
                sandbox_items = os.listdir(sandbox_dir)
                print(f"  🧪 Active test environments: {len(sandbox_items)}")
            
            print("  " + "-" * 40)
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n👋 Blackbox monitoring stopped")
            break
        except Exception as e:
            print(f"  ❌ Monitor error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_blackbox_activity()
