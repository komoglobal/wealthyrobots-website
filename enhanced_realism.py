#!/usr/bin/env python3
"""
Enhanced realism: Add random delays and occasional variations
"""

content_variations = '''
# Additional human-like behaviors:
# - Sometimes skip a cycle (2% chance) - like humans forget
# - Occasionally post slightly earlier when "inspired" 
# - Add weekend vs weekday variations
# - Slightly different intervals during business hours vs nights

import random
from datetime import datetime

def get_human_like_interval():
    """Get posting interval that mimics human behavior"""
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()  # 0=Monday, 6=Sunday
    
    base_hours = 6
    
    # Weekend variation (slightly more relaxed)
    if day_of_week >= 5:  # Weekend
        base_hours = random.uniform(5.8, 6.4)
    
    # Business hours vs off-hours
    if 9 <= hour <= 17:  # Business hours - more active
        variation = random.randint(-45, +15)  # Slightly earlier during work
    else:  # Off hours - more relaxed
        variation = random.randint(-15, +45)  # Might be delayed
    
    # Occasional "inspiration" posts (5% chance to post earlier)
    if random.random() < 0.05:
        base_hours *= 0.7  # Post 30% earlier when "inspired"
    
    # Rare skip cycle (2% chance to wait longer)
    if random.random() < 0.02:
        base_hours *= 1.5  # Wait 50% longer occasionally
    
    return timedelta(hours=base_hours, minutes=variation)
'''

print("📝 Enhanced realism features available:")
print("   • Weekend vs weekday timing")
print("   • Business hours awareness") 
print("   • Occasional 'inspiration' posts")
print("   • Rare skip cycles (like humans forget)")
print("   • Dynamic variation based on time of day")
