#!/usr/bin/env python3
"""
Enhanced startup script for meta-cognitive CLAUDE agent
"""

import subprocess
import time
import os
import sys

def start_enhanced_claude():
   print("🚀 STARTING META-COGNITIVE CLAUDE AGENT")
   print("=" * 50)
   
   # Test meta-cognitive system
   print("🧪 Testing meta-cognitive system...")
   try:
       from meta_cognitive_claude import MetaCognitiveClaude
       meta_claude = MetaCognitiveClaude()
       print("✅ Meta-cognitive CLAUDE loaded successfully")
       
       # Quick test
       result = meta_claude.meta_cognitive_cycle()
       print(f"✅ Meta-cognitive test: {result['meta_cognitive_health']}")
       
   except Exception as e:
       print(f"⚠️ Meta-cognitive system error: {e}")
       print("Proceeding with basic integration...")
   
   # Start enhanced autonomous agent
   print("\n🤖 Starting enhanced autonomous agent...")
   
   try:
       # Try to import enhanced version
       sys.path.append('.')
       from claude_full_autonomous import EnhancedClaudeAutonomous
       
       enhanced_claude = EnhancedClaudeAutonomous()
       
       print("✅ Enhanced CLAUDE agent started!")
       print("🎯 Capabilities enabled:")
       print("   • Self-awareness and monitoring")
       print("   • Stuck behavior detection") 
       print("   • Creative problem solving")
       print("   • Autonomous self-improvement")
       
       # Run a few enhanced cycles for demo
       for cycle in range(3):
           print(f"\n🔄 Enhanced Cycle #{cycle + 1}")
           try:
               result = enhanced_claude.run_enhanced_autonomous_cycle()
               print(f"   Result: {result}")
           except Exception as e:
               print(f"   Error: {e}")
           
           time.sleep(5)  # Short delay for demo
       
       print("\n🎊 Meta-cognitive CLAUDE demonstration completed!")
       
   except Exception as e:
       print(f"❌ Error starting enhanced CLAUDE: {e}")
       print("Falling back to standard autonomous mode...")
       
       # Fallback to standard mode
       try:
           subprocess.run(['python3', '-c', '''
import sys
sys.path.append(".")
from claude_full_autonomous import ClaudeFullAutonomous
claude = ClaudeFullAutonomous()
print("Standard CLAUDE autonomous mode active")
'''], timeout=10)
       except Exception as fallback_error:
           print(f"Fallback also failed: {fallback_error}")

if __name__ == "__main__":
   start_enhanced_claude()
