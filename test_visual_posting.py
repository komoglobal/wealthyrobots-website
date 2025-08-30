#!/usr/bin/env python3
"""
Test posting with visual content integration
"""

from social_media_agent import SocialMediaAgent
import os

# Check available visuals
print("🎨 Available visual content:")
visuals = [f for f in os.listdir('.') if f.endswith('.png') and ('graphic' in f or 'visual' in f)]
for v in visuals[:3]:
    print(f"  • {v}")

# Test the agent with visual integration
agent = SocialMediaAgent()

# Test visual detection
visual = agent.get_visual_content()
print(f"🖼️ Agent found visual: {visual}")

# Post with current content
print("\n🧪 Testing enhanced posting...")
result = agent.run_cycle()
print(f"📊 Result: {result}")
