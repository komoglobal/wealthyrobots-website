#!/usr/bin/env python3
"""
WealthyRobot System Analyzer
Analyzes existing agents and configurations to understand current affiliate link system
"""

import os
import json
import glob
from datetime import datetime

class SystemAnalyzer:
    def __init__(self):
        self.analysis_report = {
            'timestamp': datetime.now().isoformat(),
            'agents_found': [],
            'config_analysis': {},
            'affiliate_systems': [],
            'content_systems': [],
            'visual_systems': [],
            'issues_identified': [],
            'recommendations': []
        }
    
    def scan_affiliate_agents(self):
        """Find all agents related to affiliate marketing"""
        affiliate_keywords = ['affiliate', 'money', 'revenue', 'product', 'amazon']
        affiliate_agents = []
        
        python_files = glob.glob("*.py")
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                
                # Check if file contains affiliate-related keywords
                if any(keyword in content for keyword in affiliate_keywords):
                    file_info = {
                        'file': file_path,
                        'size': len(content),
                        'has_amazon': 'amazon' in content,
                        'has_wealthyrobot_tag': 'wealthyrobot-20' in content,
                        'has_affiliate_logic': 'affiliate' in content,
                        'last_modified': os.path.getmtime(file_path)
                    }
                    affiliate_agents.append(file_info)
                    
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        return affiliate_agents
    
    def scan_content_agents(self):
        """Find all agents related to content generation"""
        content_keywords = ['content', 'thread', 'post', 'viral', 'social']
        content_agents = []
        
        python_files = glob.glob("*.py")
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                
                if any(keyword in content for keyword in content_keywords):
                    file_info = {
                        'file': file_path,
                        'size': len(content),
                        'generates_content': 'def generate' in content or 'def create' in content,
                        'has_twitter': 'twitter' in content,
                        'has_posting': 'post' in content,
                        'last_modified': os.path.getmtime(file_path)
                    }
                    content_agents.append(file_info)
                    
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        return content_agents
    
    def scan_visual_agents(self):
        """Find all agents related to visual content"""
        visual_keywords = ['visual', 'image', 'graphic', 'photo', 'png', 'jpg']
        visual_agents = []
        
        python_files = glob.glob("*.py")
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                
                if any(keyword in content for keyword in visual_keywords):
                    file_info = {
                        'file': file_path,
                        'size': len(content),
                        'creates_images': 'image' in content,
                        'has_pillow': 'pil' in content or 'pillow' in content,
                        'last_modified': os.path.getmtime(file_path)
                    }
                    visual_agents.append(file_info)
                    
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        return visual_agents
    
    def analyze_live_config(self):
        """Analyze the live configuration"""
        try:
            with open('live_config.json', 'r') as f:
                config = json.load(f)
            
            analysis = {
                'file_exists': True,
                'has_affiliate_config': 'affiliate' in config,
                'has_content_config': 'content' in config,
                'has_posting_config': 'posting' in config,
                'config_keys': list(config.keys())
            }
            
            if 'affiliate' in config:
                analysis['affiliate_details'] = config['affiliate']
            
            return analysis
            
        except FileNotFoundError:
            return {'file_exists': False, 'error': 'live_config.json not found'}
        except Exception as e:
            return {'file_exists': True, 'error': str(e)}
    
    def check_orchestrator_integration(self):
        """Check how the orchestrator integrates different systems"""
        orchestrator_files = ['live_orchestrator.py', 'orchestrator.py', 'universal_agent_coordinator.py']
        
        for file_path in orchestrator_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    integration_info = {
                        'file': file_path,
                        'imports_affiliate_agents': self.count_imports(content, 'affiliate'),
                        'imports_content_agents': self.count_imports(content, 'content'),
                        'imports_visual_agents': self.count_imports(content, 'visual'),
                        'has_coordination_logic': 'coordinate' in content.lower() or 'orchestrate' in content.lower(),
                        'size': len(content)
                    }
                    
                    return integration_info
                    
                except Exception as e:
                    return {'file': file_path, 'error': str(e)}
        
        return {'error': 'No orchestrator file found'}
    
    def count_imports(self, content, keyword):
        """Count imports related to a keyword"""
        lines = content.split('\n')
        import_count = 0
        
        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                if keyword in line.lower():
                    import_count += 1
        
        return import_count
    
    def analyze_recent_outputs(self):
        """Analyze recent output files to understand what's working"""
        output_analysis = {
            'recent_threads': [],
            'recent_images': [],
            'recent_reports': []
        }
        
        # Check thread files
        thread_files = glob.glob("smart_viral_thread_*.txt")
        thread_files.sort(key=os.path.getmtime, reverse=True)
        
        for file_path in thread_files[:3]:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                thread_info = {
                    'file': file_path,
                    'content_length': len(content),
                    'has_affiliate_link': 'wealthyrobot-20' in content,
                    'has_amazon_link': 'amazon.com' in content,
                    'created': os.path.getmtime(file_path)
                }
                output_analysis['recent_threads'].append(thread_info)
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        
        # Check image files
        image_files = glob.glob("*.png") + glob.glob("*.jpg")
        image_files.sort(key=os.path.getmtime, reverse=True)
        
        for file_path in image_files[:5]:
            image_info = {
                'file': file_path,
                'size': os.path.getsize(file_path),
                'created': os.path.getmtime(file_path)
            }
            output_analysis['recent_images'].append(image_info)
        
        return output_analysis
    
    def identify_integration_issues(self):
        """Identify why affiliate links aren't appearing in content"""
        issues = []
        
        # Check if affiliate agents exist but aren't being used
        affiliate_agents = self.analysis_report['affiliate_systems']
        content_agents = self.analysis_report['content_systems']
        
        if affiliate_agents and content_agents:
            # Both exist - check if they're connected
            orchestrator_info = self.check_orchestrator_integration()
            if orchestrator_info.get('imports_affiliate_agents', 0) == 0:
                issues.append("Affiliate agents exist but orchestrator doesn't import them")
            
            # Check if content agents call affiliate functions
            content_calls_affiliate = False
            for agent in content_agents:
                try:
                    with open(agent['file'], 'r') as f:
                        content = f.read()
                    if 'affiliate' in content.lower():
                        content_calls_affiliate = True
                        break
                except:
                    pass
            
            if not content_calls_affiliate:
                issues.append("Content agents don't call affiliate functions")
        
        elif not affiliate_agents:
            issues.append("No affiliate agents found")
        elif not content_agents:
            issues.append("No content agents found")
        
        # Check config integration
        config_analysis = self.analysis_report['config_analysis']
        if not config_analysis.get('has_affiliate_config', False):
            issues.append("live_config.json missing affiliate configuration")
        
        return issues
    
    def generate_recommendations(self):
        """Generate specific recommendations based on analysis"""
        recommendations = []
        
        issues = self.analysis_report['issues_identified']
        
        if "Affiliate agents exist but orchestrator doesn't import them" in issues:
            recommendations.append("Add affiliate agent imports to live_orchestrator.py")
        
        if "Content agents don't call affiliate functions" in issues:
            recommendations.append("Modify content agents to call affiliate link functions")
        
        if "live_config.json missing affiliate configuration" in issues:
            recommendations.append("Add affiliate configuration to live_config.json")
        
        if "No affiliate agents found" in issues:
            recommendations.append("Create or activate existing affiliate agents")
        
        # Check if systems exist but aren't coordinated
        if self.analysis_report['affiliate_systems'] and self.analysis_report['content_systems']:
            recommendations.append("Focus on integrating existing systems rather than creating new ones")
        
        return recommendations
    
    def run_analysis(self):
        """Run complete system analysis"""
        print("🔍 Analyzing WealthyRobot system...")
        
        # Scan for different types of agents
        print("1. Scanning for affiliate agents...")
        self.analysis_report['affiliate_systems'] = self.scan_affiliate_agents()
        
        print("2. Scanning for content agents...")
        self.analysis_report['content_systems'] = self.scan_content_agents()
        
        print("3. Scanning for visual agents...")
        self.analysis_report['visual_systems'] = self.scan_visual_agents()
        
        print("4. Analyzing configuration...")
        self.analysis_report['config_analysis'] = self.analyze_live_config()
        
        print("5. Analyzing recent outputs...")
        self.analysis_report['recent_outputs'] = self.analyze_recent_outputs()
        
        print("6. Identifying integration issues...")
        self.analysis_report['issues_identified'] = self.identify_integration_issues()
        
        print("7. Generating recommendations...")
        self.analysis_report['recommendations'] = self.generate_recommendations()
        
        return self.analysis_report
    
    def print_analysis_report(self):
        """Print comprehensive analysis report"""
        print("\n" + "="*70)
        print("🏰 WEALTHYROBOT SYSTEM ANALYSIS REPORT")
        print("="*70)
        
        # Affiliate Systems
        print(f"\n💰 AFFILIATE SYSTEMS ({len(self.analysis_report['affiliate_systems'])} found):")
        for agent in self.analysis_report['affiliate_systems']:
            print(f"   • {agent['file']}")
            print(f"     Amazon: {'✅' if agent['has_amazon'] else '❌'}")
            print(f"     WealthyRobot Tag: {'✅' if agent['has_wealthyrobot_tag'] else '❌'}")
            print(f"     Affiliate Logic: {'✅' if agent['has_affiliate_logic'] else '❌'}")
        
        # Content Systems
        print(f"\n📝 CONTENT SYSTEMS ({len(self.analysis_report['content_systems'])} found):")
        for agent in self.analysis_report['content_systems']:
            print(f"   • {agent['file']}")
            print(f"     Generates Content: {'✅' if agent['generates_content'] else '❌'}")
            print(f"     Twitter Integration: {'✅' if agent['has_twitter'] else '❌'}")
            print(f"     Posting Logic: {'✅' if agent['has_posting'] else '❌'}")
        
        # Visual Systems
        print(f"\n🖼️ VISUAL SYSTEMS ({len(self.analysis_report['visual_systems'])} found):")
        for agent in self.analysis_report['visual_systems']:
            print(f"   • {agent['file']}")
            print(f"     Creates Images: {'✅' if agent['creates_images'] else '❌'}")
        
        # Configuration
        print(f"\n⚙️ CONFIGURATION:")
        config = self.analysis_report['config_analysis']
        print(f"   live_config.json: {'✅' if config['file_exists'] else '❌'}")
        if config['file_exists']:
            print(f"   Affiliate Config: {'✅' if config.get('has_affiliate_config') else '❌'}")
            print(f"   Content Config: {'✅' if config.get('has_content_config') else '❌'}")
        
        # Recent Outputs
        print(f"\n📊 RECENT OUTPUTS:")
        outputs = self.analysis_report['recent_outputs']
        print(f"   Recent Threads: {len(outputs['recent_threads'])}")
        for thread in outputs['recent_threads']:
            print(f"     • {thread['file']}")
            print(f"       Affiliate Links: {'✅' if thread['has_affiliate_link'] else '❌'}")
        
        # Issues
        print(f"\n❌ ISSUES IDENTIFIED ({len(self.analysis_report['issues_identified'])}):")
        for issue in self.analysis_report['issues_identified']:
            print(f"   • {issue}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in self.analysis_report['recommendations']:
            print(f"   • {rec}")
        
        print("\n" + "="*70)

def main():
    analyzer = SystemAnalyzer()
    
    print("🚀 Starting WealthyRobot System Analysis...")
    
    # Run analysis
    analyzer.run_analysis()
    
    # Print report
    analyzer.print_analysis_report()
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"system_analysis_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(analyzer.analysis_report, f, indent=2)
        print(f"\n📊 Detailed analysis saved to: {filename}")
    except Exception as e:
        print(f"\n❌ Could not save analysis: {e}")

if __name__ == "__main__":
    main()
