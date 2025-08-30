#!/usr/bin/env python3
"""
WealthyRobot Integration Fixer
Connects existing affiliate agents to the orchestrator and content pipeline
"""

import os
import json
import shutil
from datetime import datetime

class IntegrationFixer:
    def __init__(self):
        self.fixes_applied = []
        self.backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def backup_critical_files(self):
        """Backup critical files before modifications"""
        os.makedirs(self.backup_dir, exist_ok=True)
        
        critical_files = [
            'live_orchestrator.py',
            'live_config.json',
            'dynamic_content_selector.py',
            'social_media_agent.py'
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                shutil.copy2(file_path, self.backup_dir)
                print(f"✅ Backed up {file_path}")
        
        return self.backup_dir
    
    def fix_live_config(self):
        """Add affiliate configuration to live_config.json"""
        try:
            with open('live_config.json', 'r') as f:
                config = json.load(f)
            
            # Add affiliate configuration
            config['affiliate'] = {
                "enabled": True,
                "tag": "wealthyrobot-20",
                "product_url": "https://www.amazon.com/dp/B0C7GWQRFP?tag=wealthyrobot-20",
                "product_name": "The AI Advantage",
                "commission_rate": 0.08,
                "frequency": 0.2,
                "cta_templates": [
                    "📚 Master AI in business with '{product_name}': {product_url}",
                    "🚀 Ready to leverage AI? Start with '{product_name}': {product_url}",
                    "💡 Want to implement these strategies? '{product_name}' shows you how: {product_url}",
                    "🎯 Turn AI knowledge into business results with '{product_name}': {product_url}"
                ]
            }
            
            # Ensure content strategy includes affiliate integration
            if 'content_strategy' not in config:
                config['content_strategy'] = {}
            
            config['content_strategy']['affiliate_integration'] = True
            config['content_strategy']['value_to_affiliate_ratio'] = 0.8  # 80% value, 20% affiliate
            
            # Write back
            with open('live_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            return "Added affiliate configuration to live_config.json"
            
        except Exception as e:
            return f"Error fixing live_config.json: {e}"
    
    def fix_orchestrator_imports(self):
        """Add affiliate agent imports to live_orchestrator.py"""
        try:
            with open('live_orchestrator.py', 'r') as f:
                content = f.read()
            
            # Check if affiliate imports already exist
            if 'smart_affiliate_agent' in content and 'dynamic_content_selector' in content:
                return "Affiliate imports already exist in orchestrator"
            
            # Find import section
            lines = content.split('\n')
            import_section_end = 0
            
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_section_end = i
            
            # Add affiliate imports
            new_imports = [
                "from smart_affiliate_agent import SmartAffiliateAgent",
                "from dynamic_content_selector import DynamicContentSelector", 
                "from visual_affiliate_agent import VisualAffiliateAgent"
            ]
            
            for import_line in reversed(new_imports):
                if import_line not in content:
                    lines.insert(import_section_end + 1, import_line)
            
            # Find orchestrator class and add affiliate integration
            class_found = False
            for i, line in enumerate(lines):
                if 'class ' in line and 'Orchestrator' in line:
                    class_found = True
                    # Look for __init__ method
                    for j in range(i, min(i + 50, len(lines))):
                        if 'def __init__' in lines[j]:
                            # Add affiliate agent initialization
                            init_end = j
                            for k in range(j, min(j + 20, len(lines))):
                                if lines[k].strip().startswith('self.') and '=' in lines[k]:
                                    init_end = k
                            
                            affiliate_init = [
                                "        # Initialize affiliate agents",
                                "        self.smart_affiliate = SmartAffiliateAgent()",
                                "        self.content_selector = DynamicContentSelector()",
                                "        self.visual_affiliate = VisualAffiliateAgent()"
                            ]
                            
                            for init_line in reversed(affiliate_init):
                                lines.insert(init_end + 1, init_line)
                            break
                    break
            
            if not class_found:
                return "Could not find Orchestrator class to modify"
            
            # Write back
            with open('live_orchestrator.py', 'w') as f:
                f.write('\n'.join(lines))
            
            return "Added affiliate agent imports and initialization to live_orchestrator.py"
            
        except Exception as e:
            return f"Error fixing orchestrator: {e}"
    
    def fix_content_agent_integration(self):
        """Ensure social_media_agent calls affiliate functions"""
        try:
            with open('social_media_agent.py', 'r') as f:
                content = f.read()
            
            # Check if affiliate integration already exists
            if 'wealthyrobot-20' in content and 'affiliate' in content.lower():
                return "social_media_agent.py already has affiliate integration"
            
            # Look for content generation function
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                # Find where content is being returned or posted
                if 'return ' in line and ('content' in line or 'thread' in line or 'post' in line):
                    # Insert affiliate link addition before return
                    affiliate_code = [
                        "",
                        "        # Add affiliate link strategically",
                        "        if hasattr(self, 'config') and self.config.get('affiliate', {}).get('enabled', False):",
                        "            import random",
                        "            affiliate_config = self.config['affiliate']",
                        "            if random.random() < affiliate_config.get('frequency', 0.2):  # 20% chance",
                        "                cta_template = random.choice(affiliate_config['cta_templates'])",
                        "                cta = cta_template.format(",
                        "                    product_name=affiliate_config['product_name'],",
                        "                    product_url=affiliate_config['product_url']",
                        "                )",
                        "                content = content + '\\n\\n' + cta",
                        ""
                    ]
                    
                    for code_line in reversed(affiliate_code):
                        lines.insert(i, code_line)
                    break
            
            # Write back
            with open('social_media_agent.py', 'w') as f:
                f.write('\n'.join(lines))
            
            return "Added affiliate integration to social_media_agent.py"
            
        except Exception as e:
            return f"Error fixing social_media_agent.py: {e}"
    
    def fix_dynamic_content_selector(self):
        """Ensure dynamic_content_selector properly handles affiliate content"""
        try:
            with open('dynamic_content_selector.py', 'r') as f:
                content = f.read()
            
            # Check if it already has proper affiliate handling
            if 'wealthyrobot-20' in content and 'affiliate_link' in content:
                return "dynamic_content_selector.py already has affiliate link handling"
            
            # Add affiliate link function if missing
            affiliate_function = '''
def add_affiliate_link_to_content(content, content_type="value"):
    """Add affiliate link to content based on type and strategy"""
    import json
    import random
    
    try:
        with open('live_config.json', 'r') as f:
            config = json.load(f)
        
        affiliate_config = config.get('affiliate', {})
        if not affiliate_config.get('enabled', False):
            return content
        
        # Only add affiliate links to designated affiliate content (20% of posts)
        if content_type == "affiliate" or random.random() < affiliate_config.get('frequency', 0.2):
            cta_template = random.choice(affiliate_config.get('cta_templates', [
                "📚 Master AI with '{product_name}': {product_url}"
            ]))
            
            cta = cta_template.format(
                product_name=affiliate_config.get('product_name', 'The AI Advantage'),
                product_url=affiliate_config.get('product_url', 'https://www.amazon.com/dp/B0C7GWQRFP?tag=wealthyrobot-20')
            )
            
            content = content + '\\n\\n' + cta + '\\n\\n#AI #Business #WealthyRobot'
        
        return content
        
    except Exception as e:
        print(f"Error adding affiliate link: {e}")
        return content

'''
            
            # Insert the function at the beginning of the file
            lines = content.split('\n')
            
            # Find a good place to insert (after imports)
            insert_index = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('class ') or line.strip().startswith('def '):
                    insert_index = i
                    break
            
            # Insert the function
            function_lines = affiliate_function.strip().split('\n')
            for line in reversed(function_lines):
                lines.insert(insert_index, line)
            
            # Write back
            with open('dynamic_content_selector.py', 'w') as f:
                f.write('\n'.join(lines))
            
            return "Added affiliate link function to dynamic_content_selector.py"
            
        except Exception as e:
            return f"Error fixing dynamic_content_selector.py: {e}"
    
    def run_integration_fixes(self):
        """Run all integration fixes"""
        print("🔧 Starting WealthyRobot Integration Fix...")
        
        # Backup critical files
        print("\n1. Creating backup...")
        backup_dir = self.backup_critical_files()
        self.fixes_applied.append(f"Created backup in {backup_dir}")
        
        # Fix live_config.json
        print("\n2. Fixing live_config.json...")
        config_result = self.fix_live_config()
        print(f"   {config_result}")
        self.fixes_applied.append(config_result)
        
        # Fix orchestrator
        print("\n3. Fixing live_orchestrator.py...")
        orchestrator_result = self.fix_orchestrator_imports()
        print(f"   {orchestrator_result}")
        self.fixes_applied.append(orchestrator_result)
        
        # Fix social media agent
        print("\n4. Fixing social_media_agent.py...")
        social_result = self.fix_content_agent_integration()
        print(f"   {social_result}")
        self.fixes_applied.append(social_result)
        
        # Fix dynamic content selector
        print("\n5. Fixing dynamic_content_selector.py...")
        selector_result = self.fix_dynamic_content_selector()
        print(f"   {selector_result}")
        self.fixes_applied.append(selector_result)
        
        print(f"\n✅ Integration fixes complete!")
        
        return self.fixes_applied
    
    def print_fix_summary(self):
        """Print summary of fixes applied"""
        print("\n" + "="*60)
        print("🔗 WEALTHYROBOT INTEGRATION FIX SUMMARY")
        print("="*60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Fixes Applied: {len(self.fixes_applied)}")
        
        for i, fix in enumerate(self.fixes_applied, 1):
            print(f"   {i}. {fix}")
        
        print("\n🚀 NEXT STEPS:")
        print("   1. Restart live_orchestrator.py")
        print("   2. Run twitter_verifier.py to confirm affiliate links")
        print("   3. Monitor next few posts for affiliate integration")
        print("   4. Backup files saved in:", self.backup_dir)
        
        print("\n💡 WHAT WAS FIXED:")
        print("   • Added affiliate config to live_config.json")
        print("   • Connected affiliate agents to orchestrator")
        print("   • Integrated affiliate links into content pipeline")
        print("   • Maintained 80/20 value-to-affiliate ratio")
        
        print("\n" + "="*60)

def main():
    fixer = IntegrationFixer()
    
    print("🚀 WealthyRobot Integration Fixer")
    print("="*50)
    print("This will connect your existing affiliate agents to the content pipeline.")
    
    response = input("\nProceed with integration fixes? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        fixer.run_integration_fixes()
        fixer.print_fix_summary()
    else:
        print("Integration fixes cancelled.")

if __name__ == "__main__":
    main()
