#!/usr/bin/env python3
"""
Fix smart_affiliate_agent.py to return fields that real_money_agent expects
"""

def fix_smart_affiliate_return():
    print("🔧 FIXING SMART AFFILIATE RETURN STRUCTURE")
    
    # Read current file
    with open('smart_affiliate_agent.py', 'r') as f:
        content = f.read()
    
    # Backup first
    with open('smart_affiliate_agent_backup.py', 'w') as f:
        f.write(content)
    
    # Find and fix the return statement
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if "'enhanced_content':" in line:
            # Add the missing fields that real_money_agent expects
            fixed_lines.append(line)
            fixed_lines.append('        "optimized_tweets": content.split("\\n"),  # Add tweets format')
            fixed_lines.append('        "revenue_potential": 50.0,  # Estimated revenue per conversion')
        else:
            fixed_lines.append(line)
    
    # Write fixed version
    with open('smart_affiliate_agent.py', 'w') as f:
        f.write('\n'.join(fixed_lines))
    
    print("✅ Added missing fields: optimized_tweets, revenue_potential")
    print("✅ Backup saved to smart_affiliate_agent_backup.py")

if __name__ == "__main__":
    fix_smart_affiliate_return()
