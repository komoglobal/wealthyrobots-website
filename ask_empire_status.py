#!/usr/bin/env python3
"""
Empire Consultation System - Ask what your empire needs
"""

import json
import os
import glob
from datetime import datetime
from claude_autonomous_coder import ClaudeAutonomousCoder

def ask_empire_what_it_needs():
    print("🏰 EMPIRE CONSULTATION SESSION")
    print("=" * 40)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n👑 Consulting with your autonomous empire...")
    
    # 1. Ask Claude for empire analysis
    print("\n🤖 CONSULTING CLAUDE:")
    print("=" * 25)
    
    claude = ClaudeAutonomousCoder()
    needs = claude.analyze_empire_needs()
    
    print("🧠 Claude's Empire Assessment:")
    print(f"  📊 Missing capabilities: {len(needs.get('missing_agents', []))}")
    print(f"  ⚡ Optimization opportunities: {len(needs.get('optimization_opportunities', []))}")
    print(f"  🚀 Growth opportunities: {len(needs.get('new_capabilities_needed', []))}")
    
    # 2. Check CEO recommendations
    print("\n👑 CONSULTING CEO:")
    print("=" * 18)
    
    if os.path.exists('ultimate_ceo_report.json'):
        with open('ultimate_ceo_report.json', 'r') as f:
            ceo_report = json.load(f)
        
        print("💼 CEO's Current Assessment:")
        print(f"  💰 Monthly Revenue: ${ceo_report.get('monthly_revenue', 0)}")
        print(f"  🎯 Business Stage: {ceo_report.get('business_stage', 'Unknown')}")
        print(f"  ⚡ Recent Actions: {ceo_report.get('autonomous_actions', 0)}")
        
        # CEO recommendations
        revenue = ceo_report.get('monthly_revenue', 0)
        if revenue < 100:
            print("  👑 CEO says: 'Focus on revenue optimization'")
        elif revenue < 500:
            print("  👑 CEO says: 'Scale operations for growth'")
        else:
            print("  👑 CEO says: 'Expand to new markets'")
    else:
        print("  ⚠️ CEO report not available")
    
    # 3. Check system health
    print("\n🔧 SYSTEM HEALTH CHECK:")
    print("=" * 23)
    
    agent_count = len(glob.glob('*_agent.py'))
    recent_posts = len(glob.glob('smart_viral_thread*.txt'))
    
    print("🏥 Empire Health Status:")
    print(f"  🤖 Total Agents: {agent_count}")
    print(f"  📱 Content Pieces: {recent_posts}")
    
    # Check for issues
    issues = []
    if agent_count < 30:
        issues.append("Agent count below optimal")
    if recent_posts < 5:
        issues.append("Low content generation")
    
    if issues:
        print("  ⚠️ Issues detected:")
        for issue in issues:
            print(f"    • {issue}")
    else:
        print("  ✅ All systems healthy")
    
    # 4. Generate action recommendations
    print("\n🎯 WHAT YOUR EMPIRE NEEDS FROM YOU:")
    print("=" * 35)
    
    actions_needed = []
    
    # Based on Claude's analysis
    if needs.get('optimization_opportunities'):
        for opportunity in needs['optimization_opportunities']:
            actions_needed.append(f"🔧 Let Claude implement: {opportunity}")
    
    # Based on missing capabilities
    if needs.get('missing_agents'):
        actions_needed.append(f"🤖 Let Claude create missing agents")
    
    # Based on system health
    if issues:
        actions_needed.append("🏥 Review system health issues")
    
    # Based on revenue
    if os.path.exists('ultimate_ceo_report.json'):
        with open('ultimate_ceo_report.json', 'r') as f:
            ceo_data = json.load(f)
        
        revenue = ceo_data.get('monthly_revenue', 0)
        if revenue < 100:
            actions_needed.append("💰 Enable revenue optimization strategies")
    
    # Check Twitter status
    if not any('twitter' in f.lower() for f in os.listdir('.')):
        actions_needed.append("📱 Set up Twitter API credentials for real posting")
    
    if actions_needed:
        print("📋 ACTION ITEMS FOR YOU:")
        for i, action in enumerate(actions_needed, 1):
            print(f"  {i}. {action}")
    else:
        print("✅ NO ACTION NEEDED - Empire is self-sufficient!")
        print("🤖 Your autonomous empire is handling everything")
    
    # 5. Quick actions you can take
    print("\n⚡ QUICK ACTIONS YOU CAN TAKE:")
    print("=" * 30)
    
    quick_actions = [
        "🔄 python3 live_orchestrator.py  # Start/restart empire",
        "🤖 python3 claude_autonomous_coder.py  # Let Claude optimize",
        "👑 cat ultimate_ceo_report.json  # Review CEO decisions",
        "📱 Check @WealthyRobot on Twitter  # See your posts",
        "📊 python3 claude_activity_monitor.py  # Monitor Claude"
    ]
    
    for action in quick_actions:
        print(f"  {action}")
    
    print(f"\n🏆 EMPIRE STATUS: AUTONOMOUS AND OPERATIONAL")
    print(f"🎯 Your empire mostly runs itself!")

if __name__ == "__main__":
    ask_empire_what_it_needs()
