#!/usr/bin/env python3
"""
🚀 DIRECT AUTOMATED BENCHMARK TESTING SCRIPT
===========================================

Runs the complete automated AGI benchmark testing suite without user interaction.
This script automatically tests your AGI across 43 major benchmarks.
"""

import asyncio
import json
import sys
from datetime import datetime

# Import required systems
try:
    from automated_agi_testing import AutomatedAGITesting
    from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem
    from agi_benchmark_tests import AGIBenchmarkSuite
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

async def run_automated_benchmark_testing():
    """Run the complete automated benchmark testing suite"""

    print("🚀 STARTING AUTOMATED AGI BENCHMARK TESTING")
    print("=" * 50)

    try:
        # Initialize AGI system
        print("🤖 Initializing AGI Core System...")
        agi_system = UnrestrictedAGISystem()
        print("✅ AGI System initialized successfully")

        # Initialize benchmark suite
        print("📊 Initializing Benchmark Suite...")
        benchmark_suite = AGIBenchmarkSuite()
        print("✅ Benchmark Suite ready")

        # Initialize automated testing system
        print("🧪 Initializing Automated Testing Framework...")
        testing_system = AutomatedAGITesting()
        await testing_system.initialize_system()
        print("✅ Automated Testing System initialized")

        # Display available benchmarks
        print("\n📋 AVAILABLE BENCHMARKS:")
        print("=" * 30)

        # Get emerging AGI test suite
        emerging_suite = benchmark_suite.get_recommended_test_suite('emerging')
        print(f"🎯 Emerging AGI Test Suite: {len(emerging_suite['tests'])} benchmarks")
        print("   Tests:", ', '.join(emerging_suite['tests']))

        # Run comprehensive test suite
        print("\n🧪 RUNNING COMPREHENSIVE BENCHMARK SUITE...")
        print("=" * 45)

        # Run the tests
        results = await testing_system.run_comprehensive_test_suite('emerging')

        # Display results
        if results['success']:
            print("\n✅ TESTING COMPLETED SUCCESSFULLY!")
            print("=" * 40)

            # Show results summary
            test_results = results.get('results', {})
            total_tests = len(test_results)
            successful_tests = sum(1 for r in test_results.values() if r.get('success', False))

            print(f"📊 Total Tests Run: {total_tests}")
            print(f"✅ Successful Tests: {successful_tests}")
            print(f"📈 Success Rate: {successful_tests/total_tests*100:.1f}%")

            # Show individual test results
            print("\n🧪 INDIVIDUAL TEST RESULTS:")
            print("=" * 30)

            for test_name, result in test_results.items():
                status = "✅" if result.get('success', False) else "❌"
                score = result.get('score', 0)
                print(f"  {status} {test_name}: {score:.1f}%")

            # Show analysis
            analysis = results.get('analysis', {})
            print("\n📈 PERFORMANCE ANALYSIS:")
            print("=" * 30)
            print(f"   Average Score: {analysis.get('average_score', 0):.1f}%")
            print(f"   Total Tests: {analysis.get('total_tests', 0)}")
            print(f"   Successful Tests: {analysis.get('successful_tests', 0)}")

        else:
            print("❌ Testing failed!")
            print(f"Error: {results.get('error', 'Unknown error')}")

        # Save detailed results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f'automatic_benchmark_results_{timestamp}.json'

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n💾 Detailed results saved to: {results_file}")

        # Generate summary report
        report_file = f'automatic_benchmark_report_{timestamp}.txt'
        generate_summary_report(results, report_file)

        print(f"📄 Summary report saved to: {report_file}")

    except Exception as e:
        print(f"❌ Error during automated testing: {e}")
        import traceback
        traceback.print_exc()

def generate_summary_report(results, filename):
    """Generate a comprehensive summary report"""

    report = f"""
AUTOMATED AGI BENCHMARK TESTING REPORT
======================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
=================
Overall Success: {'✅ SUCCESS' if results.get('success', False) else '❌ FAILED'}

"""

    if results.get('success', False):
        test_results = results.get('results', {})
        total_tests = len(test_results)
        successful_tests = sum(1 for r in test_results.values() if r.get('success', False))
        avg_score = sum(r.get('score', 0) for r in test_results.values()) / total_tests if total_tests > 0 else 0

        report += f"""
Test Statistics:
• Total Tests: {total_tests}
• Successful Tests: {successful_tests}
• Success Rate: {successful_tests/total_tests*100:.1f}%
• Average Score: {avg_score:.1f}%

INDIVIDUAL TEST RESULTS
=======================
"""

        for test_name, result in test_results.items():
            status = "PASS" if result.get('success', False) else "FAIL"
            score = result.get('score', 0)
            report += f"• {test_name}: {status} ({score:.1f}%)\n"

    else:
        report += f"""
Error: {results.get('error', 'Unknown error occurred during testing')}

"""

    report += f"""
SYSTEM INFORMATION
==================
• AGI System: Unrestricted AGI System
• Testing Framework: Automated Benchmark Suite
• Benchmarks Tested: Emerging AGI Test Suite
• Total Available Benchmarks: 43

RECOMMENDATIONS
===============
"""

    if results.get('success', False):
        test_results = results.get('results', {})
        successful_tests = sum(1 for r in test_results.values() if r.get('success', False))
        total_tests = len(test_results)

        if successful_tests / total_tests > 0.8:
            report += "• Excellent performance! Consider advanced benchmark testing\n"
        elif successful_tests / total_tests > 0.6:
            report += "• Good performance! Focus on weak areas for improvement\n"
        else:
            report += "• Performance needs improvement. Focus on core capabilities\n"

        # Identify weak areas
        weak_tests = [name for name, result in test_results.items()
                     if result.get('score', 0) < 60]

        if weak_tests:
            report += "• Areas for improvement:\n"
            for test in weak_tests[:5]:  # Top 5 weak areas
                report += f"  - {test}\n"

    report += f"""
NEXT STEPS
==========
1. Review detailed results in JSON file
2. Implement recommended improvements
3. Run additional training modules
4. Schedule regular automated testing
5. Track progress over time

For more detailed analysis, run the individual testing components:
• Pattern Recognition Training: python3 enhanced_pattern_recognition.py
• Business Intelligence Testing: python3 business_testing_system.py
• Multimodal Testing: python3 multimodal_reasoning_system.py
• Comprehensive Evaluation: python3 agi_evaluation_framework.py
"""

    with open(filename, 'w') as f:
        f.write(report)

    print(f"📄 Summary report generated: {filename}")

async def main():
    """Main execution function"""
    print("🤖 AUTOMATED AGI BENCHMARK TESTING SUITE")
    print("=" * 45)

    # Run automated testing
    await run_automated_benchmark_testing()

    print("\n🎉 AUTOMATED TESTING COMPLETED!")
    print("📊 Check the generated report files for detailed results.")

if __name__ == "__main__":
    asyncio.run(main())
