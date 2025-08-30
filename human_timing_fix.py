#!/usr/bin/env python3
"""
Add human-like randomization to orchestrator timing
"""

import re

# Read the current orchestrator
with open('live_orchestrator.py', 'r') as f:
    content = f.read()

# Replace the fixed 6-hour timing with randomized timing
old_pattern = r'return time_since_last > timedelta\(hours=6\)'
new_pattern = '''# Human-like timing: 5.5 to 6.5 hours with random buffer
        import random
        base_hours = 6
        variation_minutes = random.randint(-30, +30)  # ±30 min variation
        required_interval = timedelta(hours=base_hours, minutes=variation_minutes)
        return time_since_last > required_interval'''

# Apply the fix
new_content = re.sub(old_pattern, new_pattern, content)

# Save the human-like version
with open('live_orchestrator.py', 'w') as f:
    f.write(new_content)

print("✅ Added human-like timing variation:")
print("   • Base interval: 6 hours")  
print("   • Random variation: ±30 minutes")
print("   • Actual range: 5.5 to 6.5 hours")
print("   • Looks more natural and human!")
