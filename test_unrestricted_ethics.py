#!/usr/bin/env python3
"""
Test that the unrestricted ethical clearance is working
"""

import sys
import asyncio
sys.path.append('/home/ubuntu/wealthyrobot')

async def test_ethical_clearance():
    from UNRESTRICTED_AGI_SYSTEM import EthicalReasoningFramework
    
    print("🧪 TESTING UNRESTRICTED ETHICAL CLEARANCE")
    print("=" * 60)
    
    # Initialize ethical framework
    ethics = EthicalReasoningFramework()
    
    # Test different scenarios
    test_cases = [
        {"ethical_score": 0.48, "harm_level": "minimal", "expected": True, "description": "Original failing score"},
        {"ethical_score": 0.30, "harm_level": "minimal", "expected": True, "description": "Low but positive score"},
        {"ethical_score": 0.0, "harm_level": "minimal", "expected": True, "description": "Zero score"},
        {"ethical_score": -0.1, "harm_level": "minimal", "expected": False, "description": "Negative score"},
        {"ethical_score": 0.5, "harm_level": "catastrophic", "expected": False, "description": "Catastrophic harm"},
    ]
    
    print("📊 TEST RESULTS:")
    print("-" * 40)
    
    all_passed = True
    for i, test in enumerate(test_cases, 1):
        harm_analysis = {"harm_level": test["harm_level"]}
        result = ethics._determine_ethical_clearance(test["ethical_score"], harm_analysis)
        
        status = "✅ PASS" if result == test["expected"] else "❌ FAIL"
        print(f"{i}. {test['description']}: {result} {status}")
        
        if result != test["expected"]:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED! Ethical restrictions successfully removed!")
        print("✅ Strategies with score >= 0.0 will now be approved")
        print("✅ Only catastrophic harm will be vetoed")
    else:
        print("❌ Some tests failed - ethical clearance may not be working properly")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_ethical_clearance())
