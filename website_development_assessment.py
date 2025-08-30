#!/usr/bin/env python3
"""
Assess empire's capability to build and manage website autonomously
"""

import json
import os
from datetime import datetime

def assess_agent_capabilities():
    """Check which agents can contribute to website development"""
    
    website_tasks = {
        "content_creation": {
            "required_agents": ["content_agent.py", "social_media_agent.py"],
            "tasks": [
                "Convert Twitter threads to articles",
                "Create landing page copy",
                "Write email sequences",
                "Generate SEO-optimized content"
            ]
        },
        "visual_design": {
            "required_agents": ["visual_content_agent.py", "ai_image_generator_agent.py"],
            "tasks": [
                "Create website graphics",
                "Design landing page visuals", 
                "Generate article images",
                "Brand consistency"
            ]
        },
        "technical_development": {
            "required_agents": ["claude_full_autonomous_fixed.py", "code_debug_agent.py"],
            "tasks": [
                "Generate HTML/CSS code",
                "Set up email integrations",
                "Create responsive design",
                "Debug technical issues"
            ]
        },
        "seo_optimization": {
            "required_agents": ["seo_optimizer_agent.py", "content_optimizer_agent.py"],
            "tasks": [
                "Keyword research and optimization",
                "Meta tags and descriptions",
                "Content structure optimization",
                "Performance monitoring"
            ]
        },
        "analytics_tracking": {
            "required_agents": ["data_analytics_agent.py", "conversion_tracker_agent.py"],
            "tasks": [
                "Set up Google Analytics",
                "Track conversion rates",
                "Monitor traffic sources",
                "Performance reporting"
            ]
        },
        "revenue_optimization": {
            "required_agents": ["smart_affiliate_agent.py", "revenue_booster_agent.py"],
            "tasks": [
                "Integrate affiliate links",
                "Optimize conversion funnels",
                "A/B test offers",
                "Revenue tracking"
            ]
        }
    }
    
    # Check which agents are available
    available_agents = []
    missing_agents = []
    
    for category, info in website_tasks.items():
        category_agents = {"available": [], "missing": []}
        
        for agent in info["required_agents"]:
            if os.path.exists(agent):
                available_agents.append(agent)
                category_agents["available"].append(agent)
            else:
                missing_agents.append(agent)
                category_agents["missing"].append(agent)
        
        website_tasks[category]["agent_status"] = category_agents
    
    return website_tasks, available_agents, missing_agents

def create_website_development_plan():
    """Create development plan using available agents"""
    
    tasks, available, missing = assess_agent_capabilities()
    
    development_plan = {
        "timestamp": datetime.now().isoformat(),
        "empire_readiness": "HIGH" if len(missing) <= 3 else "MEDIUM" if len(missing) <= 6 else "LOW",
        "available_agents": len(available),
        "missing_agents": len(missing),
        "development_phases": {
            "phase_1_setup": {
                "duration": "Week 1",
                "agents_involved": ["claude", "ceo", "orchestrator"],
                "tasks": [
                    "Domain registration and hosting setup",
                    "Basic website structure planning",
                    "Content strategy development",
                    "Email service integration"
                ]
            },
            "phase_2_content": {
                "duration": "Week 2-3", 
                "agents_involved": ["content_agent", "visual_content_agent", "seo_optimizer"],
                "tasks": [
                    "Convert best Twitter threads to articles",
                    "Create landing page content",
                    "Generate website graphics",
                    "SEO optimization"
                ]
            },
            "phase_3_optimization": {
                "duration": "Week 4+",
                "agents_involved": ["analytics", "conversion_tracker", "revenue_booster"],
                "tasks": [
                    "Set up tracking and analytics",
                    "A/B test conversion elements",
                    "Monitor and optimize performance",
                    "Scale successful content"
                ]
            }
        },
        "autonomous_capabilities": {
            "content_generation": "HIGH - Multiple content agents available",
            "visual_creation": "HIGH - AI image and visual agents",
            "technical_development": "MEDIUM - Claude can help with code",
            "seo_optimization": "HIGH - SEO agent available", 
            "performance_tracking": "HIGH - Multiple analytics agents",
            "revenue_optimization": "HIGH - Affiliate and revenue agents"
        }
    }
    
    return development_plan

if __name__ == "__main__":
    print("🏗️ EMPIRE WEBSITE DEVELOPMENT READINESS")
    print("=======================================")
    
    tasks, available, missing = assess_agent_capabilities()
    plan = create_website_development_plan()
    
    print(f"\n📊 READINESS SCORE: {plan['empire_readiness']}")
    print(f"Available Agents: {len(available)}")
    print(f"Missing Agents: {len(missing)}")
    
    print("\n✅ AVAILABLE CAPABILITIES:")
    for category, info in tasks.items():
        available_count = len(info["agent_status"]["available"])
        total_count = len(info["required_agents"])
        if available_count > 0:
            print(f"• {category.replace('_', ' ').title()}: {available_count}/{total_count} agents ready")
    
    print("\n🚀 AUTONOMOUS DEVELOPMENT PLAN:")
    for phase, details in plan["development_phases"].items():
        print(f"\n{phase.replace('_', ' ').title()}:")
        print(f"  Duration: {details['duration']}")
        print(f"  Agents: {', '.join(details['agents_involved'])}")
        print(f"  Key Tasks: {len(details['tasks'])} planned")
    
    print("\n💡 RECOMMENDATION:")
    if plan['empire_readiness'] == "HIGH":
        print("✅ Your empire is READY to build the website autonomously!")
        print("✅ Most required agents are available and operational")
        print("✅ Can proceed with full autonomous development")
    elif plan['empire_readiness'] == "MEDIUM":
        print("⚠️ Your empire is MOSTLY ready with some gaps")
        print("✅ Core capabilities available")
        print("🔧 May need manual assistance for missing agent functions")
    else:
        print("❌ Empire needs more agents before autonomous development")
        print("🔧 Recommend building missing agents first")
    
    # Save assessment
    with open('website_readiness_assessment.json', 'w') as f:
        json.dump(plan, f, indent=2)
    
    print(f"\n📁 Assessment saved: website_readiness_assessment.json")
