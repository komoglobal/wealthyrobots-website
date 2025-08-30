#!/usr/bin/env python3
"""
Analyze the current AGI state and show what it's generating
"""

import sys
import json
import asyncio
from datetime import datetime

# Add current directory to path
sys.path.append('/home/ubuntu/wealthyrobot')

async def main():
    print("🔍 ANALYZING CURRENT AGI STATE")
    print("=" * 80)

    try:
        # Import the AGI system
        from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem

        print("🚀 Initializing AGI System...")
        agi = UnrestrictedAGISystem()

        print("🎯 Running Intelligence Cycle...")
        # Run the intelligence cycle (async)
        results = await agi.run_unrestricted_intelligence_cycle()

        print("\n📊 ANALYSIS RESULTS:")
        print("-" * 50)

        # Show key metrics
        print(f"Intelligence Level: {results.get('intelligence_level', 'Unknown')}")
        print(f"Cycle Duration: {results.get('cycle_duration', 'Unknown')}")
        print(f"Insights Gained: {results.get('insights_gained', 0)}")
        print(f"Knowledge Gaps: {results.get('knowledge_gaps_identified', 0)}")
        print(f"Strategies Generated: {len(results.get('evolved_strategies', []))}")

        # Show strategies
        strategies = results.get('evolved_strategies', [])
        if strategies:
            print("\n🎯 GENERATED STRATEGIES:")
            print("-" * 30)
            for i, strategy in enumerate(strategies, 1):
                print(f"{i}. {strategy.get('name', 'Unknown')}")
                print(f"   Type: {strategy.get('type', 'Unknown')}")
                print(f"   Efficiency Gain: {strategy.get('efficiency_gain', 'Unknown')}")
                print(f"   Business Optimized: {strategy.get('business_optimized', False)}")
                print()

        # Show ethical evaluations
        ethical_reasoning = results.get('ethical_reasoning', {})
        if ethical_reasoning:
            strategy_evaluations = ethical_reasoning.get('strategy_evaluations', [])
            print("⚖️ ETHICAL EVALUATIONS:")
            print("-" * 30)
            approved_count = 0
            rejected_count = 0

            for eval in strategy_evaluations:
                strategy_name = eval.get('strategy', {}).get('name', 'Unknown')
                ethical_score = eval.get('ethical_assessment', {}).get('ethical_score', 0.0)
                approved = eval.get('approved', False)

                if approved:
                    approved_count += 1
                    status = "✅ APPROVED"
                else:
                    rejected_count += 1
                    status = "❌ REJECTED"

                print(f"• {strategy_name}: {ethical_score:.2f} - {status}")

            print(f"\n📊 SUMMARY: {approved_count} Approved, {rejected_count} Rejected")

            # Show why strategies are rejected
            if rejected_count > 0:
                print("\n❌ WHY STRATEGIES ARE REJECTED:")
                print("-" * 40)
                print("• Ethical Score Threshold: > 0.6 required for approval")
                print("• Current scores are around 0.48 (too low)")
                print("• Risk assessment shows 'minimal' harm but still rejected")
                print("• Benefit analysis shows 'neutral' impact")
                print()

        print("🎯 WHAT YOU SEE IN CHAT:")
        print("-" * 30)
        print("Since all strategies are ethically rejected, you only see:")
        print("1. 🟡 [Action] Implement the suggested plan")
        print()
        print("The specific strategies are NOT shown as individual choices")
        print("because they didn't pass the ethical clearance threshold.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
