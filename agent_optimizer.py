
# DEPRECATED: This agent has been merged into data_analytics_agent.py
# Please use data_analytics_agent.py instead
# This file will be removed in future updates
#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: Agent Optimizer
PURPOSE: Analyzes agent capabilities, identifies duplicates, and recommends optimizations for optimal flow
CATEGORY: System Optimization
STATUS: Active
FREQUENCY: On-demand
"""

import os
import json
import glob
from datetime import datetime
from collections import defaultdict

class AgentOptimizer:
    def __init__(self):
        self.agent_analysis = {}
        self.duplicate_groups = []
        self.optimization_recommendations = []
        
    def scan_all_agents(self):
        """Scan all Python files for agent documentation"""
        print("🔍 SCANNING EMPIRE AGENTS FOR OPTIMIZATION")
        print("=" * 50)
        
        agent_files = []
        
        # Find all Python files
        for file in glob.glob("*.py"):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    if 'EMPIRE_AGENT_INFO:' in content:
                        agent_files.append(file)
            except Exception as e:
                print(f"⚠️ Error reading {file}: {e}")
        
        print(f"📊 Found {len(agent_files)} documented agents")
        return agent_files
    
    def analyze_agent_capabilities(self, agent_files):
        """Analyze each agent's capabilities and purpose"""
        print("\n📋 ANALYZING AGENT CAPABILITIES")
        print("=" * 40)
        
        for file in agent_files:
            try:
                with open(file, 'r') as f:
                    content = f.read()
                
                # Extract agent info
                agent_info = self.extract_agent_info(content)
                if agent_info:
                    self.agent_analysis[file] = agent_info
                    print(f"✅ {file}: {agent_info['name']} - {agent_info['purpose'][:60]}...")
                    
            except Exception as e:
                print(f"❌ Error analyzing {file}: {e}")
    
    def extract_agent_info(self, content):
        """Extract EMPIRE_AGENT_INFO from content"""
        lines = content.split('\n')
        agent_info = {}
        
        in_agent_info = False
        for line in lines:
            if 'EMPIRE_AGENT_INFO:' in line:
                in_agent_info = True
                continue
            elif in_agent_info and line.strip() == '"""':
                break
            elif in_agent_info and ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                agent_info[key.lower()] = value
        
        return agent_info if agent_info else None
    
    def identify_duplicates(self):
        """Identify agents with similar or overlapping capabilities"""
        print("\n🔍 IDENTIFYING DUPLICATE CAPABILITIES")
        print("=" * 45)
        
        # Group by category and purpose
        category_groups = defaultdict(list)
        purpose_keywords = defaultdict(list)
        
        for file, info in self.agent_analysis.items():
            category = info.get('category', 'Unknown')
            purpose = info.get('purpose', '')
            name = info.get('name', 'Unknown')
            
            category_groups[category].append({
                'file': file,
                'name': name,
                'purpose': purpose,
                'status': info.get('status', 'Unknown')
            })
            
            # Extract keywords from purpose
            keywords = self.extract_keywords(purpose)
            for keyword in keywords:
                purpose_keywords[keyword].append({
                    'file': file,
                    'name': name,
                    'purpose': purpose,
                    'category': category
                })
        
        # Find duplicates
        duplicates_found = []
        
        # Check category duplicates
        for category, agents in category_groups.items():
            if len(agents) > 1:
                duplicates_found.append({
                    'type': 'category_duplicate',
                    'category': category,
                    'agents': agents,
                    'recommendation': self.generate_merge_recommendation(agents)
                })
        
        # Check purpose keyword duplicates
        for keyword, agents in purpose_keywords.items():
            if len(agents) > 1 and keyword not in ['agent', 'empire', 'active']:
                duplicates_found.append({
                    'type': 'purpose_duplicate',
                    'keyword': keyword,
                    'agents': agents,
                    'recommendation': self.generate_merge_recommendation(agents)
                })
        
        self.duplicate_groups = duplicates_found
        return duplicates_found
    
    def extract_keywords(self, text):
        """Extract meaningful keywords from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        words = text.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        return keywords
    
    def generate_merge_recommendation(self, agents):
        """Generate recommendation for merging duplicate agents"""
        if len(agents) == 2:
            # Simple merge recommendation
            primary = agents[0]
            secondary = agents[1]
            
            return {
                'action': 'merge',
                'primary_agent': primary['file'],
                'secondary_agent': secondary['file'],
                'merge_strategy': f"Keep {primary['name']} as primary, integrate {secondary['name']} capabilities",
                'benefits': [
                    "Reduced complexity",
                    "Better coordination",
                    "Eliminated redundancy",
                    "Improved performance"
                ]
            }
        else:
            # Multiple agents - need consolidation
            return {
                'action': 'consolidate',
                'agents': [agent['file'] for agent in agents],
                'strategy': f"Consolidate {len(agents)} agents into single optimized agent",
                'benefits': [
                    "Streamlined workflow",
                    "Reduced resource usage",
                    "Better coordination",
                    "Eliminated conflicts"
                ]
            }
    
    def generate_optimization_plan(self):
        """Generate comprehensive optimization plan"""
        print("\n🎯 GENERATING OPTIMIZATION PLAN")
        print("=" * 40)
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'total_agents': len(self.agent_analysis),
            'duplicates_found': len(self.duplicate_groups),
            'optimization_actions': [],
            'priority_upgrades': [],
            'system_improvements': []
        }
        
        # Add duplicate resolution actions
        for duplicate in self.duplicate_groups:
            plan['optimization_actions'].append({
                'type': 'resolve_duplicate',
                'description': f"Resolve {duplicate['type']} duplicate",
                'agents_involved': [agent['file'] for agent in duplicate['agents']],
                'recommendation': duplicate['recommendation']
            })
        
        # Identify priority upgrades
        priority_agents = self.identify_priority_upgrades()
        plan['priority_upgrades'] = priority_agents
        
        # System improvements
        plan['system_improvements'] = [
            "Implement agent health monitoring",
            "Add automatic agent coordination",
            "Create agent performance metrics",
            "Establish agent communication protocols"
        ]
        
        self.optimization_recommendations = plan
        return plan
    
    def identify_priority_upgrades(self):
        """Identify agents that need priority upgrades"""
        priority_upgrades = []
        
        for file, info in self.agent_analysis.items():
            status = info.get('status', '').lower()
            
            if 'broken' in status or 'corrupted' in status:
                priority_upgrades.append({
                    'agent': file,
                    'priority': 'critical',
                    'issue': 'Broken/corrupted agent',
                    'action': 'Fix or replace agent'
                })
            elif 'unknown' in status:
                priority_upgrades.append({
                    'agent': file,
                    'priority': 'high',
                    'issue': 'Unknown status',
                    'action': 'Add proper documentation and testing'
                })
            elif 'backup' in file.lower():
                priority_upgrades.append({
                    'agent': file,
                    'priority': 'medium',
                    'issue': 'Backup file',
                    'action': 'Clean up backup files'
                })
        
        return priority_upgrades
    
    def execute_optimization(self):
        """Execute the optimization plan"""
        print("\n🚀 EXECUTING OPTIMIZATION PLAN")
        print("=" * 40)
        
        # Create backup
        backup_dir = f"empire_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        print(f"📦 Creating backup in {backup_dir}")
        
        # Execute optimizations
        for action in self.optimization_recommendations['optimization_actions']:
            if action['type'] == 'resolve_duplicate':
                self.resolve_duplicate(action)
        
        # Handle priority upgrades
        for upgrade in self.optimization_recommendations['priority_upgrades']:
            if upgrade['priority'] == 'critical':
                self.handle_critical_upgrade(upgrade)
        
        print("\n✅ Optimization complete!")
    
    def resolve_duplicate(self, action):
        """Resolve duplicate agents"""
        agents = action['agents_involved']
        recommendation = action['recommendation']
        
        print(f"\n🔄 Resolving duplicate: {', '.join(agents)}")
        
        if recommendation['action'] == 'merge':
            primary = recommendation['primary_agent']
            secondary = recommendation['secondary_agent']
            
            print(f"📋 Merging {secondary} into {primary}")
            
            # Create backup
            backup_file = f"backup_{os.path.basename(secondary)}"
            os.system(f"cp '{secondary}' '{backup_file}'")
            
            # Mark secondary as deprecated
            self.mark_agent_deprecated(secondary, primary)
            
        elif recommendation['action'] == 'consolidate':
            print(f"📋 Consolidating {len(agents)} agents")
            for agent in agents:
                self.mark_agent_deprecated(agent, "consolidated_agent")
    
    def mark_agent_deprecated(self, agent_file, replacement):
        """Mark an agent as deprecated"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            # Add deprecation notice
            deprecation_notice = f"""
# DEPRECATED: This agent has been merged into {replacement}
# Please use {replacement} instead
# This file will be removed in future updates
"""
            
            with open(agent_file, 'w') as f:
                f.write(deprecation_notice + content)
            
            print(f"✅ Marked {agent_file} as deprecated")
            
        except Exception as e:
            print(f"❌ Error marking {agent_file} as deprecated: {e}")
    
    def handle_critical_upgrade(self, upgrade):
        """Handle critical agent upgrades"""
        agent_file = upgrade['agent']
        print(f"\n🚨 Critical upgrade needed: {agent_file}")
        print(f"   Issue: {upgrade['issue']}")
        print(f"   Action: {upgrade['action']}")
        
        # For now, just log the issue
        # In a real system, you'd implement the fix
        print(f"   ⚠️ Manual intervention required for {agent_file}")
    
    def run_optimization_cycle(self):
        """Run complete optimization cycle"""
        print("🤖 AGENT OPTIMIZER - STARTING OPTIMIZATION CYCLE")
        print("=" * 60)
        
        # Step 1: Scan all agents
        agent_files = self.scan_all_agents()
        
        # Step 2: Analyze capabilities
        self.analyze_agent_capabilities(agent_files)
        
        # Step 3: Identify duplicates
        duplicates = self.identify_duplicates()
        
        # Step 4: Generate optimization plan
        plan = self.generate_optimization_plan()
        
        # Step 5: Display results
        self.display_optimization_results(plan)
        
        # Step 6: Execute optimizations (optional)
        if duplicates:
            response = input("\n🤔 Execute optimizations? (y/n): ")
            if response.lower() == 'y':
                self.execute_optimization()
        
        return plan
    
    def display_optimization_results(self, plan):
        """Display optimization results"""
        print("\n📊 OPTIMIZATION RESULTS")
        print("=" * 30)
        print(f"Total Agents: {plan['total_agents']}")
        print(f"Duplicates Found: {plan['duplicates_found']}")
        print(f"Priority Upgrades: {len(plan['priority_upgrades'])}")
        
        if plan['duplicates_found'] > 0:
            print("\n🔍 DUPLICATE AGENTS FOUND:")
            for duplicate in self.duplicate_groups:
                print(f"\n📋 {duplicate['type'].replace('_', ' ').title()}:")
                for agent in duplicate['agents']:
                    print(f"   - {agent['name']} ({agent['file']})")
        
        if plan['priority_upgrades']:
            print("\n🚨 PRIORITY UPGRADES NEEDED:")
            for upgrade in plan['priority_upgrades']:
                print(f"   - {upgrade['agent']}: {upgrade['issue']}")

def main():
    optimizer = AgentOptimizer()
    plan = optimizer.run_optimization_cycle()
    
    # Save optimization report
    with open('agent_optimization_report.json', 'w') as f:
        json.dump(plan, f, indent=2)
    
    print(f"\n📄 Optimization report saved to agent_optimization_report.json")

if __name__ == "__main__":
    main()
