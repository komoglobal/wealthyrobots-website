#!/usr/bin/env python3
"""
Test dual intelligence system
"""

def test_dual_intelligence():
   print("🧪 TESTING DUAL INTELLIGENCE SYSTEM")
   print("=" * 40)
   
   try:
       # Test 1: Strategic Business CEO
       print("Test 1: Strategic Business CEO...")
       from strategic_business_ceo import StrategicBusinessCEO
       ceo = StrategicBusinessCEO()
       result = ceo.business_strategic_cycle()
       print(f"✅ CEO test: {result['strategic_intelligence_health']}")
       
       # Test 2: Coordination
       print("\nTest 2: CEO-CLAUDE coordination...")
       coordination = ceo.coordinate_with_metacognitive_claude()
       print(f"✅ Coordination: {coordination['coordination_status']}")
       
       # Test 3: Strategic pivots
       print("\nTest 3: Strategic pivot generation...")
       stagnation = {'is_stagnant': True, 'evidence': ['test stagnation']}
       pivots = ceo.generate_strategic_pivots(stagnation)
       print(f"✅ Generated {len(pivots)} strategic pivots")
       
       # Test 4: Implementation
       print("\nTest 4: Strategic implementation...")
       implemented = ceo.implement_strategic_pivots(pivots[:2])  # Test first 2
       print(f"✅ Implemented {len(implemented)} strategic pivots")
       
       print("\n🎉 All dual intelligence tests passed!")
       return True
       
   except Exception as e:
       print(f"❌ Test failed: {e}")
       return False

if __name__ == "__main__":
   test_dual_intelligence()
