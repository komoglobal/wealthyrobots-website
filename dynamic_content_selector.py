#!/usr/bin/env python3
"""
Dynamic Content Selector - Intelligently chooses content type based on:
- Time of day
- Performance metrics  
- CEO optimization decisions
- Conversion data
"""

import json
import os
import random
import glob
from datetime import datetime, timedelta

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
            
            content = content + '\n\n' + cta + '\n\n#AI #Business #WealthyRobot'
        
        return content
        
    except Exception as e:
        print(f"Error adding affiliate link: {e}")
        return content
class DynamicContentSelector:
    def __init__(self):
        self.load_config()
        self.performance_data = self.load_performance_data()
        
    def load_config(self):
        """Load dynamic content strategy config"""
        try:
            with open('live_config.json', 'r') as f:
                config = json.load(f)
                self.strategy = config.get('content_strategy', {})
                return True
        except:
            print("❌ Could not load content strategy config")
            return False
            
    def load_performance_data(self):
        """Load recent performance metrics"""
        try:
            # Look for performance data files
            perf_files = glob.glob('*performance*.json') + glob.glob('*analytics*.json')
            if perf_files:
                latest = max(perf_files, key=lambda x: os.path.getctime(x))
                with open(latest, 'r') as f:
                    return json.load(f)
            return {}
        except:
            return {}
            
    def get_current_content_type(self):
        """Determine content type based on time and strategy"""
        current_hour = datetime.now().hour
        schedule = self.strategy.get('daily_schedule', {})
        
        # Find closest scheduled time
        closest_time = "21:00"  # Default to evening
        min_diff = 24
        
        for time_slot in schedule.keys():
            hour = int(time_slot.split(':')[0])
            diff = abs(current_hour - hour)
            if diff < min_diff:
                min_diff = diff
                closest_time = time_slot
                
        return schedule.get(closest_time, {}).get('type', 'educational')
        
    def should_use_affiliate_content(self):
        """Intelligent decision on affiliate vs value content"""
        content_type = self.get_current_content_type()
        schedule = self.strategy.get('daily_schedule', {})
        
        # Get probability for current time slot
        current_schedule = None
        current_hour = datetime.now().hour
        
        for time_slot, config in schedule.items():
            hour = int(time_slot.split(':')[0])
            if abs(current_hour - hour) <= 1:  # Within 1 hour
                current_schedule = config
                break
                
        if not current_schedule:
            return False
            
        base_probability = current_schedule.get('probability_affiliate', 0.2)
        
        # CEO optimization adjustments
        if self.strategy.get('ceo_optimization', {}).get('enabled'):
            # Check recent performance
            engagement_rate = self.get_recent_engagement_rate()
            conversion_rate = self.get_recent_conversion_rate()
            
            targets = self.strategy['ceo_optimization']['performance_targets']
            
            # Adjust probability based on performance
            if engagement_rate < targets.get('min_engagement_rate', 2.0):
                base_probability *= 0.5  # Reduce affiliate if engagement low
            elif conversion_rate > targets.get('target_conversion_rate', 1.0):
                base_probability *= 1.2  # Increase if converting well
                
        return random.random() < base_probability
        
    def get_recent_engagement_rate(self):
        """Calculate recent engagement rate"""
        # Simplified - would integrate with real analytics
        return self.performance_data.get('avg_engagement_rate', 1.5)
        
    def get_recent_conversion_rate(self):
        """Calculate recent conversion rate"""
        # Simplified - would integrate with affiliate tracking
        return self.performance_data.get('conversion_rate', 0.0)
        
    def select_content_file(self):
        """Select appropriate content file"""
        if self.should_use_affiliate_content():
            # Use affiliate content
            affiliate_files = []
            for file in glob.glob("smart_viral_thread*.txt"):
                try:
                    with open(file, 'r') as f:
                        if 'amazon.com' in f.read() and 'wealthyrobot-20' in f.read():
                            affiliate_files.append(file)
                except:
                    continue
                    
            if affiliate_files:
                latest = max(affiliate_files, key=lambda x: os.path.getctime(x))
                print(f"📈 Selected affiliate content: {latest}")
                return latest
                
        # Use value content
        content_type = self.get_current_content_type()
        template_path = f"content_templates/{content_type}_template.txt"
        
        if os.path.exists(template_path):
            print(f"📚 Selected {content_type} content: {template_path}")
            return template_path
        else:
            print(f"⚠️ Template not found: {template_path}")
            return "content_templates/educational_template.txt"  # Fallback
            
    def log_content_decision(self, content_file, reasoning):
        """Log content selection for CEO analysis"""
        decision_log = {
            'timestamp': datetime.now().isoformat(),
            'content_file': content_file,
            'content_type': self.get_current_content_type(),
            'was_affiliate': 'affiliate' in content_file.lower() or 'smart_viral' in content_file,
            'reasoning': reasoning,
            'hour': datetime.now().hour,
            'engagement_rate': self.get_recent_engagement_rate(),
            'conversion_rate': self.get_recent_conversion_rate()
        }
        
        # Append to decision log
        try:
            with open('content_decisions.json', 'r') as f:
                decisions = json.load(f)
        except:
            decisions = []
            
        decisions.append(decision_log)
        
        # Keep only last 100 decisions
        decisions = decisions[-100:]
        
        with open('content_decisions.json', 'w') as f:
            json.dump(decisions, f, indent=2)
            
    def get_optimized_content(self):
        """Main method: Get optimized content selection"""
        content_file = self.select_content_file()
        
        reasoning = f"Time-based: {self.get_current_content_type()}, "
        reasoning += f"Affiliate probability: {self.should_use_affiliate_content()}"
        
        self.log_content_decision(content_file, reasoning)
        
        return content_file

if __name__ == "__main__":
    selector = DynamicContentSelector()
    content_file = selector.get_optimized_content()
    print(f"🎯 Selected content: {content_file}")
