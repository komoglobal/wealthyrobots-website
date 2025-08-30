#!/usr/bin/env python3
"""
Quick test of meta-cognitive capabilities
"""

def test_metacognitive_system():
   print("🧪 TESTING META-COGNITIVE SYSTEM")
   print("=" * 40)
   
   try:
       # Test 1: Import meta-cognitive CLAUDE
       print("Test 1: Loading meta-cognitive CLAUDE...")
       from meta_cognitive_claude import MetaCognitiveClaude
       meta_claude = MetaCognitiveClaude()
       print("✅ Meta-cognitive CLAUDE loaded")
       
       # Test 2: Run meta-cognitive cycle
       print("\nTest 2: Running meta-cognitive cycle...")
       result = meta_claude.meta_cognitive_cycle()
       print(f"✅ Cycle completed: {result['meta_cognitive_health']}")
       
       # Test 3: Test stuck detection
       print("\nTest 3: Testing stuck detection...")
       stuck_analysis = meta_claude.detect_stuck_behaviors()
       print(f"✅ Stuck detection: {stuck_analysis['is_stuck']}")
       
       # Test 4: Test creative solutions
       print("\nTest 4: Testing creative problem solving...")
       creative_solutions = meta_claude.think_outside_the_box("test problem")
       print(f"✅ Generated {len(creative_solutions)} creative approaches")
       
       print("\n🎉 All tests passed! Meta-cognitive system is working!")
       return True
       
   except Exception as e:
       print(f"❌ Test failed: {e}")
       return False

if __name__ == "__main__":
   test_metacognitive_system()
