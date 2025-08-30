#!/usr/bin/env python3
"""
Ask your specific CEO and Claude agents the domain/product questions
"""

import json
import subprocess
from datetime import datetime

def identify_correct_agents():
    """Find the correct agent files"""
    
    agents_found = {
        "ceo_agents": [],
        "claude_agents": [],
        "orchestrator_agents": []
    }
    
    import os
    
    # Find CEO agents
    for file in os.listdir('.'):
        if 'ceo' in file.lower() and file.endswith('.py'):
            agents_found["ceo_agents"].append(file)
    
    # Find Claude agents  
    for file in os.listdir('.'):
        if 'claude' in file.lower() and file.endswith('.py'):
            agents_found["claude_agents"].append(file)
            
    # Find orchestrator agents
    for file in os.listdir('.'):
        if any(keyword in file.lower() for keyword in ['orchestrator', 'coordinator']):
            if file.endswith('.py'):
                agents_found["orchestrator_agents"].append(file)
    
    return agents_found

def create_ceo_consultation():
    """Create CEO agent consultation"""
    
    ceo_question = {
        "timestamp": datetime.now().isoformat(),
        "consultation_type": "STRATEGIC_DOMAIN_AND_PRODUCT_DECISION",
        "urgency": "IMMEDIATE",
        "agent_target": "ULTIMATE_CEO_AGENT",
        
        "strategic_questions": {
            "domain_strategy": {
                "situation": "wealthyrobot.com is taken - need alternative",
                "options": [
                    {
                        "domain": "wealthyrobot.ai",
                        "cost": "$70/year",
                        "pros": "Perfect brand match, AI credibility, premium positioning",
                        "cons": "Higher cost"
                    },
                    {
                        "domain": "thewealthyrobot.com", 
                        "cost": "$11/year",
                        "pros": "Brand consistency, authority, standard cost",
                        "cons": "Slightly longer"
                    },
                    {
                        "domain": "OTHER_SUGGESTION",
                        "cost": "VARIES",
                        "pros": "CEO to suggest alternatives",
                        "cons": "Unknown"
                    }
                ],
                "question": "Which domain gives us the best strategic positioning for building authority and maximizing conversions in the AI automation niche?"
            },
            
            "product_monetization_strategy": {
                "situation": "Need to choose optimal affiliate products for revenue",
                "options": [
                    {
                        "category": "ClickBank Products",
                        "commission": "50-75%",
                        "pros": "High commissions, instant approval",
                        "cons": "Lower quality, potential brand damage"
                    },
                    {
                        "category": "SaaS/Business Tools",
                        "commission": "25-40% recurring",
                        "pros": "High quality, recurring revenue, brand alignment",
                        "cons": "Lower commission percentage"
                    },
                    {
                        "category": "Premium Courses/Training",
                        "commission": "30-50%",
                        "pros": "High value, good commissions, authority building",
                        "cons": "Longer sales cycles"
                    }
                ],
                "question": "What product strategy maximizes both immediate revenue and long-term brand building for our AI automation empire?"
            }
        },
        
        "required_ceo_analysis": [
            "ROI projection for each option",
            "Risk assessment and mitigation",
            "Brand positioning impact",
            "Market opportunity evaluation",
            "Budget allocation recommendation",
            "Timeline for implementation",
            "Success metrics definition"
        ],
        
        "expected_deliverable": "Strategic recommendation with business case"
    }
    
    # Save CEO consultation
    with open('ceo_strategic_consultation.json', 'w') as f:
        json.dump(ceo_question, f, indent=2)
    
    return ceo_question

def create_claude_consultation():
    """Create Claude agent consultation"""
    
    claude_question = {
        "timestamp": datetime.now().isoformat(),
        "consultation_type": "TECHNICAL_IMPLEMENTATION_ANALYSIS",
        "urgency": "IMMEDIATE", 
        "agent_target": "CLAUDE_AUTONOMOUS_AGENT",
        
        "technical_questions": {
            "domain_technical_analysis": {
                "situation": "Need technical assessment of domain alternatives",
                "evaluation_criteria": [
                    "SEO impact and ranking potential",
                    "Technical implementation complexity",
                    "User experience and memorability",
                    "Integration with existing systems",
                    "Scalability for future growth"
                ],
                "options": [
                    {
                        "domain": "wealthyrobot.ai",
                        "technical_factors": "Premium extension, AI relevance, higher cost"
                    },
                    {
                        "domain": "thewealthyrobot.com",
                        "technical_factors": "Standard extension, longer name, standard cost"
                    }
                ],
                "question": "Which domain provides optimal technical performance for SEO, user experience, and system integration?"
            },
            
            "affiliate_implementation_analysis": {
                "situation": "Need technical assessment of affiliate product integration",
                "evaluation_criteria": [
                    "API quality and tracking capabilities",
                    "Implementation complexity",
                    "Analytics and reporting features", 
                    "Compliance and technical requirements",
                    "Performance optimization potential"
                ],
                "options": [
                    {
                        "category": "ClickBank Integration",
                        "technical_factors": "Simple setup, basic tracking, compliance challenges"
                    },
                    {
                        "category": "SaaS Tool APIs",
                        "technical_factors": "Advanced APIs, detailed tracking, complex setup"
                    },
                    {
                        "category": "Premium Affiliate Networks",
                        "technical_factors": "Professional APIs, comprehensive analytics, approval required"
                    }
                ],
                "question": "Which affiliate approach provides the best technical implementation for tracking, optimization, and scalability?"
            }
        },
        
        "required_claude_analysis": [
            "SEO impact assessment",
            "Technical implementation roadmap", 
            "Performance optimization strategy",
            "Integration complexity evaluation",
            "Scalability and maintenance considerations",
            "Tracking and analytics capabilities",
            "Security and compliance factors"
        ],
        
        "expected_deliverable": "Technical recommendation with implementation plan"
    }
    
    # Save Claude consultation
    with open('claude_technical_consultation.json', 'w') as f:
        json.dump(claude_question, f, indent=2)
    
    return claude_question

if __name__ == "__main__":
    print("🎯 CREATING SPECIFIC AGENT CONSULTATIONS")
    print("=======================================")
    
    # Identify agents
    agents = identify_correct_agents()
    
    print("📋 AGENTS IDENTIFIED:")
    print("====================")
    print(f"CEO Agents: {agents['ceo_agents']}")
    print(f"Claude Agents: {agents['claude_agents']}")
    print(f"Orchestrator Agents: {agents['orchestrator_agents']}")
    
    # Create consultations
    ceo_consultation = create_ceo_consultation()
    claude_consultation = create_claude_consultation()
    
    print("\n✅ CONSULTATION FILES CREATED:")
    print("=============================")
    print("• ceo_strategic_consultation.json")
    print("• claude_technical_consultation.json")
    
    print("\n🎯 NEXT STEPS:")
    print("=============")
    print("1. Check which specific agent files you have")
    print("2. Run the correct agent with consultation files")
    print("3. Collect their responses")
    print("4. Get unified decision")
