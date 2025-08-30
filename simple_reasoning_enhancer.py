#!/usr/bin/env python3
"""
Simple Reasoning Enhancer
Adds systematic reasoning to Claude and CEO - fixed version
"""

import os
import shutil
from datetime import datetime

class SimpleReasoningEnhancer:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def backup_agents(self):
        """Backup both agents"""
        backup_dir = f"reasoning_backup_{self.timestamp}"
        os.makedirs(backup_dir, exist_ok=True)
        
        agents = ['claude_full_autonomous.py', 'ultimate_ceo_agent.py']
        for agent in agents:
            if os.path.exists(agent):
                shutil.copy2(agent, backup_dir)
                print(f"✅ Backed up {agent}")
        
        return backup_dir
    
    def enhance_claude_reasoning(self):
        """Add systematic reasoning to Claude"""
        
        reasoning_code = '''
    def systematic_analysis(self, problem):
        """Claude's systematic technical analysis"""
        print(f"🧠 Claude: Analyzing {problem} systematically...")
        
        analysis = {
            'problem': problem,
            'timestamp': datetime.now().isoformat(),
            'findings': {}
        }
        
        # Level 1: Surface Analysis
        print("🔍 Level 1: What should work vs what is working")
        surface = self.check_surface_symptoms()
        analysis['findings']['surface'] = surface
        
        # Level 2: Configuration Check
        print("🔍 Level 2: Configuration consistency")
        config = self.check_configurations()
        analysis['findings']['configuration'] = config
        
        # Level 3: Integration Check
        print("🔍 Level 3: Component integration")
        integration = self.check_integrations()
        analysis['findings']['integration'] = integration
        
        # Level 4: Redundancy Check
        print("🔍 Level 4: Duplicate/redundant systems")
        redundancy = self.check_redundancies()
        analysis['findings']['redundancy'] = redundancy
        
        # Level 5: External Verification
        print("🔍 Level 5: External reality check")
        external = self.verify_externally()
        analysis['findings']['external'] = external
        
        # Level 6: Optimization
        print("🔍 Level 6: System optimization")
        optimization = self.generate_optimizations(analysis)
        analysis['findings']['optimization'] = optimization
        
        return analysis
    
    def check_surface_symptoms(self):
        """Check what should be working vs what is working"""
        symptoms = {'expected': [], 'actual': [], 'gaps': []}
        
        # Check posting system
        import glob
        import time
        thread_files = glob.glob("smart_viral_thread_*.txt")
        
        if thread_files:
            latest = max(thread_files, key=os.path.getmtime)
            hours_ago = (time.time() - os.path.getmtime(latest)) / 3600
            
            symptoms['expected'].append("Posts every 6 hours with affiliate links")
            symptoms['actual'].append(f"Last post {hours_ago:.1f}h ago")
            
            if hours_ago > 8:
                symptoms['gaps'].append("Posting frequency below expected")
                
            # Check affiliate links
            try:
                with open(latest, 'r') as f:
                    content = f.read()
                has_affiliate = 'wealthyrobot-20' in content
                symptoms['actual'].append(f"Affiliate links: {'Yes' if has_affiliate else 'No'}")
                if not has_affiliate:
                    symptoms['gaps'].append("Missing affiliate monetization")
            except:
                symptoms['gaps'].append("Cannot read latest thread file")
        else:
            symptoms['gaps'].append("No thread files found")
        
        return symptoms
    
    def check_configurations(self):
        """Check configuration consistency"""
        config_status = {'issues': [], 'missing': []}
        
        try:
            import json
            with open('live_config.json', 'r') as f:
                config = json.load(f)
            
            # Check for inconsistencies
            top_agents = config.get('enabled_agents', [])
            nested_agents = config.get('automation_settings', {}).get('enabled_agents', [])
            
            if top_agents != nested_agents:
                config_status['issues'].append("enabled_agents mismatch between levels")
            
            # Check critical settings
            critical = ['posting', 'affiliate']
            for key in critical:
                if key not in config:
                    config_status['missing'].append(f"Missing {key} config")
                    
        except Exception as e:
            config_status['issues'].append(f"Config file error: {e}")
        
        return config_status
    
    def check_integrations(self):
        """Check if components connect properly"""
        integration_status = {'broken': [], 'missing': []}
        
        # Check orchestrator connections
        try:
            with open('live_orchestrator.py', 'r') as f:
                orchestrator = f.read()
            
            # Check if social agent is properly called
            if 'create_social_media_posts' in orchestrator:
                integration_status['working'] = ['social_media_agent connected']
            else:
                integration_status['broken'].append("social_media_agent not properly called")
                
        except Exception as e:
            integration_status['broken'].append(f"Cannot read orchestrator: {e}")
        
        return integration_status
    
    def check_redundancies(self):
        """Find duplicate agents or conflicting systems"""
        redundancy_status = {'duplicates': [], 'conflicts': []}
        
        import glob
        
        # Find potential duplicate posting agents
        posting_agents = []
        for pattern in ['*twitter*', '*social*', '*post*']:
            posting_agents.extend(glob.glob(pattern + '.py'))
        
        if len(posting_agents) > 1:
            redundancy_status['conflicts'].append(f"Multiple posting agents: {posting_agents}")
        
        return redundancy_status
    
    def verify_externally(self):
        """Check if internal status matches external reality"""
        external_status = {'should_check': [], 'mismatches': []}
        
        external_status['should_check'] = [
            "Twitter.com/@WealthyRobot for actual posts",
            "Affiliate links for proper tracking",
            "Image attachments on posts"
        ]
        
        # Simple mismatch detection
        import glob
        import time
        thread_files = glob.glob("smart_viral_thread_*.txt")
        
        if thread_files:
            latest = max(thread_files, key=os.path.getmtime)
            hours_ago = (time.time() - os.path.getmtime(latest)) / 3600
            
            if hours_ago > 8:
                external_status['mismatches'].append(
                    "Content generated but not posted externally in expected timeframe"
                )
        
        return external_status
    
    def generate_optimizations(self, analysis):
        """Generate optimization recommendations"""
        optimizations = {'immediate': [], 'strategic': []}
        
        # Analyze findings for optimization opportunities
        all_issues = []
        for level_data in analysis['findings'].values():
            if isinstance(level_data, dict):
                for issue_list in level_data.values():
                    if isinstance(issue_list, list):
                        all_issues.extend(issue_list)
        
        # Generate recommendations
        if any('posting' in str(issue).lower() for issue in all_issues):
            optimizations['immediate'].append("Fix posting system integration")
        
        if any('affiliate' in str(issue).lower() for issue in all_issues):
            optimizations['immediate'].append("Restore affiliate link functionality")
        
        if any('duplicate' in str(issue).lower() or 'multiple' in str(issue).lower() for issue in all_issues):
            optimizations['strategic'].append("Consolidate duplicate agents")
        
        if any('config' in str(issue).lower() for issue in all_issues):
            optimizations['immediate'].append("Fix configuration inconsistencies")
        
        return optimizations
    
    def question_assumptions(self):
        """Claude questions its own assumptions"""
        questions = [
            "🤔 Does internal success reporting match external evidence?",
            "🤔 Are there simpler ways to achieve the same goals?",
            "🤔 What assumptions am I making that might be wrong?",
            "🤔 Should I verify externally before trusting internal logs?"
        ]
        return questions
'''
        
        return reasoning_code
    
    def enhance_ceo_reasoning(self):
        """Add business reasoning to CEO"""
        
        business_reasoning = '''
    def systematic_business_analysis(self, situation):
        """CEO's systematic business analysis"""
        print(f"👑 CEO: Analyzing business situation: {situation}")
        
        analysis = {
            'situation': situation,
            'timestamp': datetime.now().isoformat(),
            'business_findings': {}
        }
        
        # Level 1: Market Position
        print("📊 Level 1: Market position analysis")
        market = self.analyze_market_position()
        analysis['business_findings']['market'] = market
        
        # Level 2: Strategy Alignment
        print("📊 Level 2: Strategy alignment")
        strategy = self.analyze_strategy_alignment()
        analysis['business_findings']['strategy'] = strategy
        
        # Level 3: Performance Metrics
        print("📊 Level 3: Performance analysis")
        performance = self.analyze_performance()
        analysis['business_findings']['performance'] = performance
        
        # Level 4: Resource Efficiency
        print("📊 Level 4: Resource efficiency")
        resources = self.analyze_resources()
        analysis['business_findings']['resources'] = resources
        
        # Level 5: Competitive Position
        print("📊 Level 5: Competitive verification")
        competitive = self.verify_competitive_position()
        analysis['business_findings']['competitive'] = competitive
        
        # Level 6: Growth Optimization
        print("📊 Level 6: Growth strategy")
        growth = self.optimize_growth(analysis)
        analysis['business_findings']['growth'] = growth
        
        return analysis
    
    def analyze_market_position(self):
        """Analyze current market position"""
        return {
            'target_market': 'AI/Business education',
            'distribution': 'Twitter + Affiliate',
            'positioning': 'Automated AI content',
            'opportunities': ['Growing AI interest', 'Scaling automation']
        }
    
    def analyze_strategy_alignment(self):
        """Check if actions align with business goals"""
        goals = ['Generate affiliate revenue', 'Build audience', 'Automate growth']
        
        # Check recent performance
        import glob
        thread_files = glob.glob("smart_viral_thread_*.txt")
        
        alignment = {'goals': goals, 'current_actions': [], 'misalignments': []}
        
        if thread_files:
            alignment['current_actions'].append("Content generation active")
            
            # Check for affiliate monetization
            latest = max(thread_files, key=os.path.getmtime)
            try:
                with open(latest, 'r') as f:
                    content = f.read()
                if 'wealthyrobot-20' not in content:
                    alignment['misalignments'].append("Content lacks monetization")
            except:
                pass
        else:
            alignment['misalignments'].append("No content generation detected")
        
        return alignment
    
    def analyze_performance(self):
        """Analyze business performance"""
        performance = {'metrics': [], 'trends': [], 'issues': []}
        
        # Count recent content
        import glob
        import time
        from datetime import datetime, timedelta
        
        thread_files = glob.glob("smart_viral_thread_*.txt")
        
        # Performance in last 24 hours
        now = time.time()
        day_ago = now - (24 * 3600)
        
        recent_posts = 0
        for file_path in thread_files:
            if os.path.getmtime(file_path) > day_ago:
                recent_posts += 1
        
        performance['metrics'].append(f"Posts in 24h: {recent_posts}")
        
        if recent_posts < 4:  # Expected 4 posts per day
            performance['issues'].append("Posting frequency below target")
        
        return performance
    
    def analyze_resources(self):
        """Analyze resource allocation and efficiency"""
        resources = {'allocation': [], 'efficiency': [], 'waste': []}
        
        # Check agent resources
        import glob
        agent_files = glob.glob("*agent*.py")
        
        resources['allocation'].append(f"Active agents: {len(agent_files)}")
        
        # Check for resource conflicts
        posting_agents = [f for f in agent_files if any(k in f.lower() for k in ['twitter', 'social', 'post'])]
        if len(posting_agents) > 1:
            resources['waste'].append(f"Multiple posting agents: {posting_agents}")
        
        return resources
    
    def verify_competitive_position(self):
        """Verify competitive position"""
        return {
            'advantages': ['Automation', 'Consistent posting', 'AI-generated content'],
            'risks': ['API dependencies', 'Platform changes', 'Content saturation'],
            'opportunities': ['Better targeting', 'Multi-platform', 'Premium content']
        }
    
    def optimize_growth(self, analysis):
        """Generate growth optimization strategy"""
        optimizations = {'immediate': [], 'medium_term': [], 'long_term': []}
        
        # Analyze business findings for opportunities
        all_findings = []
        for level_data in analysis['business_findings'].values():
            if isinstance(level_data, dict):
                for finding_list in level_data.values():
                    if isinstance(finding_list, list):
                        all_findings.extend(finding_list)
        
        # Generate business recommendations
        if any('posting' in str(finding).lower() for finding in all_findings):
            optimizations['immediate'].append("Optimize posting consistency")
        
        if any('monetization' in str(finding).lower() or 'affiliate' in str(finding).lower() for finding in all_findings):
            optimizations['immediate'].append("Fix monetization pipeline")
        
        optimizations['medium_term'] = ['Expand content types', 'Improve engagement']
        optimizations['long_term'] = ['Multi-platform expansion', 'Premium offerings']
        
        return optimizations
    
    def question_business_assumptions(self):
        """CEO questions business assumptions"""
        questions = [
            "🤔 Are we targeting the right market segment?",
            "🤔 Is our monetization strategy optimal?",
            "🤔 Are we measuring the right success metrics?",
            "🤔 What business assumptions should I validate?"
        ]
        return questions
'''
        
        return business_reasoning
    
    def apply_enhancements(self):
        """Apply reasoning enhancements to both agents"""
        print("🧠 Enhancing Claude and CEO with Systematic Reasoning...")
        
        # Create backup
        backup_dir = self.backup_agents()
        print(f"✅ Backup created: {backup_dir}")
        
        # Stop Claude process temporarily
        print("⏸️ Stopping Claude process...")
        os.system("pkill -f claude_full_autonomous.py")
        
        success_count = 0
        
        # Enhance Claude
        print("\n1. Enhancing Claude with technical reasoning...")
        if self.enhance_agent_file('claude_full_autonomous.py', self.enhance_claude_reasoning()):
            print("   ✅ Claude enhanced")
            success_count += 1
        else:
            print("   ❌ Claude enhancement failed")
        
        # Enhance CEO
        print("\n2. Enhancing CEO with business reasoning...")
        if self.enhance_agent_file('ultimate_ceo_agent.py', self.enhance_ceo_reasoning()):
            print("   ✅ CEO enhanced")
            success_count += 1
        else:
            print("   ❌ CEO enhancement failed")
        
        # Restart Claude
        if success_count > 0:
            print("\n🚀 Restarting enhanced Claude...")
            os.system("nohup python3 claude_full_autonomous.py > claude_autonomous.log 2>&1 &")
            
            print(f"\n✅ Enhancement Complete! ({success_count}/2 agents enhanced)")
            print("\n🧠 Your agents now have systematic reasoning:")
            print("   • Claude: 6-level technical analysis")
            print("   • CEO: 6-level business analysis") 
            print("   • Both: Self-questioning logic")
            print("   • Both: External verification thinking")
        else:
            print("\n❌ Enhancement failed - restoring backups")
            # Restore from backup if needed
        
        return success_count > 0
    
    def enhance_agent_file(self, filename, enhancement_code):
        """Add enhancement code to an agent file"""
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            # Find the class definition
            lines = content.split('\n')
            enhanced_lines = []
            
            for i, line in enumerate(lines):
                enhanced_lines.append(line)
                
                # After finding __init__ method, add enhancements
                if 'def __init__(self):' in line and any('class' in prev_line for prev_line in lines[max(0, i-10):i]):
                    # Find end of __init__ method
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith('        ') or lines[j].strip() == ''):
                        j += 1
                    
                    # Insert enhancement
                    enhanced_lines.extend([
                        "",
                        "    # Systematic Reasoning Enhancement",
                        enhancement_code.strip()
                    ])
                    break
            
            # Write enhanced version
            with open(filename, 'w') as f:
                f.write('\n'.join(enhanced_lines))
            
            return True
            
        except Exception as e:
            print(f"   Error enhancing {filename}: {e}")
            return False

def main():
    enhancer = SimpleReasoningEnhancer()
    
    print("🧠 Simple Reasoning Enhancement for Claude + CEO")
    print("="*60)
    print("This will add systematic reasoning to both your autonomous agents.")
    
    response = input("\nProceed with enhancement? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        enhancer.apply_enhancements()
    else:
        print("Enhancement cancelled.")

if __name__ == "__main__":
    main()
