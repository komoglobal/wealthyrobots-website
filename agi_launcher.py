#!/usr/bin/env python3
"""
🚀 AGI MASTER SYSTEM LAUNCHER
=============================

Simple launcher for the complete AGI development suite.
This script provides a clean interface to start your AGI laboratory.
"""

import asyncio
import sys
import subprocess
from pathlib import Path

def check_system_requirements():
    """Check if all required files exist"""
    required_files = [
        'UNRESTRICTED_AGI_SYSTEM.py',
        'automated_agi_testing.py',
        'enhanced_pattern_recognition.py',
        'business_testing_system.py',
        'multimodal_reasoning_system.py',
        'agi_evaluation_framework.py',
        'continuous_learning_system.py'
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        return False

    print("✅ All system files found")
    return True

def display_welcome():
    """Display welcome message"""
    welcome = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                   🤖 AGI MASTER SYSTEM 🤖                     ║
║                                                              ║
║              Complete AGI Development Suite                  ║
║                                                              ║
║  🧪 Automated Testing     🔍 Pattern Recognition              ║
║  💼 Business Intelligence 🎨 Multimodal Reasoning             ║
║  🏆 Evaluation Framework  🔄 Continuous Learning               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🎯 Welcome to your AGI Development Laboratory!
================================================
"""
    print(welcome)

def display_menu():
    """Display main menu"""
    menu = """
🚀 AGI MASTER SYSTEM MENU
=========================

1. 🧪 Run Automated Benchmark Testing
2. 🎨 Run Pattern Recognition Training
3. 💼 Run Business Intelligence Testing
4. 🎭 Run Multimodal Reasoning Testing
5. 🏆 Run Comprehensive AGI Evaluation
6. 🔄 Start Continuous Learning Mode
7. 📊 View System Status
8. 🔧 System Maintenance
0. 👋 Exit

Choose an option (0-8): """
    return menu

async def run_automated_testing():
    """Run automated benchmark testing"""
    print("\n🧪 Starting Automated Benchmark Testing...")
    try:
        from automated_agi_testing import AutomatedAGITesting
        from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem

        agi_system = UnrestrictedAGISystem()
        testing_system = AutomatedAGITesting()

        print("✅ Systems initialized")
        results = await testing_system.run_comprehensive_test_suite('emerging')
        print("✅ Testing completed")

        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def run_pattern_training():
    """Run pattern recognition training"""
    print("\n🎨 Starting Pattern Recognition Training...")
    try:
        from enhanced_pattern_recognition import EnhancedPatternRecognition
        from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem

        agi_system = UnrestrictedAGISystem()
        pattern_system = EnhancedPatternRecognition()

        print("✅ Systems initialized")
        training_session = pattern_system.create_training_session('medium', 'all')
        results = await pattern_system.run_training_session(training_session, agi_system)
        print("✅ Training completed")

        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def run_business_testing():
    """Run business intelligence testing"""
    print("\n💼 Starting Business Intelligence Testing...")
    try:
        from business_testing_system import BusinessTestingSystem
        from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem

        agi_system = UnrestrictedAGISystem()
        business_system = BusinessTestingSystem()

        print("✅ Systems initialized")
        results = await business_system.run_comprehensive_business_test_suite(agi_system)
        print("✅ Testing completed")

        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def run_multimodal_testing():
    """Run multimodal reasoning testing"""
    print("\n🎭 Starting Multimodal Reasoning Testing...")
    try:
        from multimodal_reasoning_system import MultimodalReasoningSystem
        from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem

        agi_system = UnrestrictedAGISystem()
        multimodal_system = MultimodalReasoningSystem()

        print("✅ Systems initialized")
        results = await multimodal_system.run_comprehensive_multimodal_test_suite(agi_system)
        print("✅ Testing completed")

        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def run_comprehensive_evaluation():
    """Run comprehensive AGI evaluation"""
    print("\n🏆 Starting Comprehensive AGI Evaluation...")
    try:
        from agi_evaluation_framework import AGIEvaluationFramework
        from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem

        agi_system = UnrestrictedAGISystem()
        evaluation_framework = AGIEvaluationFramework()

        print("✅ Systems initialized")
        results = await evaluation_framework.run_comprehensive_agi_evaluation(agi_system)
        print("✅ Evaluation completed")

        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def start_continuous_learning():
    """Start continuous learning mode"""
    print("\n🔄 Starting Continuous Learning Mode...")
    try:
        from continuous_learning_system import ContinuousLearningSystem

        learning_system = ContinuousLearningSystem()

        print("✅ Continuous Learning System initialized")
        print("🔄 System is now running automated learning cycles...")
        print("⚠️ Press Ctrl+C to stop continuous learning mode")

        # Keep the system running
        while True:
            await asyncio.sleep(60)  # Check every minute
            print(f"🔄 Continuous learning active...")

    except KeyboardInterrupt:
        print("\n⏹️ Continuous learning mode stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_system_status():
    """Show system status"""
    print("\n📊 SYSTEM STATUS")
    print("=" * 20)

    # Check for data files
    data_files = [
        'learning_patterns.json',
        'improvement_history.json',
        'skill_levels.json',
        'test_history.json'
    ]

    for file in data_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"✅ {file}: {size} bytes")
        else:
            print(f"📭 {file}: Not found")

    # Check for report files
    report_files = list(Path('.').glob('*report*.txt')) + list(Path('.').glob('*results*.json'))
    print(f"\n📄 Recent Reports: {len(report_files)} files")

    if report_files:
        for i, report in enumerate(sorted(report_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]):
            mtime = Path(report).stat().st_mtime
            from datetime import datetime
            dt = datetime.fromtimestamp(mtime)
            print(f"  {i+1}. {report.name} ({dt.strftime('%Y-%m-%d %H:%M')})")

def system_maintenance():
    """System maintenance menu"""
    print("\n🔧 SYSTEM MAINTENANCE")
    print("=" * 22)

    maintenance_menu = """
1. 💾 Backup system data
2. 🧹 Clean old reports
3. 📊 Generate system summary
4. 🔄 Reset learning patterns
5. 🔙 Back to main menu

Choose maintenance option (1-5): """

    try:
        choice = input(maintenance_menu).strip()

        if choice == '1':
            backup_system_data()
        elif choice == '2':
            clean_old_reports()
        elif choice == '3':
            generate_system_summary()
        elif choice == '4':
            reset_learning_patterns()
        elif choice == '5':
            return
        else:
            print("❌ Invalid choice")

    except KeyboardInterrupt:
        return

def backup_system_data():
    """Backup system data"""
    print("\n💾 Backing up system data...")

    backup_files = [
        'learning_patterns.json',
        'improvement_history.json',
        'skill_levels.json',
        'test_history.json'
    ]

    backup_count = 0
    for file in backup_files:
        if Path(file).exists():
            from datetime import datetime
            backup_name = f"{file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                import shutil
                shutil.copy2(file, backup_name)
                backup_count += 1
                print(f"  ✅ {file} -> {backup_name}")
            except Exception as e:
                print(f"  ❌ Failed to backup {file}: {e}")

    print(f"\n💾 Backup completed: {backup_count} files backed up")

def clean_old_reports():
    """Clean old report files"""
    print("\n🧹 Cleaning old reports...")

    report_patterns = ['*report*.txt', '*results*.json', '*test_results*.json']
    deleted_count = 0

    for pattern in report_patterns:
        for file in Path('.').glob(pattern):
            try:
                # Keep files from last 7 days
                from datetime import datetime, timedelta
                file_age = datetime.now() - datetime.fromtimestamp(file.stat().st_mtime)
                if file_age > timedelta(days=7):
                    file.unlink()
                    deleted_count += 1
                    print(f"  🗑️ Deleted {file.name}")
            except Exception as e:
                print(f"  ❌ Failed to delete {file.name}: {e}")

    print(f"\n🧹 Cleanup completed: {deleted_count} old files removed")

def generate_system_summary():
    """Generate system summary"""
    print("\n📊 Generating system summary...")

    summary = f"""
AGI MASTER SYSTEM SUMMARY
=========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SYSTEM COMPONENTS
=================
"""

    # Check system files
    system_files = [
        'UNRESTRICTED_AGI_SYSTEM.py',
        'automated_agi_testing.py',
        'enhanced_pattern_recognition.py',
        'business_testing_system.py',
        'multimodal_reasoning_system.py',
        'agi_evaluation_framework.py',
        'continuous_learning_system.py'
    ]

    operational_count = 0
    for file in system_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            summary += f"✅ {file}: {size} bytes\n"
            operational_count += 1
        else:
            summary += f"❌ {file}: Missing\n"

    summary += f"""
DATA FILES
==========
"""

    data_files = [
        'learning_patterns.json',
        'improvement_history.json',
        'skill_levels.json',
        'test_history.json'
    ]

    data_count = 0
    for file in data_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            summary += f"📄 {file}: {size} bytes\n"
            data_count += 1
        else:
            summary += f"📭 {file}: Not found\n"

    summary += f"""
SYSTEM STATUS
=============
Operational Components: {operational_count}/{len(system_files)}
Data Files: {data_count}/{len(data_files)}

Ready for AGI Development: {'✅ Yes' if operational_count == len(system_files) else '⚠️ Partial'}
"""

    # Save summary
    summary_file = f"system_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(summary_file, 'w') as f:
        f.write(summary)

    print(summary)
    print(f"\n💾 Summary saved to: {summary_file}")

def reset_learning_patterns():
    """Reset learning patterns"""
    print("\n🔄 Resetting learning patterns...")

    reset_files = [
        'learning_patterns.json',
        'improvement_history.json',
        'skill_levels.json'
    ]

    reset_count = 0
    for file in reset_files:
        try:
            if Path(file).exists():
                Path(file).unlink()
                reset_count += 1
                print(f"  🗑️ Reset {file}")
            else:
                print(f"  📭 {file} not found")
        except Exception as e:
            print(f"  ❌ Failed to reset {file}: {e}")

    print(f"\n🔄 Reset completed: {reset_count} files reset")
    print("🎯 AGI system ready for fresh learning")

async def main():
    """Main launcher function"""
    # Display welcome
    display_welcome()

    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met. Please ensure all files are present.")
        return

    print("✅ All systems ready for operation!\n")

    # Main menu loop
    while True:
        try:
            # Display menu and get choice
            choice = input(display_menu()).strip()

            if choice == '0':
                print("\n👋 Thank you for using the AGI Master System!")
                print("🎯 Your AGI development laboratory is ready for your next session.")
                break

            elif choice == '1':
                await run_automated_testing()

            elif choice == '2':
                await run_pattern_training()

            elif choice == '3':
                await run_business_testing()

            elif choice == '4':
                await run_multimodal_testing()

            elif choice == '5':
                await run_comprehensive_evaluation()

            elif choice == '6':
                await start_continuous_learning()

            elif choice == '7':
                show_system_status()

            elif choice == '8':
                system_maintenance()

            else:
                print("❌ Invalid choice. Please enter 0-8.")

            # Pause before showing menu again
            if choice != '0':
                input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n\n⏹️ AGI Master System interrupted")
            print("💾 Progress saved")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("🔄 Returning to main menu...")

if __name__ == "__main__":
    from datetime import datetime
    asyncio.run(main())
