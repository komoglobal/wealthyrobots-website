#!/usr/bin/env python3
"""
Automatically interact with AGI Live Chat
"""

import subprocess
import time
import sys
import os

def interact_with_agi():
    print("🚀 STARTING AUTOMATED AGI INTERACTION")
    print("=" * 60)
    
    # Kill any existing AGI Live Chat processes
    print("🛑 Killing existing AGI Live Chat processes...")
    os.system("pkill -f 'agi_live_chat' > /dev/null 2>&1")
    time.sleep(2)
    
    # Start AGI Live Chat
    print("🤖 Starting AGI Live Chat...")
    process = subprocess.Popen(
        [sys.executable, "agi_live_chat.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/home/ubuntu/wealthyrobot"
    )
    
    # Wait for initialization
    time.sleep(3)
    
    # Send the command
    command = "activate full AGI mode - what else do you need to advance intelligence and provide specific implementation suggestions\n"
    
    print(f"📝 Sending command: {command.strip()}")
    process.stdin.write(command)
    process.stdin.flush()
    
    # Read and display output
    print("\n📊 AGI RESPONSE:")
    print("=" * 60)
    
    # Read output for a while
    time.sleep(5)  # Give time for processing
    
    # Try to read available output
    try:
        output, error = process.communicate(timeout=10)
        print(output)
        if error:
            print("Errors:", error)
    except subprocess.TimeoutExpired:
        print("⏱️  Response taking longer, here are the actionable choices:")
        process.kill()
    
    print("=" * 60)
    print("✅ INTERACTION COMPLETE!")

if __name__ == "__main__":
    interact_with_agi()
