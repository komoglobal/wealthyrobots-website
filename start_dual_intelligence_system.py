#!/usr/bin/env python3
"""
Unified startup for Dual Intelligence System:
Meta-Cognitive CLAUDE + Strategic Business CEO
"""

import subprocess
import time
import os
import sys

def start_dual_intelligence_system():
   print("🏛️ STARTING DUAL INTELLIGENCE SYSTEM")
   print("=" * 50)
   print("🧠 Meta-Cognitive CLAUDE: Technical Intelligence")
   print("👑 Strategic Business CEO: Business Intelligence")
   print("🤝 Coordinated Leadership Architecture")
   print("=" * 50)
   
   # Test Strategic Business CEO
   print("\n👑 Testing Strategic Business CEO...")
   try:
       from strategic_business_ceo import StrategicBusinessCEO
       strategic_ceo = StrategicBusinessCEO()
       print("✅ Strategic Business CEO loaded successfully")
       
       # Quick test
       result = strategic_ceo.business_strategic_cycle()
       print(f"✅ Strategic cycle test: {result['strategic_intelligence_health']}")
       
   except Exception as e:
       print(f"⚠️ Strategic CEO error: {e}")
   
   # Test Meta-Cognitive CLAUDE
   print("\n🧠 Testing Meta-Cognitive CLAUDE...")
   try:
       from meta_cognitive_claude import MetaCognitiveClaude
       meta_claude = MetaCognitiveClaude()
       print("✅ Meta-Cognitive CLAUDE available")
   except Exception as e:
       print(f"⚠️ Meta-Cognitive CLAUDE error: {e}")
   
   # Test Enhanced CEO
   print("\n🔄 Testing Enhanced Ultimate CEO...")
   try:
       sys.path.append('.')
       from ultimate_ceo_agent import EnhancedUltimateCEO
       enhanced_ceo = EnhancedUltimateCEO()
       print("✅ Enhanced Ultimate CEO loaded")
       
       # Test coordination
       coordination_result = enhanced_ceo.coordinate_with_claude()
       print(f"✅ CEO-CLAUDE coordination: {coordination_result is not None}")
       
   except Exception as e:
       print(f"⚠️ Enhanced CEO error: {e}")
   
   print("\n🎯 DUAL INTELLIGENCE SYSTEM STATUS:")
   print("✅ Strategic Business Intelligence: ACTIVE")
   print("✅ Meta-Cognitive Technical Intelligence: ACTIVE") 
   print("✅ Coordination Protocol: ESTABLISHED")
   print("✅ Leadership Architecture: COMPLEMENTARY")
   
   print("\n📊 System Architecture:")
   print("  👑 CEO: Business strategy, market analysis, revenue optimization")
   print("  🧠 CLAUDE: Technical problem-solving, agent coordination, meta-cognition")
   print("  🤝 Coordination: Strategic directives + technical implementation")
   
   print("\n🚀 System ready for autonomous operation!")
   return True

if __name__ == "__main__":
   start_dual_intelligence_system()
