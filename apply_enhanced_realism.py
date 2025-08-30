#!/usr/bin/env python3
"""
Apply enhanced human-like behaviors to the orchestrator
"""

import re

# Read the current orchestrator
with open('live_orchestrator.py', 'r') as f:
    content = f.read()

# Find and replace the should_create_content method with advanced logic
old_method = r'def should_create_content\(self\):.*?return time_since_last > required_interval'

new_method = '''def should_create_content(self):
        """Determine if it's time to create new content with enhanced human-like behavior"""
        import random
        from datetime import datetime, timedelta
        import glob
        import os
        
        # Check last content creation time
        recent_files = glob.glob('smart_viral_thread_*.txt')
        if not recent_files:
            return True
        
        # Get most recent file
        most_recent = max(recent_files, key=os.path.getctime)
        file_time = datetime.fromtimestamp(os.path.getctime(most_recent))
        time_since_last = datetime.now() - file_time
        
        # Enhanced human-like behavior
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        
        # Base interval
        base_hours = 6
        
        # Weekend variation (slightly more relaxed)
        if day_of_week >= 5:  # Weekend
            base_hours = random.uniform(5.8, 6.4)
            print("📅 Weekend mode: Relaxed timing")
        
        # Business hours vs off-hours
        if 9 <= hour <= 17:  # Business hours - more active
            variation = random.randint(-45, +15)  # Slightly earlier during work
            print("💼 Business hours: More active posting")
        else:  # Off hours - more relaxed
            variation = random.randint(-15, +45)  # Might be delayed
            print("🌙 Off hours: Relaxed posting")
        
        # Occasional "inspiration" posts (5% chance to post earlier)
        if random.random() < 0.05:
            base_hours *= 0.7  # Post 30% earlier when "inspired"
            print("💡 Inspiration mode: Posting earlier!")
        
        # Rare skip cycle (2% chance to wait longer)
        if random.random() < 0.02:
            base_hours *= 1.5  # Wait 50% longer occasionally
            print("😴 Skip cycle: Taking a longer break")
        
        required_interval = timedelta(hours=base_hours, minutes=variation)
        
        # Debug info
        next_post_time = file_time + required_interval
        print(f"⏰ Last post: {file_time.strftime('%H:%M:%S')}")
        print(f"🎯 Next post window: {next_post_time.strftime('%H:%M:%S')} (±variation)")
        print(f"📊 Time until next: {str(required_interval - time_since_last).split('.')[0]}")
        
        return time_since_last > required_interval'''

# Apply the enhanced method
new_content = re.sub(old_method, new_method, content, flags=re.DOTALL)

# Save the enhanced version
with open('live_orchestrator.py', 'w') as f:
    f.write(new_content)

print("✅ ENHANCED REALISM APPLIED!")
print("=" * 50)
print("🎯 New human-like behaviors:")
print("   • Weekend vs weekday timing")
print("   • Business hours awareness (9 AM - 5 PM)")
print("   • 5% chance for 'inspiration' posts (30% earlier)")
print("   • 2% chance to skip cycles (like humans forget)")
print("   • Dynamic timing based on time of day")
print("   • Detailed debug info for monitoring")
print("")
print("🎊 Your empire now behaves like a real human!")
