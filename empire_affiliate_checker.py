#!/usr/bin/env python3
"""
Check WealthyRobot Empire for Real Affiliate Tracking Implementation
"""

import os
import json
import glob
from datetime import datetime

def check_affiliate_tracking():
    print("🔍 CHECKING WEALTHYROBOT AFFILIATE TRACKING SYSTEM")
    print("=" * 60)
    
    tracking_found = {
        'revenue_files': [],
        'tracking_agents': [],
        'config_settings': {},
        'real_data_integration': False,
        'simulation_vs_real': 'unknown'
    }
    
    # 1. Check for revenue tracking files
    print("\n📊 REVENUE TRACKING FILES:")
    revenue_patterns = [
        '*revenue*',
        '*affiliate*', 
        '*tracking*',
        '*amazon*',
        '*performance*',
        '*earnings*',
        '*commission*'
    ]
    
    for pattern in revenue_patterns:
        files = glob.glob(pattern + '.json') + glob.glob(pattern + '.py') + glob.glob(pattern + '.log')
        if files:
            tracking_found['revenue_files'].extend(files)
            print(f"✅ Found: {files}")
    
    if not tracking_found['revenue_files']:
        print("❌ No revenue tracking files found")
    
    # 2. Check specific tracking agents
    print("\n🤖 AFFILIATE TRACKING AGENTS:")
    tracking_agents = [
        'real_revenue_tracker.py',
        'revenue_tracker.py', 
        'affiliate_tracker.py',
        'conversion_tracker_agent.py',
        'click_tracker.py',
        'real_money_agent.py'
    ]
    
    for agent in tracking_agents:
        if os.path.exists(agent):
            tracking_found['tracking_agents'].append(agent)
            print(f"✅ Found: {agent}")
            
            # Check if it's using real vs simulated data
            try:
                with open(agent, 'r') as f:
                    content = f.read()
                    if 'simulation' in content.lower() or 'fake' in content.lower():
                        print(f"   ⚠️  Contains simulation code")
                    elif 'amazon' in content.lower() and 'api' in content.lower():
                        print(f"   ✅ Appears to use real Amazon API")
                    else:
                        print(f"   ❓ Uncertain if real or simulated")
            except:
                print(f"   ❌ Could not read file")
        else:
            print(f"❌ Missing: {agent}")
    
    # 3. Check live config for revenue settings
    print("\n⚙️ LIVE CONFIG REVENUE SETTINGS:")
    if os.path.exists('live_config.json'):
        try:
            with open('live_config.json', 'r') as f:
                config = json.load(f)
                
            revenue_settings = {}
            
            # Look for revenue-related settings
            for key, value in config.items():
                if any(word in key.lower() for word in ['revenue', 'affiliate', 'amazon', 'tracking']):
                    revenue_settings[key] = value
            
            if revenue_settings:
                tracking_found['config_settings'] = revenue_settings
                print("✅ Revenue settings found:")
                for key, value in revenue_settings.items():
                    print(f"   {key}: {value}")
            else:
                print("❌ No revenue settings in live_config.json")
                
        except Exception as e:
            print(f"❌ Could not read live_config.json: {e}")
    else:
        print("❌ live_config.json not found")
    
    # 4. Check CEO and orchestrator for revenue logic
    print("\n👑 CEO & ORCHESTRATOR REVENUE LOGIC:")
    files_to_check = [
        'ultimate_ceo_agent.py',
        'live_orchestrator.py',
        'ceo_strategic_report.json',
        'ultimate_ceo_report.json'
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            try:
                if file.endswith('.json'):
                    with open(file, 'r') as f:
                        content = json.load(f)
                    content_str = json.dumps(content, indent=2)
                else:
                    with open(file, 'r') as f:
                        content_str = f.read()
                
                # Check for revenue references
                if 'revenue' in content_str.lower():
                    print(f"✅ {file} contains revenue logic")
                    
                    # Check if it's real or simulated
                    if any(word in content_str.lower() for word in ['simulation', 'fake', 'mock', 'test']):
                        print(f"   ⚠️  Contains simulation/test revenue")
                    elif any(word in content_str.lower() for word in ['amazon', 'api', 'real', 'actual']):
                        print(f"   ✅ May use real revenue data")
                    else:
                        print(f"   ❓ Revenue source unclear")
                        
                    # Show revenue amount if found
                    import re
                    amounts = re.findall(r'\$[\d,]+', content_str)
                    if amounts:
                        print(f"   💰 Revenue amounts found: {amounts[:3]}")  # First 3
                else:
                    print(f"❌ {file} - no revenue logic found")
                    
            except Exception as e:
                print(f"❌ Could not read {file}: {e}")
        else:
            print(f"❌ Missing: {file}")
    
    # 5. Check for Amazon Associates integration
    print("\n🛒 AMAZON ASSOCIATES INTEGRATION:")
    amazon_indicators = [
        'wealthyrobot-20',  # Your affiliate tag
        'amazon.com',
        'amzn.to',
        'associates',
        'affiliate_tag'
    ]
    
    amazon_files = []
    for file in glob.glob('*.py') + glob.glob('*.json'):
        try:
            with open(file, 'r') as f:
                content = f.read()
            
            for indicator in amazon_indicators:
                if indicator in content.lower():
                    amazon_files.append(f"{file} (contains: {indicator})")
                    break
        except:
            continue
    
    if amazon_files:
        print("✅ Amazon integration found in:")
        for file in amazon_files[:5]:  # First 5
            print(f"   {file}")
    else:
        print("❌ No Amazon Associates integration found")
    
    # 6. Generate summary report
    print("\n" + "="*60)
    print("📋 AFFILIATE TRACKING SUMMARY:")
    print("="*60)
    
    if tracking_found['revenue_files']:
        print(f"✅ Revenue tracking files: {len(tracking_found['revenue_files'])}")
    else:
        print("❌ No revenue tracking files")
    
    if tracking_found['tracking_agents']:
        print(f"✅ Tracking agents: {len(tracking_found['tracking_agents'])}")
    else:
        print("❌ No tracking agents found")
    
    if tracking_found['config_settings']:
        print("✅ Revenue config settings found")
    else:
        print("❌ No revenue config settings")
    
    if amazon_files:
        print("✅ Amazon integration detected")
    else:
        print("❌ No Amazon integration found")
    
    # 7. Generate recommendation
    print("\n🎯 RECOMMENDATION:")
    
    if not tracking_found['revenue_files'] and not tracking_found['tracking_agents']:
        print("🚨 NO REAL TRACKING DETECTED")
        print("   System appears to be using simulated revenue")
        print("   URGENT: Implement real Amazon Associates tracking")
        
    elif tracking_found['tracking_agents'] and amazon_files:
        print("✅ TRACKING SYSTEM EXISTS")
        print("   Need to verify if using real vs simulated data")
        print("   Check agent code to confirm Amazon API integration")
        
    else:
        print("⚠️ PARTIAL TRACKING DETECTED")
        print("   Some tracking elements found but incomplete")
        print("   Review files above to determine real vs simulated")
    
    return tracking_found

if __name__ == "__main__":
    results = check_affiliate_tracking()
    
    print(f"\n📊 NEXT STEPS:")
    print("1. Review files listed above")
    print("2. Verify real vs simulated revenue data")
    print("3. Implement Amazon Associates API if missing")
    print("4. Update CEO agent to use real metrics")
