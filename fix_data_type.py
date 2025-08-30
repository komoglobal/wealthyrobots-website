#!/usr/bin/env python3
"""
Fix the data type mismatch in affiliate connection
"""

def fix_data_type_bug():
    print("🔧 Fixing data type mismatch...")
    
    # Read the fixed file
    with open('real_money_agent_FIXED.py', 'r') as f:
        content = f.read()
    
    # Fix the data type issue
    old_call = 'enhanced_result = enhance_with_smart_affiliates(viral_content)'
    new_call = 'enhanced_result = enhance_with_smart_affiliates(viral_content["topic"])'
    
    content = content.replace(old_call, new_call)
    
    # Write the final working version
    with open('real_money_agent_WORKING.py', 'w') as f:
        f.write(content)
    
    print("✅ Final fix applied!")
    print("🔧 Changed: enhance_with_smart_affiliates(viral_content)")
    print("🔧 To: enhance_with_smart_affiliates(viral_content['topic'])")
    print("📁 Saved as: real_money_agent_WORKING.py")

if __name__ == "__main__":
    fix_data_type_bug()
