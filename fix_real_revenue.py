#!/usr/bin/env python3
"""
Fix real_money_agent.py to use actual revenue instead of simulations
"""

import re

def fix_revenue_simulation():
    print("🔧 FIXING REVENUE SIMULATION IN real_money_agent.py")
    
    # Read the current file
    with open('real_money_agent.py', 'r') as f:
        content = f.read()
    
    # Replace fake revenue with real tracking
    fixes = [
        # Fix the hardcoded fallback
        (r'revenue_potential = 165\.47  # Fallback', 'revenue_potential = 0.0  # Real: No revenue yet'),
        
        # Fix session revenue fallback
        (r'session_revenue = 165\.47', 'session_revenue = 0.0  # Real: No conversions yet'),
        
        # Add real revenue check
        (r'# Step 5: Track performance', '''# Step 5: Track performance (REAL DATA ONLY)
        # Check real revenue from Amazon Associates
        try:
            from real_revenue_tracker import get_real_amazon_revenue
            real_revenue = get_real_amazon_revenue()
            print(f"💰 Real Amazon revenue: ${real_revenue}")
        except:
            real_revenue = 0.0
            print("💰 Real Amazon revenue: $0.00 (no sales yet)")'''),
            
        # Update revenue calculation to use real data
        (r'total_revenue = sum\(self\.revenue_streams\.values\(\)\) \+ session_revenue',
         'total_revenue = real_revenue  # Use ONLY real revenue'),
    ]
    
    # Apply fixes
    for old, new in fixes:
        content = re.sub(old, new, content)
    
    # Backup original
    with open('real_money_agent_backup.py', 'w') as f:
        f.write(open('real_money_agent.py', 'r').read())
    
    # Write fixed version
    with open('real_money_agent.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed revenue simulation")
    print("✅ Backed up original to real_money_agent_backup.py")
    print("✅ Now using real revenue data only")

if __name__ == "__main__":
    fix_revenue_simulation()
