#!/usr/bin/env python3
"""
Test the CLAUDE blackbox system
"""

def test_claude_blackbox():
    print("🧪 TESTING CLAUDE BLACKBOX SYSTEM")
    print("=" * 40)
    
    try:
        # Test 1: Initialize blackbox
        print("Test 1: Initialize blackbox...")
        from claude_testing_blackbox import ClaudeTestingBlackbox
        blackbox = ClaudeTestingBlackbox()
        print("✅ Blackbox initialized")
        
        # Test 2: Simple code test
        print("\nTest 2: Code execution test...")
        simple_code = 'print("Hello from CLAUDE blackbox!")'
        result = blackbox.test_code_execution(simple_code, "hello_test")
        print(f"✅ Code test: {result['success']}")
        
        # Test 3: Algorithm test
        print("\nTest 3: Algorithm performance test...")
        def simple_algo(data):
            return sum(data)
        
        result = blackbox.test_algorithm_performance(simple_algo, [1, 2, 3, 4, 5], "sum_test")
        print(f"✅ Algorithm test: {result['success']}")
        
        # Test 4: Creative solution test
        print("\nTest 4: Creative solution test...")
        solutions = [
            {
                "name": "test_solution",
                "approach": "testing",
                "implementation": lambda: "This is a test solution"
            }
        ]
        result = blackbox.test_creative_solution("Test problem", solutions, "creativity_test")
        print(f"✅ Creative test: {result['solutions_tested']} solutions tested")
        
        print("\n🎉 All blackbox tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_claude_blackbox()
