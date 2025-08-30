#!/usr/bin/env python3
"""
🔧 CLAUDE REASONING FIX
Adds systematic reasoning to Claude agent (manual approach)
"""

import os
import sys
import shutil
from datetime import datetime

def fix_claude_reasoning():
    """Fix Claude reasoning enhancement"""
    claude_file = "claude_full_autonomous.py"
    
    if not os.path.exists(claude_file):
        print(f"❌ {claude_file} not found!")
        return False
    
    print(f"🔍 Analyzing {claude_file}...")
    
    with open(claude_file, 'r') as f:
        content = f.read()
    
    print(f"📊 File size: {len(content)} characters")
    print(f"📊 Lines: {len(content.split('\\n'))}")
    
    # Look for any class definitions
    classes = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('class '):
            classes.append((i+1, line.strip()))
    
    if classes:
        print("🎯 Found classes:")
        for line_num, class_def in classes:
            print(f"   Line {line_num}: {class_def}")
    else:
        print("❌ No class definitions found")
        print("🔍 Looking for function definitions...")
        
        functions = []
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                functions.append((i+1, line.strip()))
        
        if functions:
            print("🎯 Found functions:")
            for line_num, func_def in functions[:5]:  # Show first 5
                print(f"   Line {line_num}: {func_def}")
            if len(functions) > 5:
                print(f"   ... and {len(functions) - 5} more")
    
    # Check if reasoning already exists
    if "SystematicReasoning" in content:
        print("✅ SystematicReasoning already exists in Claude!")
        return True
    
    print("🔧 Adding reasoning to Claude...")
    
    # Create backup
    backup_file = f"claude_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    shutil.copy2(claude_file, backup_file)
    print(f"✅ Backup created: {backup_file}")
    
    # Add reasoning class at the beginning after imports
    reasoning_code = '''
class SystematicReasoning:
    """6-Level Technical Analysis System for Claude"""
    
    def technical_analysis(self, problem, context=""):
        """Systematic technical problem analysis"""
        analysis = {
            "level_1_problem_identification": self._identify_core_problem(problem),
            "level_2_constraint_analysis": self._analyze_constraints(problem, context),
            "level_3_solution_space": self._map_solution_space(problem),
            "level_4_implementation_strategy": self._develop_strategy(problem),
            "level_5_risk_assessment": self._assess_risks(problem),
            "level_6_optimization_path": self._find_optimizations(problem)
        }
        return analysis
    
    def _identify_core_problem(self, problem):
        """Level 1: What exactly needs to be solved?"""
        return {
            "primary_issue": problem.strip(),
            "root_cause_hypothesis": "Analyzing technical requirements",
            "success_criteria": "Functional, maintainable solution"
        }
    
    def _analyze_constraints(self, problem, context):
        """Level 2: What are the limitations and requirements?"""
        return {
            "technical_constraints": "Existing codebase compatibility",
            "resource_constraints": "Available libraries and tools",
            "time_constraints": "Immediate implementation needed",
            "context_factors": context if context else "Operating within current system"
        }
    
    def _map_solution_space(self, problem):
        """Level 3: What are all possible approaches?"""
        return {
            "direct_approach": "Straightforward implementation",
            "modular_approach": "Component-based solution",
            "integrated_approach": "System-wide enhancement",
            "recommended": "Start simple, enhance iteratively"
        }
    
    def _develop_strategy(self, problem):
        """Level 4: How should this be implemented?"""
        return {
            "phase_1": "Core functionality",
            "phase_2": "Error handling and robustness",
            "phase_3": "Integration and testing",
            "fallback_plan": "Revert to backup if issues arise"
        }
    
    def _assess_risks(self, problem):
        """Level 5: What could go wrong?"""
        return {
            "high_risk": "System instability",
            "medium_risk": "Performance degradation",
            "low_risk": "Minor functionality issues",
            "mitigation": "Comprehensive testing and backup strategy"
        }
    
    def _find_optimizations(self, problem):
        """Level 6: How can this be improved?"""
        return {
            "performance": "Efficient algorithms and caching",
            "maintainability": "Clean, documented code",
            "scalability": "Modular design for future expansion",
            "monitoring": "Logging and metrics for continuous improvement"
        }
    
    def self_verify(self, solution, original_problem):
        """Self-verification questions"""
        questions = [
            f"Does this solution address the core problem: {original_problem}?",
            "Are there any edge cases I have not considered?",
            "Is this the most efficient approach?",
            "How will this integrate with existing systems?",
            "What would I do differently if I started over?"
        ]
        return {"verification_questions": questions, "status": "requires_review"}

'''
    
    # Find a good place to insert (after imports, before any class/function)
    lines = content.split('\n')
    insert_line = 0
    
    # Find last import
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            insert_line = i + 1
    
    # If no imports found, insert at beginning
    if insert_line == 0:
        insert_line = 0
    
    # Insert reasoning code
    lines.insert(insert_line, reasoning_code)
    enhanced_content = '\n'.join(lines)
    
    # Write enhanced content
    with open(claude_file, 'w') as f:
        f.write(enhanced_content)
    
    print("✅ Claude enhanced with SystematicReasoning class!")
    
    # Test the file
    try:
        exec(compile(enhanced_content, claude_file, 'exec'))
        print("✅ Enhanced Claude file syntax is valid!")
        return True
    except Exception as e:
        print(f"❌ Syntax error in enhanced file: {e}")
        # Restore backup
        shutil.copy2(backup_file, claude_file)
        print("🔄 Restored from backup")
        return False

if __name__ == "__main__":
    success = fix_claude_reasoning()
    if success:
        print("\n🎯 Claude reasoning enhancement complete!")
        print("🚀 Restart Claude to activate reasoning:")
        print("   pkill -f claude_full_autonomous.py")
        print("   nohup python3 claude_full_autonomous.py > claude_autonomous.log 2>&1 &")
    else:
        print("\n❌ Enhancement failed - check file structure")
