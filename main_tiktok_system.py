#!/usr/bin/env python3
"""
MAIN AUTOMATED TIKTOK PROFIT SYSTEM
Complete system for automated TikTok profit generation

SYSTEM COMPONENTS:
1. Content Discovery Agent - Discovers trending content automatically
2. Automated Editing Agent - AI-powered video editing and optimization
3. TikTok Integration Agent - Handles posting and Shop integration
4. Revenue Optimization Agent - Maximizes profit from multiple streams
5. Performance Monitoring Agent - Real-time analytics and optimization
6. Automation Orchestrator - Coordinates all components

USAGE:
python3 automated_tiktok_orchestrator.py

This will start the complete automated system that runs 24/7.
"""

import json
import os
from datetime import datetime

def show_system_status():
    """Show current system status"""
    
    print("🎬 AUTOMATED TIKTOK PROFIT SYSTEM - STATUS")
    print("=" * 50)
    
    # Check component files
    components = [
        "content_discovery_agent.py",
        "automated_editing_agent.py", 
        "tiktok_integration_agent.py",
        "revenue_optimization_agent.py",
        "performance_monitoring_agent.py",
        "automated_tiktok_orchestrator.py"
    ]
    
    print("📁 System Components:")
    for component in components:
        if os.path.exists(component):
            print(f"  ✅ {component}")
        else:
            print(f"  ❌ {component}")
    
    # Check for results files
    results_files = [
        "content_discovery_results.json",
        "editing_cycle_results.json",
        "tiktok_posting_cycle.json",
        "revenue_optimization_results.json",
        "performance_monitoring_results.json"
    ]
    
    print("\n📊 Recent Results:")
    for result_file in results_files:
        if os.path.exists(result_file):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    timestamp = data.get('timestamp', 'Unknown')
                    print(f"  📈 {result_file} - {timestamp}")
            except:
                print(f"  ⚠️ {result_file} - Error reading")
        else:
            print(f"  ❌ {result_file} - No data yet")
    
    print("\n🚀 To start the automated system:")
    print("  python3 automated_tiktok_orchestrator.py")
    
    print("\n📋 To check system status:")
    print("  python3 main_tiktok_system.py --status")

def main():
    """Main function"""
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        show_system_status()
    else:
        print("🎬 AUTOMATED TIKTOK PROFIT SYSTEM")
        print("=" * 40)
        print("This system is ready for automated operation!")
        print("\nTo start automation:")
        print("  python3 automated_tiktok_orchestrator.py")
        print("\nTo check status:")
        print("  python3 main_tiktok_system.py --status")

if __name__ == "__main__":
    main()
