#!/usr/bin/env python3
"""
FIX MAIN FUNCTIONS SCRIPT
Fix main functions in all generated AGI components
"""

import os
import re
from pathlib import Path

def fix_main_functions():
    """Fix main functions in all component files"""

    workspace_path = Path("/home/ubuntu/wealthyrobot")

    # Agent files to fix
    agent_files = [
        "master_coordinator_agent.py",
        "resource_manager_agent.py",
        "security_monitor_agent.py",
        "data_analyst_agent.py",
        "research_agent.py",
        "trading_agent.py",
        "pattern_recognition_agent.py",
        "marketing_agent.py",
        "predictive_analytics_agent.py",
        "sentiment_analysis_agent.py",
        "healthcare_agent.py",
        "finance_agent.py",
        "gaming_agent.py",
        "social_media_agent.py"
    ]

    fixes_applied = 0

    for filename in agent_files:
        filepath = workspace_path / filename
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    content = f.read()

                # Find the class name
                class_match = re.search(r'class (\w+):', content)
                if class_match:
                    class_name = class_match.group(1)

                    # Replace the broken main function
                    old_main = '''def main():
    """Main execution function"""
    # This will be replaced with the actual agent instantiation when the code is generated

    # Register capabilities
    agent.register_capabilities()'''

                    new_main = f'''def main():
    """Main execution function"""
    agent = {class_name}()

    # Register capabilities
    agent.register_capabilities()'''

                    if old_main in content:
                        content = content.replace(old_main, new_main)
                        fixes_applied += 1
                        print(f"✅ Fixed main function in {filename}")

                # Write back if changed
                with open(filepath, 'w') as f:
                    f.write(content)

            except Exception as e:
                print(f"❌ Failed to fix {filename}: {e}")

    print(f"\\n📊 Fixed main functions in {fixes_applied} agent files")

def fix_framework_main_functions():
    """Fix main functions in framework files"""

    workspace_path = Path("/home/ubuntu/wealthyrobot")

    # Framework files to fix
    framework_files = [
        "unified_agi_architecture.py",
        "self_evolution_engine.py",
        "global_optimization_framework.py",
        "advanced_reasoning_engine.py",
        "security_monitoring_system.py"
    ]

    fixes_applied = 0

    for filename in framework_files:
        filepath = workspace_path / filename
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    content = f.read()

                # Find the class name
                class_match = re.search(r'class (\w+):', content)
                if class_match:
                    class_name = class_match.group(1)

                    # Replace the broken main function
                    old_main = '''def main():
    """Main execution function"""
    # This will be replaced with the actual framework instantiation when the code is generated'''

                    new_main = f'''def main():
    """Main execution function"""
    framework = {class_name}()'''

                    if old_main in content:
                        content = content.replace(old_main, new_main)
                        fixes_applied += 1
                        print(f"✅ Fixed main function in {filename}")

                # Write back if changed
                with open(filepath, 'w') as f:
                    f.write(content)

            except Exception as e:
                print(f"❌ Failed to fix {filename}: {e}")

    print(f"\\n📊 Fixed main functions in {fixes_applied} framework files")

if __name__ == "__main__":
    print("🔧 FIXING MAIN FUNCTIONS")
    print("=" * 30)

    fix_main_functions()
    fix_framework_main_functions()

    print("\\n🎯 MAIN FUNCTION FIX PROCESS COMPLETE!")
