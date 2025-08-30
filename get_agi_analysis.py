#!/usr/bin/env python3
import subprocess
import time

def get_full_agi_analysis():
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
    time.sleep(3)
    
    # Send the full AGI mode question
    question = "activate full AGI mode - what else do you need to advance intelligence and provide specific implementation suggestions\n"
    
    try:
        process.stdin.write(question)
        process.stdin.flush()
        
        # Read response
        time.sleep(2)  # Give it time to process
        
        # Try to read output
        output = ""
        while True:
            line = process.stdout.readline()
            if not line:
                break
            output += line
            print(line, end='')
            
            # Look for completion indicators
            if "ACTIONABLE CHOICES" in line or "Your choice" in line:
                break
                
        return output
        
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Clean up
        try:
            process.stdin.write("quit\n")
            process.stdin.flush()
            time.sleep(1)
            process.terminate()
        except:
            pass

if __name__ == "__main__":
    print("🚀 Getting Full AGI Intelligence Analysis...")
    result = get_full_agi_analysis()
    print("\n" + "="*70)
    print("🎯 ANALYSIS COMPLETE!")
    print("="*70)
