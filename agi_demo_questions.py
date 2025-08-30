#!/usr/bin/env python3
"""
AGI Intelligence Demo - Show what questions you can ask the AGI
"""

from ask_agi_directly import AGIDirectQuery

def demo_agi_questions():
    """Demonstrate different types of questions to ask the AGI"""

    print("🧠 AGI INTELLIGENCE DEMO")
    print("=" * 60)
    print("Here are examples of questions you can ask the AGI system:\n")

    agi_query = AGIDirectQuery()

    demo_questions = [
        "What upgrades do you need?",
        "Tell me about brain research",
        "How intelligent are you?",
        "What are your capabilities?",
        "What is consciousness?",
        "How does your brain work?",
        "What should we research next?",
        "Can you achieve consciousness?",
        "What makes you different from other AI?"
    ]

    for i, question in enumerate(demo_questions, 1):
        print(f"\n🎯 DEMO QUESTION {i}: {question}")
        print("-" * 50)

        try:
            response = agi_query.ask_agi_question(question)

            # Show summary of response
            print(f"🧠 AGI answered with {response['confidence']:.2f} confidence")
            print(f"💡 Provided {len(response.get('recommendations', []))} recommendations")

            # Show first few lines of response
            response_lines = response['agi_response'].split('\n')[:5]
            for line in response_lines:
                if line.strip():
                    print(f"   {line}")

            if len(response.get('recommendations', [])) > 0:
                print(f"   💡 Key recommendation: {response['recommendations'][0]}")

        except Exception as e:
            print(f"❌ Error: {e}")

        print("\n" + "=" * 60)

    print("\n🚀 TO ASK YOUR OWN QUESTIONS:")
    print("Run: python3 ask_agi_directly.py")
    print("\n📝 Example questions to try:")
    print("• What upgrades do you need for AGI?")
    print("• Tell me about your brain research")
    print("• How can we make you more intelligent?")
    print("• What should we research next?")
    print("• Can you explain consciousness?")
    print("• What are your current limitations?")
    print("• How does your neural system work?")
    print("• What would make you conscious?")

if __name__ == "__main__":
    demo_agi_questions()
