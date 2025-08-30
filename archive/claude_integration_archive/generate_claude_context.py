#!/usr/bin/env python3
"""
Quick Claude Context Generator for WealthyRobot
Generates comprehensive documentation for Claude in new chats
"""

import os
import json
from datetime import datetime

def scan_project():
    """Scan the current project and generate context"""
    
    context = {
        "project_name": "WealthyRobot Autonomous Business Empire",
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "FULLY OPERATIONAL",
        "files_analyzed": {},
        "system_summary": {}
    }
    
    print("🔍 Scanning WealthyRobot project...")
    
    # Scan Python files
    python_files = [f for f in os.listdir('.') if f.endswith('.py')]
    
    for file in python_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_info = {
                "size_kb": round(len(content) / 1024, 2),
                "lines": len(content.split('\n')),
                "classes": content.count('class '),
                "functions": content.count('def '),
                "imports": content.count('import '),
                "has_main": '__main__' in content,
                "key_features": []
            }
            
            # Detect key features
            if 'live' in file.lower():
                file_info["key_features"].append("Live Control System")
            if 'ceo' in file.lower():
                file_info["key_features"].append("AI CEO Agent")
            if 'orchestrator' in file.lower():
                file_info["key_features"].append("Main Orchestrator")
            if 'agent' in file.lower():
                file_info["key_features"].append("AI Agent")
            if 'config' in file.lower():
                file_info["key_features"].append("Configuration Management")
            
            context["files_analyzed"][file] = file_info
            
        except Exception as e:
            context["files_analyzed"][file] = {"error": str(e)}
    
    # Generate system summary
    total_files = len(context["files_analyzed"])
    total_lines = sum(f.get("lines", 0) for f in context["files_analyzed"].values() if isinstance(f, dict))
    total_classes = sum(f.get("classes", 0) for f in context["files_analyzed"].values() if isinstance(f, dict))
    
    context["system_summary"] = {
        "total_python_files": total_files,
        "total_lines_of_code": total_lines,
        "total_classes": total_classes,
        "key_components": identify_key_components(context["files_analyzed"]),
        "architecture_type": "Agent-Based with Live Controls"
    }
    
    return context

def identify_key_components(files):
    """Identify key system components"""
    components = []
    
    for filename, info in files.items():
        if isinstance(info, dict) and "key_features" in info:
            for feature in info["key_features"]:
                components.append({
                    "file": filename,
                    "component": feature,
                    "size": info.get("size_kb", 0)
                })
    
    return sorted(components, key=lambda x: x["size"], reverse=True)

def generate_claude_summary(context):
    """Generate Claude-friendly summary"""
    
    summary = f"""# WealthyRobot - Claude Context Summary
*Generated: {context['scan_date']}*

## 🤖 SYSTEM OVERVIEW
**Project:** {context['project_name']}
**Status:** {context['status']}
**Architecture:** {context['system_summary']['architecture_type']}

## 📊 SYSTEM STATS
- **Python Files:** {context['system_summary']['total_python_files']}
- **Lines of Code:** {context['system_summary']['total_lines_of_code']:,}
- **Classes:** {context['system_summary']['total_classes']}

## 🏗️ KEY COMPONENTS
"""
    
    for component in context['system_summary']['key_components']:
        summary += f"- **{component['file']}** - {component['component']} ({component['size']} KB)\n"
    
    summary += "\n## 📁 FILE DETAILS\n"
    
    for filename, info in context['files_analyzed'].items():
        if isinstance(info, dict) and 'lines' in info:
            features = ", ".join(info.get('key_features', ['General']))
            summary += f"- **{filename}** ({info['lines']} lines) - {features}\n"
    
    summary += """
## 🎮 CURRENT CAPABILITIES
✅ Live control system operational
✅ AI CEO making autonomous decisions  
✅ Real-time configuration changes
✅ Pause/resume automation
✅ Emergency stop functionality
✅ Budget and risk adjustment

## 🚀 DEPLOYMENT STATUS
- Environment: Ubuntu 24.04 AWS EC2
- Python: 3.12 virtual environment
- APIs: OpenAI, Twitter, Amazon Associates
- Operation: 24/7 autonomous capability

## 💡 USAGE NOTES
- Use `python3 live_orchestrator.py` to start system
- Use `python3 live_control.py` for interactive control
- Edit `live_config.json` for real-time changes
- System auto-creates config files on first run
"""
    
    return summary

def main():
    """Main function"""
    print("🤖 CLAUDE CONTEXT GENERATOR FOR WEALTHYROBOT")
    print("=" * 60)
    
    # Scan project
    context = scan_project()
    
    # Generate summary
    summary = generate_claude_summary(context)
    
    # Save files
    with open('claude_context_full.json', 'w') as f:
        json.dump(context, f, indent=2)
    
    with open('CLAUDE_SUMMARY.md', 'w') as f:
        f.write(summary)
    
    print(f"\n✅ Analysis complete!")
    print(f"📁 Full context: claude_context_full.json")
    print(f"📋 Claude summary: CLAUDE_SUMMARY.md")
    print(f"📄 Main context: WEALTHYROBOT_CONTEXT.md")
    
    print(f"\n🎯 USAGE:")
    print(f"Copy content from CLAUDE_SUMMARY.md or WEALTHYROBOT_CONTEXT.md")
    print(f"Paste into new Claude chats for instant context!")

if __name__ == "__main__":
    main()
