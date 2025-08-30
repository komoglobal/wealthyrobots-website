#!/usr/bin/env python3
"""
FIX ALL AGENTS SCRIPT
Fix capability registration in all agent files
"""

import os
import re
from pathlib import Path

def fix_agent_capabilities():
    """Fix capability registration in all agent files"""

    workspace_path = Path("/home/ubuntu/wealthyrobot")

    # Agent files to fix
    agent_files = [
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

                # Check if capabilities are already being registered
                if "self.register_capabilities()" not in content:
                    # Find the print statements and add capability registration
                    old_pattern = r'(\s+)print\(f"🤖 [A-Z_]+ AGENT initialized"\)\s*\n(\s+)print\(f"📁 Workspace: .+"\)\s*\n(\s+)print\(f"🎯 Capabilities: 0"\)'
                    new_pattern = r'\1# Register capabilities automatically\n\1self.register_capabilities()\n\n\1print(f"🤖 [A-Z_]+ AGENT initialized")\n\2print(f"📁 Workspace: {self.workspace_path}")\n\3print(f"🎯 Capabilities: {len(self.capabilities)}")'

                    # Replace the pattern
                    if re.search(r'print\(f"🎯 Capabilities: 0"\)', content):
                        content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE)

                        fixes_applied += 1
                        print(f"✅ Fixed capabilities in {filename}")

                # Write back if changed
                with open(filepath, 'w') as f:
                    f.write(content)

            except Exception as e:
                print(f"❌ Failed to fix {filename}: {e}")

    print(f"\\n📊 Fixed capability registration in {fixes_applied} agent files")

def fix_enhanced_market_data_agent():
    """Fix the enhanced market data agent capabilities"""
    workspace_path = Path("/home/ubuntu/wealthyrobot")
    filepath = workspace_path / "enhanced_market_data_agent.py"

    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                content = f.read()

            # Check if capabilities are being registered
            if "self.register_capabilities()" not in content:
                # Find the print statements and add capability registration
                old_pattern = r'(\s+)print\(f"🤖 ENHANCED MARKET DATA AGENT initialized"\)\s*\n(\s+)print\(f"📁 Workspace: .+"\)\s*\n(\s+)print\(f"🎯 Capabilities: .+"\)'
                new_pattern = r'\1# Register capabilities automatically\n\1self.register_capabilities()\n\n\1print(f"🤖 ENHANCED MARKET DATA AGENT initialized")\n\2print(f"📁 Workspace: {self.workspace_path}")\n\3print(f"🎯 Capabilities: {len(self.capabilities)}")'

                # Replace the pattern
                content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE)

                with open(filepath, 'w') as f:
                    f.write(content)

                print("✅ Fixed enhanced market data agent capabilities")

        except Exception as e:
            print(f"❌ Failed to fix enhanced_market_data_agent.py: {e}")

if __name__ == "__main__":
    print("🔧 FIXING AGENT CAPABILITIES")
    print("=" * 35)

    fix_agent_capabilities()
    fix_enhanced_market_data_agent()

    print("\\n🎯 AGENT CAPABILITY FIX PROCESS COMPLETE!")
