#!/usr/bin/env python3
"""
Fix the key name mismatch in affiliate links
"""

def fix_key_mismatch():
    print("🔧 Fixing key name mismatch...")
    
    # Read the working file
    with open('real_money_agent_WORKING.py', 'r') as f:
        content = f.read()
    
    # Fix the key name mismatches
    fixes = [
        ("link['link']", "link['amazon_link']"),
        ("link['placement_strategy']", "link.get('placement_strategy', 'General recommendation')"),
    ]
    
    for old, new in fixes:
        content = content.replace(old, new)
    
    # Write the final version
    with open('real_money_agent_FINAL.py', 'w') as f:
        f.write(content)
    
    print("✅ Key mismatch fixed!")
    print("🔧 Changed: link['link'] → link['amazon_link']")
    print("🔧 Added: Safe key access for placement_strategy")
    print("📁 Saved as: real_money_agent_FINAL.py")

if __name__ == "__main__":
    fix_key_mismatch()
