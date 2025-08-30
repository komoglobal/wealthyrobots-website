#!/usr/bin/env python3
"""
Direct questions to pose to your agents about website strategy
"""

questions = {
    "for_claude": [
        "What specific website features would best support your traffic generation goal?",
        "Should we start with a landing page or full site for maximum traffic conversion?",
        "How can the website integrate with our existing autonomous agent system?",
        "What content from our Twitter threads should be the foundation of the website?"
    ],
    "for_ceo": [
        "What's the minimum viable website that could generate our first confirmed sale?",
        "How much of our $100 daily budget should go to website development?",
        "Landing page vs full site - which gives better conversion ROI?", 
        "What success metrics should we track for the website?"
    ],
    "for_system": [
        "Can our existing content creation agents help build/manage the website?",
        "What new agents do we need for website operations?",
        "How do we maintain our 80/20 strategy on the website?",
        "Should the website replace Twitter or complement it?"
    ]
}

print("🤖 QUESTIONS TO ASK YOUR AGENTS:")
print("================================")

for agent, agent_questions in questions.items():
    print(f"\n{agent.upper()}:")
    for i, q in enumerate(agent_questions, 1):
        print(f"{i}. {q}")

print("\n💡 RECOMMENDATION:")
print("Ask your agents these questions and let them guide the website strategy")
print("based on their current priorities and your empire's needs.")
