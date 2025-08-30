#!/usr/bin/env python3
"""
START OPTIMIZED AGI - Maximum Performance, No System Overload
Easy startup script for the optimized AGI system
"""

import os
import sys
import time
from datetime import datetime

def show_startup_info():
    """Show startup information"""
    print("🧠 OPTIMIZED AGI SYSTEM - MAXIMUM PERFORMANCE")
    print("=" * 60)
    print("🚀 System designed to maximize AGI performance")
    print("⚡ Smart resource management prevents overload")
    print("🎯 Adaptive feature gating based on system capacity")
    print("📊 Real-time performance monitoring")
    print("🔄 Automatic emergency mode activation")
    print("=" * 60)

def check_system_requirements():
    """Check if system requirements are met"""
    print("🔍 Checking system requirements...")

    requirements_met = True

    # Check if required files exist
    required_files = [
        "config/system_optimization.yaml",
        "UNRESTRICTED_AGI_SYSTEM.py",
        "meta_cognitive_claude.py"
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            requirements_met = False

    # Check for required directories
    required_dirs = ["data", "config", "reports"]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory")
        else:
            print(f"⚠️  {dir_name}/ directory - Creating...")
            try:
                os.makedirs(dir_name, exist_ok=True)
                print(f"✅ Created {dir_name}/")
            except Exception as e:
                print(f"❌ Failed to create {dir_name}/: {e}")
                requirements_met = False

    if requirements_met:
        print("✅ All system requirements met!")
    else:
        print("❌ Some requirements not met - system may not work optimally")

    return requirements_met

def show_optimization_features():
    """Show optimization features"""
    print("\n⚙️  OPTIMIZATION FEATURES:")
    print("   • Smart resource monitoring (CPU, RAM, Disk)")
    print("   • Adaptive cycle timing (5min normal, 30s emergency)")
    print("   • Feature gating based on system load")
    print("   • Emergency mode with automatic load reduction")
    print("   • Memory optimization and cache management")
    print("   • Performance tracking and reporting")
    print("   • Batch processing for efficiency")

def start_agi_system():
    """Start the optimized AGI system"""
    print("\n🚀 STARTING OPTIMIZED AGI SYSTEM...")
    print("Press Ctrl+C to stop gracefully")

    try:
        # Import and run the optimized AGI runner
        from optimized_agi_runner import main
        main()

    except KeyboardInterrupt:
        print("\n🛑 AGI system shutdown requested")
        show_shutdown_info()
    except Exception as e:
        print(f"\n❌ AGI system error: {e}")
        import traceback
        traceback.print_exc()
        show_shutdown_info()

def show_shutdown_info():
    """Show shutdown information"""
    print("\n📊 SHUTDOWN INFORMATION:")
    print("   • AGI system stopped gracefully")
    print("   • Performance data saved to data/optimized_agi_cycles.jsonl")
    print("   • System logs available in data/ directory")
    print("   • To restart: python3 start_optimized_agi.py")

def show_usage_tips():
    """Show usage tips"""
    print("\n💡 USAGE TIPS:")
    print("   • System automatically adjusts to your hardware")
    print("   • Monitor performance via the real-time metrics")
    print("   • Emergency mode activates automatically if needed")
    print("   • Features are enabled/disabled based on system load")
    print("   • Check data/ directory for detailed logs and reports")

def main():
    """Main startup function"""
    show_startup_info()

    if check_system_requirements():
        show_optimization_features()
        show_usage_tips()

        print("\n" + "=" * 60)
        input("Press Enter to start the Optimized AGI System...")

        start_agi_system()
    else:
        print("\n❌ Cannot start AGI system due to missing requirements")
        print("Please ensure all required files are present")

if __name__ == "__main__":
    main()
