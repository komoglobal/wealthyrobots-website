#!/usr/bin/env python3
"""
Fix CLAUDE Agent Problem Rotation
Add intelligent problem switching to prevent getting stuck
"""

import json
import os
import random
from datetime import datetime

class ClaudeAgentProblemRotator:
    def __init__(self):
        self.empire_problems = [
            "revenue_optimization",
            "content_creation_optimization", 
            "social_media_automation",
            "affiliate_link_optimization",
            "analytics_dashboard_creation",
            "customer_engagement_improvement",
            "seo_content_optimization",
            "conversion_rate_optimization",
            "email_marketing_automation",
            "competitor_analysis_enhancement",
            "payment_system_optimization",
            "user_experience_improvement"
        ]
        
        self.problem_history = []
        self.max_repeats = 3
        
    def load_problem_history(self):
        """Load recent problem history from solution files"""
        try:
            import glob
            solution_files = sorted(glob.glob("claude_solution_*.py"), key=os.path.getmtime, reverse=True)
            
            recent_problems = []
            for file in solution_files[:20]:
                try:
                    with open(file, 'r') as f:
                        content = f.read()
                    
                    for line in content.split('\n'):
                        if 'Problem:' in line:
                            problem = line.split('Problem:')[-1].strip()
                            recent_problems.append(problem)
                            break
                except:
                    continue
            
            self.problem_history = recent_problems
            return recent_problems
        except Exception as e:
            print(f"Error loading problem history: {e}")
            return []
    
    def get_next_problem(self, current_problem=None):
        """Get next problem with intelligent rotation"""
        self.load_problem_history()
        
        # Count how many times current problem appears recently
        if current_problem and self.problem_history:
            recent_count = 0
            for problem in self.problem_history[:10]:
                if problem == current_problem:
                    recent_count += 1
                else:
                    break
            
            if recent_count >= self.max_repeats:
                print(f"🔄 FORCING SWITCH: Stuck on '{current_problem}' for {recent_count} cycles")
                
                # Get problems we haven't worked on recently
                recent_problems = set(self.problem_history[:5])
                available_problems = [p for p in self.empire_problems if p not in recent_problems]
                
                if available_problems:
                    next_problem = random.choice(available_problems)
                    print(f"✅ Switching to: {next_problem}")
                    return next_problem
        
        # Return a random different problem
        if current_problem:
            other_problems = [p for p in self.empire_problems if p != current_problem]
            return random.choice(other_problems)
        else:
            return random.choice(self.empire_problems)
    
    def create_rotation_config(self):
        """Create configuration file for problem rotation"""
        current_problem = "revenue_optimization"
        next_problem = self.get_next_problem(current_problem)
        
        config = {
            "timestamp": datetime.now().isoformat(),
            "action": "problem_rotation_fix",
            "current_problem": current_problem,
            "next_problem": next_problem,
            "rotation_enabled": True,
            "max_repeats": self.max_repeats,
            "available_problems": self.empire_problems
        }
        
        with open('claude_problem_rotation.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Problem rotation config created!")
        print(f"   Current: {current_problem}")
        print(f"   Next: {next_problem}")
        
        return config

def main():
    print("🔄 CLAUDE AGENT PROBLEM ROTATION FIX")
    print("=" * 50)
    
    rotator = ClaudeAgentProblemRotator()
    
    # Analyze current stuck state
    print("📊 Analyzing current problem state...")
    recent_problems = rotator.load_problem_history()
    
    if recent_problems:
        current_problem = recent_problems[0]
        print(f"Current problem: {current_problem}")
        print(f"Problem appears {recent_problems.count(current_problem)} times in recent history")
    
    # Create rotation configuration
    print(f"\n🔧 Creating problem rotation fix...")
    config = rotator.create_rotation_config()
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Stop stuck processes: pkill -f continuous_empire_optimizer")
    print("2. Stop stuck processes: pkill -f empire_intelligence_agent") 
    print("3. Restart with new problem rotation enabled")

if __name__ == "__main__":
    main()
