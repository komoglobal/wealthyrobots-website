#!/usr/bin/env python3
"""
Visual Agent Code Extractor
Extracts and displays your visual generation agent code for analysis
"""

import os
import sys
from pathlib import Path

def extract_visual_agent_code():
    """Extract and display visual agent code files"""
    
    # List of visual agent files to extract
    visual_agents = [
        'visual_affiliate_agent.py',
        'visual_content_agent.py', 
        'ai_image_generator_agent.py',
        'twitter_visual_enhancement.py',
        'twitter_visual_verifier.py',
        'visual_enhancement.py',
        'hybrid_visual_system.py'
    ]
    
    print("=" * 80)
    print("🎨 VISUAL AGENT CODE EXTRACTION")
    print("=" * 80)
    print()
    
    current_dir = Path.cwd()
    extracted_count = 0
    
    for agent_file in visual_agents:
        file_path = current_dir / agent_file
        
        if file_path.exists():
            print(f"📄 {agent_file}")
            print("-" * 60)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Show file size and line count
                lines = content.split('\n')
                print(f"📊 Size: {len(content)} chars, {len(lines)} lines")
                print()
                
                # Display the code
                print("```python")
                print(content)
                print("```")
                print()
                print("=" * 80)
                print()
                
                extracted_count += 1
                
            except Exception as e:
                print(f"❌ Error reading {agent_file}: {e}")
                print()
        else:
            print(f"⚠️  {agent_file} - Not found")
            print()
    
    # Also check for any visual-related configuration files
    config_files = [
        'live_config.json',
        'twitter_visual_branding_guide.json'
    ]
    
    print("🔧 VISUAL CONFIGURATION FILES")
    print("-" * 60)
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"📋 {config_file}")
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                print("```json")
                print(content[:1000])  # First 1000 chars
                if len(content) > 1000:
                    print("... (truncated)")
                print("```")
                print()
            except Exception as e:
                print(f"Error reading {config_file}: {e}")
    
    print("=" * 80)
    print(f"✅ EXTRACTION COMPLETE - Found {extracted_count} visual agents")
    print("📋 Copy the output above and paste it to Claude for analysis")
    print("=" * 80)

if __name__ == "__main__":
    extract_visual_agent_code()
