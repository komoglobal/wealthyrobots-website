#!/usr/bin/env python3

def fix_rotation_execution():
    print("🔧 Ensuring rotation logic executes properly...")
    
    with open('claude_autonomous_coder.py', 'r') as f:
        content = f.read()
    
    # Backup
    with open('claude_autonomous_coder.py.backup5', 'w') as f:
        f.write(content)
    
    lines = content.split('\n')
    
    # Find the analyze_empire_needs method and ensure rotation logic runs
    in_method = False
    method_indent = 0
    
    for i, line in enumerate(lines):
        if 'def analyze_empire_needs(self):' in line:
            in_method = True
            method_indent = len(line) - len(line.lstrip())
            print(f"Found analyze_empire_needs at line {i+1}")
            
        elif in_method and line.strip() and not line.startswith(' ' * (method_indent + 1)) and not line.strip().startswith('#'):
            # End of method
            print(f"Method ends around line {i}")
            
            # Insert rotation logic right before the return statement
            rotation_logic = f'''
{' ' * (method_indent + 8)}# FORCED ROTATION - Always add a rotated optimization
{' ' * (method_indent + 8)}import json
{' ' * (method_indent + 8)}import random
{' ' * (method_indent + 8)}try:
{' ' * (method_indent + 12)}if os.path.exists('claude_force_problem.json'):
{' ' * (method_indent + 16)}with open('claude_force_problem.json', 'r') as f:
{' ' * (method_indent + 20)}config = json.load(f)
{' ' * (method_indent + 16)}if config.get('rotation_active'):
{' ' * (method_indent + 20)}needs_analysis['optimization_opportunities'].append(config['force_problem'])
{' ' * (method_indent + 20)}print(f"🔄 Added forced optimization: {{config['force_problem']}}")
{' ' * (method_indent + 12)}elif os.path.exists('claude_problem_rotation.json'):
{' ' * (method_indent + 16)}with open('claude_problem_rotation.json', 'r') as f:
{' ' * (method_indent + 20)}config = json.load(f)
{' ' * (method_indent + 16)}problems = config.get('available_problems', ['conversion_rate_optimization'])
{' ' * (method_indent + 16)}selected = random.choice(problems)
{' ' * (method_indent + 16)}needs_analysis['optimization_opportunities'].append(selected)
{' ' * (method_indent + 16)}print(f"🔄 Added rotated optimization: {{selected}}")
{' ' * (method_indent + 12)}else:
{' ' * (method_indent + 16)}needs_analysis['optimization_opportunities'].append('conversion_rate_optimization')
{' ' * (method_indent + 16)}print("🔄 Added default rotated optimization: conversion_rate_optimization")
{' ' * (method_indent + 8)}except Exception as e:
{' ' * (method_indent + 12)}print(f"Rotation error: {{e}}")
{' ' * (method_indent + 12)}needs_analysis['optimization_opportunities'].append('conversion_rate_optimization')
'''
            
            # Find the return statement
            for j in range(i-10, i+5):
                if j < len(lines) and 'return needs_analysis' in lines[j]:
                    lines.insert(j, rotation_logic)
                    print(f"Inserted rotation logic before return at line {j}")
                    break
            break
    
    # Write the fixed version
    with open('claude_autonomous_coder.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Fixed rotation execution logic!")

if __name__ == "__main__":
    fix_rotation_execution()
