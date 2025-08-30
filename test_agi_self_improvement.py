#!/usr/bin/env python3
"""
Test AGI Self-Improvement Integration
Manually run one AGI cycle to test the self-improvement integration
"""

import asyncio
import json
from datetime import datetime

# Import the AGI system
from AGI_CORE_SYSTEM import AGICoreSystem

async def test_agi_cycle():
    """Test one complete AGI cycle with self-improvement"""
    print("🧪 TESTING AGI CYCLE WITH SELF-IMPROVEMENT")
    print("=" * 60)

    # Initialize AGI system
    agi = AGICoreSystem()

    try:
        # Run one complete AGI cycle
        print("🔄 Running AGI intelligence cycle...")
        cycle_results = await agi.run_agi_cycle()

        # Display results
        print("\n📊 CYCLE RESULTS:")
        print(f"Timestamp: {cycle_results.get('timestamp', 'Unknown')}")
        print(f"Duration: {cycle_results.get('cycle_duration', 'Unknown')}")
        print(f"Opportunities Found: {cycle_results.get('opportunities_identified', 0)}")

        # Show self-improvement results
        if 'self_improvement_results' in cycle_results:
            si_results = cycle_results['self_improvement_results']
            print("\n🔧 SELF-IMPROVEMENT RESULTS:")
            print(f"Improvements Implemented: {si_results.get('improvements_implemented', 0)}")
            print(f"Files Modified: {len(si_results.get('files_modified', []))}")
            print(f"Errors: {len(si_results.get('errors', []))}")

            if si_results.get('errors'):
                print("❌ Errors:")
                for error in si_results.get('errors'):
                    print(f"   • {error}")

        # Show AGI progress
        if 'agi_progress' in cycle_results:
            agi_progress = cycle_results['agi_progress']
            print("\n🧠 AGI PROGRESS:")
            print(f"Overall Progress: {agi_progress.get('overall_progress', 0):.1f}%")
            print(f"Profit Generated: ${agi_progress.get('profit_generated', 0)}")

        return cycle_results

    except Exception as e:
        print(f"❌ Error during AGI cycle: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Run the test
    results = asyncio.run(test_agi_cycle())

    # Save results for inspection
    with open(f"agi_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n📁 Results saved to: agi_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
