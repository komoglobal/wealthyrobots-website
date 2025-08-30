#!/usr/bin/env python3
"""
Quick script to add EMPIRE_AGENT_INFO to existing agents
"""

import os

def add_documentation_to_agent(filename, name, purpose, category):
    """Add documentation header to an agent file"""
    
    doc_template = f'''"""
EMPIRE_AGENT_INFO:
NAME: {name}
PURPOSE: {purpose}
CATEGORY: {category}
STATUS: Active
FREQUENCY: On-demand
"""

'''
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Check if already has documentation
        if 'EMPIRE_AGENT_INFO:' in content:
            print(f"✅ {filename} already has documentation")
            return
        
        # Add documentation at the top after shebang
        lines = content.split('\n')
        insert_line = 0
        
        # Find where to insert (after shebang)
        for i, line in enumerate(lines):
            if line.startswith('#!'):
                insert_line = i + 1
                break
        
        # Insert documentation
        lines.insert(insert_line, doc_template)
        
        # Write back
        with open(filename, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Added documentation to {filename}")
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")

# Add documentation to key agents
if __name__ == "__main__":
    agents_to_document = [
        ("live_orchestrator.py", "Live Orchestrator", "Master coordinator managing all empire agents and workflows", "Core Control"),
        ("ultimate_ceo_agent.py", "Ultimate CEO Agent", "Strategic decision maker controlling budget allocation and empire strategy", "Core Control"),
        ("social_media_agent.py", "Social Media Agent", "Posts educational threads to Twitter with professional graphics and affiliate links", "Content & Social Media"),
        ("smart_affiliate_agent.py", "Smart Affiliate Agent", "Manages Amazon affiliate links and tracks conversion performance", "Revenue & Affiliate"),
        ("visual_affiliate_agent.py", "Visual Affiliate Agent", "Creates professional branded graphics and visual content for posts", "Visual & Creative"),
        ("data_analytics_agent.py", "Data Analytics Agent", "Analyzes performance metrics and provides actionable insights", "Analytics & Intelligence"),
        ("real_money_agent.py", "Real Money Agent", "Tracks actual revenue generation and financial performance", "Revenue & Affiliate"),
        ("content_agent.py", "Content Agent", "Creates educational and valuable content for the 80/20 strategy", "Content & Social Media"),
    ]
    
    print("🔧 Adding EMPIRE_AGENT_INFO to key agents...")
    for filename, name, purpose, category in agents_to_document:
        if os.path.exists(filename):
            add_documentation_to_agent(filename, name, purpose, category)
        else:
            print(f"⚠️ {filename} not found - skipping")
    
    print("\n✅ Documentation update complete!")
