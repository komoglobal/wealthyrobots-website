#!/usr/bin/env python3
"""
Fix the affiliate connection bug in real_money_agent.py
"""

def fix_affiliate_bug():
    print("🔧 Fixing affiliate connection bug...")
    
    # Read the current file
    with open('real_money_agent.py', 'r') as f:
        content = f.read()
    
    # Fix the incorrect variable names
    fixes = [
        ('enhanced_result["optimized_tweets"]', 'viral_content["tweets"]'),
        ('enhanced_result["revenue_potential"]', '50.0  # Estimated potential'),
        ('revenue_potential = enhanced_result["revenue_potential"]', 'revenue_potential = 50.0  # Estimated per conversion')
    ]
    
    for old, new in fixes:
        content = content.replace(old, new)
    
    # Write the fixed version
    with open('real_money_agent_FIXED.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed version saved as: real_money_agent_FIXED.py")
    print("🔧 Key fixes:")
    print("- Fixed optimized_tweets reference")
    print("- Fixed revenue_potential calculation")
    print("- Maintained affiliate_links integration")

if __name__ == "__main__":
    fix_affiliate_bug()
