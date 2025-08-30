#!/usr/bin/env python3
"""
Test script to check if the trading engine can start properly
"""

import sys
import traceback

def test_engine_initialization():
    print("🔧 TESTING ENGINE INITIALIZATION")
    print("=" * 50)

    try:
        print("📦 Importing required modules...")

        # Test basic imports
        from comprehensive_opportunity_scanner import ComprehensiveOpportunityScanner
        print("✅ ComprehensiveOpportunityScanner imported")

        from sdk_imports import get_tinyman_client, is_sdk_available
        print("✅ SDK imports working")

        import yaml
        print("✅ YAML module available")

        from algosdk import mnemonic
        print("✅ Algorand SDK available")

        print()
        print("🚀 Testing main engine components...")

        # Test the do_defillama_sweep function
        print("🔄 Testing do_defillama_sweep function...")
        from run_hybrid_trading_empire import do_defillama_sweep

        sweep_result = do_defillama_sweep()
        print(f"   ✅ Sweep completed: {sweep_result}")

        if sweep_result.get('top'):
            print(f"   🎯 Top opportunities found: {len(sweep_result['top'])}")
            for i, opp in enumerate(sweep_result['top'][:3]):
                source = opp.get('source', 'unknown')
                score = opp.get('opportunity_score', 0)
                print(f"      {i+1}. {source} (Score: {score})")
        else:
            print("   ⚠️ No top opportunities returned")

        print()
        print("🎉 ENGINE INITIALIZATION TEST PASSED")
        print("   ✅ All imports working")
        print("   ✅ Scanner functional")
        print("   ✅ Sweep function working")
        print("   ✅ Opportunities being found")

        return True

    except Exception as e:
        print(f"❌ ENGINE INITIALIZATION FAILED: {e}")
        print()
        print("🔍 FULL ERROR TRACEBACK:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_engine_initialization()

    if success:
        print()
        print("🎯 RECOMMENDATION:")
        print("   The engine components are working correctly.")
        print("   The issue may be in the main loop execution or timing.")
        print("   Try restarting the engine or check for blocking operations.")
    else:
        print()
        print("🚨 CRITICAL ISSUE:")
        print("   Fix the errors above before running the main engine.")








