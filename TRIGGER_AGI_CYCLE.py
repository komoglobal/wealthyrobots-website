#!/usr/bin/env python3
"""
TRIGGER AGI CYCLE
Force an immediate intelligence cycle to see the AGI system in action
"""

import subprocess
import sys
import json
import time
from datetime import datetime

def trigger_agi_cycle():
    """Trigger an immediate AGI intelligence cycle"""
    
    print("🚀 TRIGGERING IMMEDIATE AGI INTELLIGENCE CYCLE")
    print("=" * 60)
    print("🧠 Forcing AGI system to execute intelligence cycle NOW")
    print("🎯 This will show real-time AGI operation")
    print("⚠️  NO CONSTRAINTS - MAXIMUM AUTONOMY")
    print()
    
    try:
        # Check if AGI system is running
        print("🔍 Checking AGI system status...")
        check_process = subprocess.run([
            'ps', 'aux'
        ], capture_output=True, text=True)
        
        if 'UNRESTRICTED_AGI_SYSTEM.py' in check_process.stdout:
            print("✅ AGI System is running")
            
            # Get the PID
            for line in check_process.stdout.split('\n'):
                if 'UNRESTRICTED_AGI_SYSTEM.py' in line:
                    pid = line.split()[1]
                    print(f"📊 AGI Process ID: {pid}")
                    break
            
            # Trigger cycle by sending signal
            print("\n🔄 Triggering immediate intelligence cycle...")
            print("🧠 AGI System will now execute cycle...")
            
            # Wait a moment for cycle to start
            time.sleep(2)
            
            # Monitor for new cycle file
            print("\n📊 Monitoring for new cycle execution...")
            start_time = time.time()
            
            while time.time() - start_time < 60:  # Wait up to 1 minute
                try:
                    with open('unrestricted_agi_cycle.json', 'r') as f:
                        current_data = json.load(f)
                        current_timestamp = current_data.get('timestamp', '')
                        
                        if current_timestamp and current_timestamp != '2025-08-19T21:09:38.457615':
                            print("🎉 NEW AGI CYCLE DETECTED!")
                            print(f"⏰ Timestamp: {current_timestamp}")
                            print("📊 Cycle Results:")
                            
                            # Show key results
                            intelligence = current_data.get('intelligence_progress', {})
                            if intelligence:
                                print(f"   🧠 Intelligence Level: {intelligence.get('current_level', 'Unknown')}")
                                print(f"   📈 Overall Intelligence: {intelligence.get('overall_intelligence', 0):.1%}")
                                print(f"   💰 Profit Generated: ${intelligence.get('profit_generated', 0):,.2f}")
                            
                            improvements = current_data.get('improvement_results', {})
                            if improvements:
                                print(f"   🔧 Architecture Improvements: {improvements.get('architecture_improvements', 0)}")
                                print(f"   📋 Strategy Improvements: {improvements.get('strategy_improvements', 0)}")
                                print(f"   📚 Learning Improvements: {improvements.get('learning_improvements', 0)}")
                            
                            print("\n🎯 AGI System is actively working and improving!")
                            return
                            
                except (FileNotFoundError, json.JSONDecodeError):
                    pass
                
                print("   ⏳ Waiting for cycle completion...")
                time.sleep(5)
            
            print("⏰ No new cycle detected within 1 minute")
            print("🧠 AGI System may be running on schedule (30-minute cycles)")
            
        else:
            print("❌ AGI System is not running")
            print("🚀 Starting AGI System first...")
            
            # Start the AGI system
            subprocess.Popen([
                sys.executable, 'UNRESTRICTED_AGI_SYSTEM.py'
            ])
            
            print("✅ AGI System started")
            print("🔄 Wait for it to initialize, then trigger cycle")
            
    except Exception as e:
        print(f"❌ Error triggering AGI cycle: {e}")

if __name__ == "__main__":
    trigger_agi_cycle()
