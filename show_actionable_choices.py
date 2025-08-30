#!/usr/bin/env python3
import subprocess
import time
import sys

def show_complete_agi_response():
    """Show the complete AGI response including actionable choices"""
    
    print("🚀 Getting Complete AGI Analysis with Actionable Choices...")
    print("=" * 80)
    
    # Start AGI Live Chat
    process = subprocess.Popen(
        ['python3', 'agi_live_chat.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Wait for initialization
    time.sleep(5)
    
    # Send the question
    question = "activate full AGI mode - what else do you need to advance intelligence and provide specific implementation suggestions\n"
    
    try:
        process.stdin.write(question)
        process.stdin.flush()
        
        print("🤖 AGI is processing your request...")
        time.sleep(15)  # Give it time to complete the full analysis
        
        # Read response
        output_lines = []
        actionable_found = False
        
        while True:
            line = process.stdout.readline()
            if not line:
                break
                
            output_lines.append(line.rstrip())
            print(line, end='')
            
            # Check for actionable choices
            if "ACTIONABLE CHOICES" in line:
                actionable_found = True
                print("\n" + "="*80)
                print("🎯 FOUND ACTIONABLE CHOICES SECTION!")
                print("="*80)
                
            # Stop when we reach the end of choices
            if actionable_found and ("Your choice" in line or "quit" in line):
                break
                
        print("\n" + "="*80)
        print("📋 SUMMARY:")
        print("="*80)
        
        if actionable_found:
            print("✅ Actionable choices were displayed above!")
            print("💡 You can now:")
            print("   • Type the number (1, 2, 3...) to select a choice")
            print("   • Type 'implement all' to implement all suggestions")
            print("   • Type 'help' for more options")
        else:
            print("❌ Actionable choices section not found in output")
            print("�� Try running the AGI Live Chat directly to see the full response")
        
        return actionable_found
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Clean up
        try:
            process.stdin.write("quit\n")
            process.stdin.flush()
            time.sleep(2)
            process.terminate()
        except:
            pass

if __name__ == "__main__":
    success = show_complete_agi_response()
    if not success:
        print("\n" + "="*80)
        print("💡 ALTERNATIVE: Run AGI Live Chat Directly")
        print("="*80)
        print("cd /home/ubuntu/wealthyrobot && python3 agi_live_chat.py")
        print("Then type: activate full AGI mode - what else do you need to advance intelligence")
        print("="*80)
