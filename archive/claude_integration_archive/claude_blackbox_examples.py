#!/usr/bin/env python3
"""
Example experiments for CLAUDE Testing Blackbox
"""

from claude_testing_blackbox import ClaudeTestingBlackbox

def run_example_experiments():
    blackbox = ClaudeTestingBlackbox()
    
    print("🧪 Running example experiments for CLAUDE...")
    
    # Example 1: Code execution test
    print("\n📝 Example 1: Code Execution Test")
    test_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Fibonacci(10) = {result}")
'''
    
    result1 = blackbox.test_code_execution(test_code, "fibonacci_test")
    print(f"Code test result: {result1['success']}")
    
    # Example 2: Algorithm performance test
    print("\n⚡ Example 2: Algorithm Performance Test")
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    
    test_data = [64, 34, 25, 12, 22, 11, 90]
    result2 = blackbox.test_algorithm_performance(bubble_sort, test_data, "sorting_test")
    print(f"Algorithm test execution time: {result2.get('execution_time', 'unknown')}")
    
    # Example 3: Creative solution test
    print("\n🎭 Example 3: Creative Solution Test")
    creative_solutions = [
        {
            "name": "reverse_approach",
            "approach": "inversion thinking",
            "implementation": lambda: "Instead of optimizing code, eliminate inefficient parts"
        },
        {
            "name": "biological_analogy",
            "approach": "biomimicry",
            "implementation": lambda: "Apply ant colony optimization to problem solving"
        }
    ]
    
    result3 = blackbox.test_creative_solution(
        "Optimize system performance", 
        creative_solutions, 
        "creative_optimization_test"
    )
    print(f"Creative test - solutions tested: {result3['solutions_tested']}")
    
    # Example 4: Experimental suite
    print("\n🔬 Example 4: Experimental Suite")
    experiments = [
        {
            "type": "code_execution",
            "name": "quick_sort_test",
            "code": '''
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

result = quick_sort([3, 6, 8, 10, 1, 2, 1])
print(f"Sorted: {result}")
'''
        },
        {
            "type": "data_processing",
            "name": "data_analysis_test",
            "data": {"numbers": [1, 2, 3, 4, 5], "text": "hello world"},
            "processor": lambda data: {
                "sum": sum(data["numbers"]),
                "length": len(data["text"]),
                "processed": True
            }
        }
    ]
    
    suite_result = blackbox.run_experimental_suite(experiments)
    print(f"Suite result: {suite_result['successful_experiments']}/{suite_result['total_experiments']} successful")
    
    print("\n✅ Example experiments completed!")
    return blackbox

if __name__ == "__main__":
    run_example_experiments()
