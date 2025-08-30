import time
#!/usr/bin/env python3
"""
Twitter Agent Audit - Find API freeze causes
"""
import os
import re
import json

def audit_twitter_agents():
    print("🔍 TWITTER AGENT AUDIT REPORT")
    print("=" * 50)
    
    issues_found = []
    agents_checked = 0
    
    # Find all Python files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    # Check if it's a Twitter-related agent
                    if any(term in content.lower() for term in ['twitter', 'tweet', 'social', 'post']):
                        agents_checked += 1
                        print(f"\n📂 Checking: {filepath}")
                        
                        # Issue 1: No rate limit handling
                        if 'rate' not in content.lower() and 'sleep' not in content.lower():
                            issues_found.append(f"❌ {file}: No rate limit handling")
                        
                        # Issue 2: No 429 error handling
                        if '429' not in content and 'too many requests' not in content.lower():
                            issues_found.append(f"❌ {file}: No 429 error handling")
                        
                        # Issue 3: Rapid posting patterns
                        if 'time.sleep' not in content and 'delay' not in content.lower():
                            issues_found.append(f"❌ {file}: No posting delays")
                        
                        # Issue 4: No API key management
                        if 'bearer' in content.lower() and 'rotation' not in content.lower():
                            issues_found.append(f"⚠️ {file}: Single API key (no rotation)")
                        
                        # Issue 5: High frequency posting
                        post_patterns = re.findall(r'post.*(\d+)', content)
                        for pattern in post_patterns:
                            if int(pattern) > 10:  # More than 10 posts
                                issues_found.append(f"❌ {file}: High frequency posting detected")
                        
                        # Show positive findings
                        if 'sleep' in content.lower():
                            print(f"  ✅ Has sleep/delay mechanisms")
                        if '429' in content:
                            print(f"  ✅ Has 429 error handling")
                        if 'rate' in content.lower():
                            print(f"  ✅ Has rate limit awareness")
                
                except Exception as e:
                    pass
    
    print(f"\n📊 AUDIT SUMMARY:")
    print(f"  Agents checked: {agents_checked}")
    print(f"  Issues found: {len(issues_found)}")
    
    if issues_found:
        print(f"\n🚨 CRITICAL ISSUES CAUSING API FREEZES:")
        for issue in issues_found:
            print(f"  {issue}")
    else:
        print(f"\n✅ No obvious issues found in agent code")
    
    return issues_found

def show_twitter_limits():
    print(f"\n📋 CURRENT TWITTER API LIMITS (2025):")
    print(f"  • Posting: 300 tweets per 3 hours MAX")
    print(f"  • Free tier: 1,500 tweets per month")
    print(f"  • Per user: 100 tweets per 24 hours")
    print(f"  • 15-minute windows for requests")
    print(f"  • HTTP 429 when exceeded")

if __name__ == "__main__":
    issues = audit_twitter_agents()
    show_twitter_limits()
    
    if issues:
        print(f"\n🔧 RECOMMENDED FIXES:")
        print(f"  1. Add exponential backoff for API calls")
        print(f"  2. Implement 429 error handling")
        print(f"  3. Add delays between posts (minimum 10 seconds)")
        print(f"  4. Monitor rate limit headers")
        print(f"  5. Use multiple API keys with rotation")
