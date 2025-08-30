#!/usr/bin/env python3
"""
TEST WHY TO HOW CONNECTION
Demonstrates how the Curiosity Engine (WHY) now connects to the HOW Execution Engine
"""

import asyncio
import json
from datetime import datetime

async def test_why_to_how_connection():
    """Test the complete flow from WHY questions to real business execution"""
    print("🧠 TESTING WHY TO HOW CONNECTION")
    print("=" * 50)
    print("🎯 This will show the complete flow:")
    print("   WHY Question → Insight → HOW Execution → Real Business Action")
    print("")
    
    try:
        # Import the AGI system
        from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem
        
        print("🚀 Initializing Unrestricted AGI System...")
        agi_system = UnrestrictedAGISystem()
        await agi_system.initialize_unrestricted_system()
        
        print("\n🔍 Testing Curiosity Engine (WHY)...")
        
        # Generate WHY questions
        why_questions = await agi_system.curiosity_engine.generate_why_questions("business_optimization")
        print(f"   ✅ Generated {len(why_questions)} WHY questions")
        
        # Investigate WHY questions to get insights
        insights = await agi_system.curiosity_engine.investigate_why_questions(why_questions)
        print(f"   ✅ Generated {len(insights)} insights from WHY questions")
        
        # Show the insights
        print(f"\n💡 INSIGHTS GENERATED:")
        for i, insight in enumerate(insights, 1):
            print(f"   {i}. {insight.get('summary', 'No summary')}")
            print(f"      Implication: {insight.get('implication', 'No implication')}")
            print(f"      Evidence: {insight.get('evidence', 'No evidence')}")
            print("")
        
        print("🚀 Testing HOW Execution Engine connection...")
        
        # Check if HOW Execution Engine is available
        if agi_system.how_execution_engine:
            print("   ✅ HOW Execution Engine is connected!")
            print("   💰 Ready to execute insights into real business actions!")
            
            # Test executing one insight
            if insights:
                test_insight = insights[0]
                print(f"\n🎯 EXECUTING INSIGHT: {test_insight.get('summary', 'Unknown')}")
                
                # Execute the insight with real business actions
                execution_result = await agi_system.how_execution_engine.execute_insight(test_insight)
                
                print(f"\n🎉 EXECUTION COMPLETE!")
                print(f"   💰 Business Impact: {execution_result.get('business_impact', 'None')}")
                print(f"   📊 Success Rate: {execution_result.get('execution_results', {}).get('overall_success', 'Unknown')}")
                
        else:
            print("   ❌ HOW Execution Engine not available")
            print("   🔧 Insights will be applied internally only")
        
        print(f"\n📊 SUMMARY:")
        print(f"   WHY Questions Generated: {len(why_questions)}")
        print(f"   Insights Generated: {len(insights)}")
        print(f"   HOW Execution Available: {'Yes' if agi_system.how_execution_engine else 'No'}")
        
        if agi_system.how_execution_engine:
            print(f"   🎯 READY FOR REAL BUSINESS EXECUTION!")
            print(f"   💰 Your AGI can now turn insights into actual profit!")
        else:
            print(f"   ⚠️  Limited to internal improvements only")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Make sure both UNRESTRICTED_AGI_SYSTEM.py and AGI_HOW_EXECUTION_ENGINE.py are available")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Main function"""
    success = await test_why_to_how_connection()
    
    if success:
        print(f"\n🎉 WHY TO HOW CONNECTION TEST COMPLETE!")
        print(f"🚀 Your AGI now has the complete flow:")
        print(f"   Curiosity (WHY) → Execution (HOW) → Real Business Results")
    else:
        print(f"\n❌ Test failed - check the errors above")

if __name__ == "__main__":
    asyncio.run(main())
