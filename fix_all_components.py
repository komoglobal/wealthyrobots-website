#!/usr/bin/env python3
"""
FIX ALL COMPONENTS SCRIPT
Fix syntax errors in all generated AGI components
"""

import os
import re
from pathlib import Path

def fix_component_files():
    """Fix all component files with syntax errors"""

    workspace_path = Path("/home/ubuntu/wealthyrobot")

    # Files to fix
    component_files = [
        "unified_agi_architecture.py",
        "self_evolution_engine.py",
        "global_optimization_framework.py",
        "advanced_reasoning_engine.py",
        "security_monitoring_system.py",
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

    for filename in component_files:
        filepath = workspace_path / filename
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    content = f.read()

                original_content = content

                # Fix malformed attribute assignments like self."component_name"
                content = re.sub(r'self\."([^"]+)"', r'self.\1', content)

                # Fix undefined component_name variables
                component_name = filename.replace('.py', '')
                content = content.replace('component_name', f'"{component_name}"')

                # Fix agent_name assignments
                content = re.sub(r'self\.agent_name = "[^"]*"', f'self.agent_name = "{component_name}"', content)

                # Fix framework_name assignments
                content = re.sub(r'self\.framework_name = "[^"]*"', f'self.framework_name = "{component_name}"', content)

                # Fix system_name assignments
                content = re.sub(r'self\.system_name = "[^"]*"', f'self.system_name = "{component_name}"', content)

                # Write back if changed
                if content != original_content:
                    with open(filepath, 'w') as f:
                        f.write(content)
                    fixes_applied += 1
                    print(f"✅ Fixed {filename}")

            except Exception as e:
                print(f"❌ Failed to fix {filename}: {e}")

    print(f"\\n📊 Fixed {fixes_applied} component files")

def test_component_imports():
    """Test that all components can be imported and instantiated"""

    import importlib
    import inspect

    workspace_path = Path("/home/ubuntu/wealthyrobot")

    component_files = [
        "unified_agi_architecture",
        "self_evolution_engine",
        "global_optimization_framework",
        "advanced_reasoning_engine",
        "security_monitoring_system",
        "master_coordinator_agent",
        "resource_manager_agent",
        "security_monitor_agent",
        "data_analyst_agent",
        "research_agent",
        "trading_agent",
        "pattern_recognition_agent",
        "marketing_agent",
        "predictive_analytics_agent",
        "sentiment_analysis_agent",
        "healthcare_agent",
        "finance_agent",
        "gaming_agent",
        "social_media_agent"
    ]

    successful_imports = 0
    successful_instantiations = 0

    for component in component_files:
        try:
            module = importlib.import_module(component)
            successful_imports += 1

            # Try to instantiate
            classes = [obj for name, obj in inspect.getmembers(module)
                      if inspect.isclass(obj) and not name.startswith('_')]
            if classes:
                cls = classes[0]
                try:
                    if 'workspace_path' in inspect.signature(cls.__init__).parameters:
                        instance = cls(workspace_path=str(workspace_path))
                    else:
                        instance = cls()
                    successful_instantiations += 1
                    print(f"✅ {component} - OK")
                except Exception as e:
                    print(f"⚠️ {component} - Import OK, instantiation failed: {e}")
            else:
                print(f"⚠️ {component} - Import OK, no classes found")

        except Exception as e:
            print(f"❌ {component} - Import failed: {e}")

    print(f"\\n📊 Test Results:")
    print(f"• Successful imports: {successful_imports}/{len(component_files)}")
    print(f"• Successful instantiations: {successful_instantiations}/{len(component_files)}")

if __name__ == "__main__":
    print("🔧 FIXING ALL AGI COMPONENTS")
    print("=" * 40)

    fix_component_files()

    print("\\n🧪 TESTING COMPONENT FIXES")
    print("=" * 30)

    test_component_imports()

    print("\\n🎯 COMPONENT FIX PROCESS COMPLETE!")
