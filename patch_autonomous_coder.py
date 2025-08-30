#!/usr/bin/env python3
import re

# Read the file
with open('claude_autonomous_coder.py', 'r') as f:
    content = f.read()

# Replace hardcoded revenue_optimization with rotation logic
rotation_logic = '''
# ROTATION FIX - Dynamic problem selection
import json
import random
import os

def get_current_problem():
    """Get current problem with rotation support"""
    try:
        # Check for forced problem
        if os.path.exists('claude_force_problem.json'):
            with open('claude_force_problem.json', 'r') as f:
                force_config = json.load(f)
            if force_config.get('rotation_active'):
                return force_config['force_problem']
        
        # Use rotation config
        if os.path.exists('claude_problem_rotation.json'):
            with open('claude_problem_rotation.json', 'r') as f:
                rotation_config = json.load(f)
            problems = rotation_config.get('available_problems', [])
            if problems:
                return random.choice(problems)
    except:
        pass
    
    # Fallback to conversion optimization
    return "conversion_rate_optimization"

current_problem = get_current_problem()
'''

# Replace any hardcoded revenue_optimization
if 'revenue_optimization' in content:
    print("✅ Found hardcoded revenue_optimization - patching...")
    
    # Replace the hardcoded problem
    content = content.replace(
        '"Implement revenue_optimization autonomously"',
        'f"Implement {current_problem} autonomously"'
    )
    content = content.replace(
        "'Implement revenue_optimization autonomously'",
        'f"Implement {current_problem} autonomously"'
    )
    
    # Add rotation logic at the top
    lines = content.split('\n')
    
    # Find where to insert rotation logic (after imports)
    insert_point = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            insert_point = i + 1
        elif line.strip() and not line.startswith('#'):
            break
    
    # Insert rotation logic
    lines.insert(insert_point, rotation_logic)
    
    # Write fixed version
    with open('claude_autonomous_coder.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ claude_autonomous_coder.py patched with rotation logic!")
else:
    print("❓ No hardcoded revenue_optimization found")
