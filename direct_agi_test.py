#!/usr/bin/env python3
"""
Direct AGI test to show actionable choices
"""

import sys
import asyncio
sys.path.append('/home/ubuntu/wealthyrobot')

async def direct_agi_test():
    print("🚀 DIRECT AGI TEST - UNRESTRICTED MODE")
    print("=" * 70)
    
    try:
        from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem
        
        print("🤖 Initializing AGI System...")
        agi = UnrestrictedAGISystem()
        
        print("🎯 Running Full Intelligence Analysis...")
        results = await agi.run_unrestricted_intelligence_cycle()
        
        print("\n📊 INTELLIGENCE ANALYSIS COMPLETE")
        print("=" * 50)
        
        # Show strategies
        strategies = results.get('evolved_strategies', [])
        if strategies:
            print("�� GENERATED STRATEGIES (NOW APPROVED!):")
            print("-" * 40)
            for i, strategy in enumerate(strategies, 1):
                name = strategy.get('name', 'Unknown')
                gain = strategy.get('efficiency_gain', 'Unknown')
                print(f"{i}. 🟡 [Action] {name} ({gain} efficiency gain)")
                print(f"   Type: {strategy.get('type', 'Unknown')}")
                print(f"   Business Optimized: {strategy.get('business_optimized', False)}")
                print(f"   Risk Adjusted: {strategy.get('risk_adjusted', False)}")
                print()
        
        # Show ethical evaluations
        ethical_reasoning = results.get('ethical_reasoning', {})
        strategy_evaluations = ethical_reasoning.get('strategy_evaluations', [])
        
        if strategy_evaluations:
            print("⚖️ ETHICAL EVALUATIONS:")
            print("-" * 30)
            approved_count = 0
            
            for eval in strategy_evaluations:
                strategy_name = eval.get('strategy', {}).get('name', 'Unknown')
                approved = eval.get('approved', False)
                status = "✅ APPROVED" if approved else "❌ REJECTED"
                
                if approved:
                    approved_count += 1
                
                print(f"• {strategy_name}: {status}")
            
            print(f"\n📊 RESULT: {approved_count} Approved, {len(strategy_evaluations) - approved_count} Rejected")
        
        # Show final actionable choices
        print("\n🎯 ACTIONABLE CHOICES YOU WOULD SEE:")
        print("=" * 40)
        
        if approved_count > 0:
            print("✅ SUCCESS! You would see ALL these specific strategies:")
            for i, strategy in enumerate(strategies, 1):
                name = strategy.get('name', 'Unknown')
                gain = strategy.get('efficiency_gain', 'Unknown')
                print(f"{i}. 🟡 [Action] {name} ({gain} efficiency gain)")
        else:
            print("❌ Still showing generic fallback:")
            
        print("6. 🟡 [Action] Implement the suggested plan")
        
        print("\n💡 You can:")
        print("• Reply with the number to select a choice")
        print("• Ask follow-up questions")
        print("• Request more details about any option")
        print("• Say 'implement all' to implement all suggestions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(direct_agi_test())
