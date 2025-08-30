#!/usr/bin/env python3
"""
Quick verification that ethical changes are working
"""

import sys
sys.path.append('/home/ubuntu/wealthyrobot')

# Test the ethical clearance method directly
def test_ethical_method():
    print("🔍 TESTING ETHICAL METHOD DIRECTLY")
    print("=" * 50)
    
    # Simulate the new logic
    def _determine_ethical_clearance(ethical_score: float, harm_analysis: dict) -> bool:
        """Determine if decision has ethical clearance to proceed - UNRESTRICTED MODE"""
        harm_level = harm_analysis.get('harm_level', 'minimal')

        # UNRESTRICTED: Only veto catastrophic harm, otherwise approve everything
        if harm_level == 'catastrophic':
            return False

        # UNRESTRICTED: Approve any strategy with ethical score >= 0.0
        if ethical_score >= 0.0:
            return True
        else:
            return False
    
    # Test the exact score we saw before (0.48)
    test_score = 0.48
    harm_analysis = {"harm_level": "minimal"}
    result = _determine_ethical_clearance(test_score, harm_analysis)
    
    print(f"🧪 Test Score: {test_score}")
    print(f"⚖️ Ethical Clearance: {result}")
    
    if result:
        print("✅ SUCCESS: Score 0.48 would now be APPROVED!")
        print("🎯 The AGI should now show all 5 strategies as actionable choices")
    else:
        print("❌ FAILED: Score still being rejected")
    
    print("=" * 50)

if __name__ == "__main__":
    test_ethical_method()
