#!/usr/bin/env python3

def fix_needs_analysis():
    print("🔧 Fixing optimization_opportunities in analyze_empire_needs...")
    
    with open('claude_autonomous_coder.py', 'r') as f:
        content = f.read()
    
    # Backup
    with open('claude_autonomous_coder.py.backup4', 'w') as f:
        f.write(content)
    
    # Find the line that adds revenue_optimization to opportunities
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if "'revenue_optimization'" in line and 'append' in line:
            print(f"Found line {i+1}: {line.strip()}")
            
            # Replace with rotation logic
            rotation_fix = '''                    # ROTATION FIX - Add rotated optimization instead of hardcoded
                    import json
                    import random
                    try:
                        if os.path.exists('claude_force_problem.json'):
                            with open('claude_force_problem.json', 'r') as f:
                                config = json.load(f)
                            if config.get('rotation_active'):
                                needs_analysis['optimization_opportunities'].append(config['force_problem'])
                            else:
                                needs_analysis['optimization_opportunities'].append('conversion_rate_optimization')
                        elif os.path.exists('claude_problem_rotation.json'):
                            with open('claude_problem_rotation.json', 'r') as f:
                                config = json.load(f)
                            problems = config.get('available_problems', ['conversion_rate_optimization'])
                            selected_problem = random.choice(problems)
                            needs_analysis['optimization_opportunities'].append(selected_problem)
                            print(f"🔄 Selected rotated optimization: {selected_problem}")
                        else:
                            needs_analysis['optimization_opportunities'].append('conversion_rate_optimization')
                    except Exception as e:
                        print(f"Rotation error: {e}")
                        needs_analysis['optimization_opportunities'].append('conversion_rate_optimization')'''
            
            lines[i] = rotation_fix
            break
    
    # Write the fixed version
    with open('claude_autonomous_coder.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Fixed needs analysis with rotation logic!")

if __name__ == "__main__":
    fix_needs_analysis()
