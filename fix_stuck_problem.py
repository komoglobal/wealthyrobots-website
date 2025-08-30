#!/usr/bin/env python3
"""
Direct patch to fix stuck revenue_optimization problem
"""

import os
import re

def patch_file(filename, old_pattern, new_text):
    """Patch a file to replace stuck problem"""
    if not os.path.exists(filename):
        print(f"❌ {filename} not found")
        return False
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Look for the stuck pattern
        if old_pattern in content:
            print(f"✅ Found stuck pattern in {filename}")
            
            # Replace with rotation logic
            new_content = content.replace(old_pattern, new_text)
            
            # Backup original
            with open(f"{filename}.backup", 'w') as f:
                f.write(content)
            
            # Write fixed version
            with open(filename, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Patched {filename} (backup saved)")
            return True
        else:
            print(f"❓ Pattern not found in {filename}")
            return False
            
    except Exception as e:
        print(f"❌ Error patching {filename}: {e}")
        return False

def main():
    print("🔧 DIRECT PATCH FOR STUCK PROBLEM")
    print("=" * 40)
    
    # Patterns to find and replace
    stuck_patterns = [
        '"Implement revenue_optimization autonomously"',
        "'Implement revenue_optimization autonomously'",
        "revenue_optimization",
        '"revenue_optimization"',
        "'revenue_optimization'"
    ]
    
    # Replacement with rotation logic
    rotation_replacement = '''
# ROTATION FIX - Check for forced problem
import json
try:
    if os.path.exists('claude_force_problem.json'):
        with open('claude_force_problem.json', 'r') as f:
            force_config = json.load(f)
        if force_config.get('rotation_active'):
            current_problem = force_config['force_problem']
            print(f"🔄 Using rotated problem: {current_problem}")
        else:
            current_problem = "conversion_rate_optimization"
    else:
        current_problem = "conversion_rate_optimization"
except:
    current_problem = "conversion_rate_optimization"
'''
    
    # Files to patch
    files_to_check = [
        'continuous_empire_optimizer.py',
        'empire_intelligence_agent.py', 
        'claude_full_autonomous.py'
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            print(f"\n🔍 Checking {filename}...")
            
            # Read file to see what's causing the stuck behavior
            with open(filename, 'r') as f:
                content = f.read()
            
            # Look for hardcoded revenue_optimization
            if 'revenue_optimization' in content:
                print(f"⚠️  Found hardcoded revenue_optimization in {filename}")
                
                # Show the problematic lines
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'revenue_optimization' in line:
                        print(f"   Line {i}: {line.strip()}")
                
                # Ask for manual fix guidance
                print(f"\n🔧 MANUAL FIX NEEDED for {filename}")
                print("Replace hardcoded 'revenue_optimization' with problem rotation logic")

if __name__ == "__main__":
    main()
