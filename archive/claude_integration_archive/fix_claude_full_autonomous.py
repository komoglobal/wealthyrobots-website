#!/usr/bin/env python3
import re
import json
import os

def fix_claude_full_autonomous():
    print("🔧 Fixing claude_full_autonomous.py...")
    
    if not os.path.exists('claude_full_autonomous.py'):
        print("❌ claude_full_autonomous.py not found")
        return
    
    # Read the file
    with open('claude_full_autonomous.py', 'r') as f:
        content = f.read()
    
    # Backup
    with open('claude_full_autonomous.py.backup2', 'w') as f:
        f.write(content)
    
    # Find hardcoded revenue_optimization and replace with rotation logic
    rotation_fix = '''
    # ROTATION FIX - Dynamic problem selection
    def get_rotated_problem():
        import json
        import random
        try:
            if os.path.exists('claude_force_problem.json'):
                with open('claude_force_problem.json', 'r') as f:
                    config = json.load(f)
                if config.get('rotation_active'):
                    return f"Implement {config['force_problem']} autonomously"
            
            if os.path.exists('claude_problem_rotation.json'):
                with open('claude_problem_rotation.json', 'r') as f:
                    config = json.load(f)
                problems = config.get('available_problems', [])
                if problems:
                    problem = random.choice(problems)
                    return f"Implement {problem} autonomously"
        except:
            pass
        return "Implement conversion_rate_optimization autonomously"
    '''
    
    # Look for hardcoded problem strings
    patterns_to_replace = [
        '"Implement revenue_optimization autonomously"',
        "'Implement revenue_optimization autonomously'",
        '"revenue_optimization"',
        "'revenue_optimization'"
    ]
    
    found_patterns = False
    for pattern in patterns_to_replace:
        if pattern in content:
            print(f"✅ Found pattern: {pattern}")
            found_patterns = True
            # Replace with rotation call
            content = content.replace(pattern, 'get_rotated_problem()')
    
    if found_patterns:
        # Add rotation function at the top after imports
        lines = content.split('\n')
        import_end = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_end = i + 1
        
        lines.insert(import_end, rotation_fix)
        
        # Write fixed version
        with open('claude_full_autonomous.py', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ claude_full_autonomous.py patched with rotation!")
    else:
        print("❓ No hardcoded patterns found - looking for other sources...")
        
        # Show problem sources
        for i, line in enumerate(lines, 1):
            if 'revenue_optimization' in line.lower():
                print(f"Line {i}: {line.strip()}")

if __name__ == "__main__":
    fix_claude_full_autonomous()
