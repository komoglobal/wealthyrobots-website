#!/usr/bin/env python3

import fileinput
import sys

# Read the current claude_full_autonomous.py and update the agent selection logic
with open('claude_full_autonomous.py', 'r') as f:
    content = f.read()

# Find and replace the agent selection logic
old_pattern = 'agent_files = glob.glob(\'*_agent.py\')'
new_pattern = '''# Hybrid approach: 80% core revenue agents, 20% utility agents
            import random
            core_agents = ["content_agent.py", "smart_affiliate_agent.py", "real_money_agent.py", "social_media_agent.py"]
            utility_agents = ["data_analytics_agent.py", "visual_affiliate_agent.py", "customer_service_agent.py", "email_marketing_agent.py", "market_research_agent.py", "conversion_tracker_agent.py"]
            
            # 80% chance to pick from core agents, 20% from utility
            if random.random() < 0.8:
                agent_files = core_agents
            else:
                agent_files = utility_agents'''

# Replace the old logic with new hybrid logic
updated_content = content.replace(old_pattern, new_pattern)

# Write back to file
with open('claude_full_autonomous.py', 'w') as f:
    f.write(updated_content)

print("✅ Claude updated to hybrid approach!")
print("📊 80% focus on core revenue agents")
print("🛠️ 20% focus on utility agents")
