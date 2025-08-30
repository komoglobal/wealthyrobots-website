#!/usr/bin/env python3

def fix_optimization_variable():
    print("🔧 Fixing optimization variable in claude_full_autonomous.py...")
    
    with open('claude_full_autonomous.py', 'r') as f:
        content = f.read()
    
    # Backup
    with open('claude_full_autonomous.py.backup3', 'w') as f:
        f.write(content)
    
    # Find and replace the hardcoded optimization
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Look for the line that assigns optimization variable
        if 'optimization = decision[' in line or "optimization = 'revenue_optimization'" in line:
            print(f"Found optimization assignment at line {i+1}: {line.strip()}")
            
            # Replace with rotation logic
            rotation_code = '''                    # ROTATION FIX - Get rotated optimization
                    import json
                    import random
                    try:
                        if os.path.exists('claude_force_problem.json'):
                            with open('claude_force_problem.json', 'r') as f:
                                config = json.load(f)
                            if config.get('rotation_active'):
                                optimization = config['force_problem']
                            else:
                                optimization = 'conversion_rate_optimization'
                        elif os.path.exists('claude_problem_rotation.json'):
                            with open('claude_problem_rotation.json', 'r') as f:
                                config = json.load(f)
                            problems = config.get('available_problems', ['conversion_rate_optimization'])
                            optimization = random.choice(problems)
                        else:
                            optimization = 'conversion_rate_optimization'
                    except:
                        optimization = 'conversion_rate_optimization'
                    
                    print(f"🔄 Using rotated optimization: {optimization}")'''
            
            lines[i] = rotation_code
            break
    else:
        # If no direct assignment found, look for where decisions come from
        print("Looking for decision source...")
        for i, line in enumerate(lines):
            if "decision['optimization']" in line:
                print(f"Found decision usage at line {i+1}: {line.strip()}")
                # Insert rotation logic before this line
                rotation_code = '''                # ROTATION FIX - Override decision optimization
                import json
                import random
                try:
                    if os.path.exists('claude_force_problem.json'):
                        with open('claude_force_problem.json', 'r') as f:
                            config = json.load(f)
                        if config.get('rotation_active'):
                            decision['optimization'] = config['force_problem']
                    elif os.path.exists('claude_problem_rotation.json'):
                        with open('claude_problem_rotation.json', 'r') as f:
                            config = json.load(f)
                        problems = config.get('available_problems', ['conversion_rate_optimization'])
                        decision['optimization'] = random.choice(problems)
                    else:
                        decision['optimization'] = 'conversion_rate_optimization'
                except:
                    decision['optimization'] = 'conversion_rate_optimization'
                print(f"🔄 Overrode decision optimization: {decision['optimization']}")
'''
                lines.insert(i, rotation_code)
                break
    
    # Write the fixed version
    with open('claude_full_autonomous.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Fixed optimization variable with rotation logic!")

if __name__ == "__main__":
    fix_optimization_variable()
