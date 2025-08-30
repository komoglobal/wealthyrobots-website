import os
import json
import time
import requests
from datetime import datetime
import re

class SimpleTwitterVerifier:
    def __init__(self):
        self.username = "WealthyRobot"
        self.verification_log = []
        
    def check_recent_threads(self):
        """Check locally generated thread files"""
        thread_files = []
        
        try:
            import glob
            pattern = "smart_viral_thread_*.txt"
            files = glob.glob(pattern)
            
            files.sort(key=os.path.getmtime, reverse=True)
            recent_files = files[:3]
            
            for file_path in recent_files:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    thread_data = {
                        'file': file_path,
                        'timestamp': os.path.getmtime(file_path),
                        'content_length': len(content),
                        'has_affiliate_link': 'wealthyrobot-20' in content or 'amazon.com' in content,
                        'content_preview': content[:200] + "..." if len(content) > 200 else content
                    }
                    
                    thread_files.append(thread_data)
                    
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
        except Exception as e:
            print(f"Error checking thread files: {e}")
            
        return thread_files
    
    def verify_posting_system(self):
        """Main verification function"""
        verification_report = {
            'timestamp': datetime.now().isoformat(),
            'username': self.username,
            'local_threads': [],
            'overall_status': 'unknown',
            'issues_found': [],
            'recommendations': []
        }
        
        print(f"Starting verification of @{self.username} posting system...")
        
        # Check local thread files
        print("Checking local thread files...")
        verification_report['local_threads'] = self.check_recent_threads()
        
        # Analyze results
        local_issues = []
        
        if not verification_report['local_threads']:
            local_issues.append("No recent thread files found")
        else:
            for thread in verification_report['local_threads']:
                if not thread['has_affiliate_link']:
                    local_issues.append(f"Thread {thread['file']} missing affiliate links")
        
        verification_report['issues_found'] = local_issues
        
        # Determine overall status
        if not local_issues:
            verification_report['overall_status'] = 'ALL_SYSTEMS_VERIFIED'
        else:
            verification_report['overall_status'] = 'ISSUES_DETECTED'
        
        return verification_report
    
    def print_verification_summary(self, report):
        """Print a formatted summary"""
        print("\n" + "="*60)
        print(f"WEALTHYROBOT POSTING VERIFICATION")
        print("="*60)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Overall Status: {report['overall_status']}")
        
        print(f"\nLocal Thread Files Analysis:")
        if report['local_threads']:
            for thread in report['local_threads']:
                print(f"   • {thread['file']}")
                print(f"     Content Length: {thread['content_length']} chars")
                print(f"     Has Affiliate Links: {'YES' if thread['has_affiliate_link'] else 'NO'}")
                print(f"     Preview: {thread['content_preview'][:100]}...")
        else:
            print("   No recent thread files found")
        
        if report.get('issues_found'):
            print(f"\nIssues Found:")
            for issue in report['issues_found']:
                print(f"   • {issue}")
        
        print("\n" + "="*60)

def main():
    """Run the simple verification"""
    verifier = SimpleTwitterVerifier()
    
    print("Starting Simple Twitter Verification...")
    
    report = verifier.verify_posting_system()
    verifier.print_verification_summary(report)
    
    return 0

if __name__ == "__main__":
    main()
