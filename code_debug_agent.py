import subprocess
import os
import time
from datetime import datetime

class CodeDebugAgent:
    def __init__(self):
        print("🔧 CODE DEBUG AGENT - INITIALIZING...")
        print("🎯 Automatically debugging and fixing empire code!")
        
        self.debug_active = True
        self.debug_count = 0
        
    def run_continuous_debugging(self):
        """Continuously debug empire code"""
        print("🔧 STARTING CONTINUOUS DEBUGGING...")
        
        while self.debug_active:
            try:
                self.debug_count += 1
                
                print(f"\n🔧 DEBUG CYCLE #{self.debug_count}")
                print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 35)
                
                # 1. Check for Python syntax errors
                self.check_syntax_errors()
                
                # 2. Check for missing dependencies
                self.check_dependencies()
                
                # 3. Check for runtime errors in logs
                self.check_runtime_errors()
                
                # 4. Auto-fix common issues
                self.auto_fix_common_issues()
                
                # 5. Validate empire health
                self.validate_empire_health()
                
                print("⏰ Next debug cycle in 10 minutes...")
                time.sleep(600)  # 10 minutes
                
            except KeyboardInterrupt:
                print("🛑 Code Debug Agent stopping...")
                break
            except Exception as e:
                print(f"⚠️ Debug agent error: {e}")
                time.sleep(300)
    
    def check_syntax_errors(self):
        """Check all Python files for syntax errors"""
        print("📝 Checking Python syntax...")
        
        python_files = [f for f in os.listdir('.') if f.endswith('.py')]
        syntax_errors = []
        
        for file in python_files:
            try:
                result = subprocess.run(['python3', '-m', 'py_compile', file],
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    syntax_errors.append((file, result.stderr))
            except:
                pass
        
        if syntax_errors:
            print(f"⚠️ Found {len(syntax_errors)} syntax errors")
            for file, error in syntax_errors[:3]:  # Show first 3
                print(f"   🔧 {file}: {error.split(':')[-1].strip()}")
        else:
            print("✅ No syntax errors found")
    
    def check_dependencies(self):
        """Check for missing dependencies"""
        print("📦 Checking dependencies...")
        
        required_modules = ['openai', 'tweepy', 'dotenv', 'json', 'datetime']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module.replace('-', '_'))
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"⚠️ Missing modules: {missing_modules}")
            # Could auto-install here
        else:
            print("✅ All dependencies available")
    
    def check_runtime_errors(self):
        """Check log files for runtime errors"""
        print("📋 Checking runtime errors...")
        
        log_files = [f for f in os.listdir('.') if f.endswith('.log')]
        error_count = 0
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    content = f.read()
                    if 'Error' in content or 'Exception' in content:
                        error_count += 1
            except:
                pass
        
        if error_count > 0:
            print(f"⚠️ Found errors in {error_count} log files")
        else:
            print("✅ No runtime errors detected")
    
    def auto_fix_common_issues(self):
        """Auto-fix common empire issues"""
        print("🔧 Auto-fixing common issues...")
        
        fixes_applied = []
        
        # Fix 1: Restart stopped critical processes
        critical_processes = [
            'autonomous_operations_manager',
            'strategic_advisor_agent',
            'lightweight_ceo_budget_controller'
        ]
        
        for process in critical_processes:
            try:
                result = subprocess.run(['pgrep', '-f', process],
                                      capture_output=True, text=True)
                if not result.stdout.strip():
                    # Process not running, restart it
                    subprocess.Popen(['python3', f'{process}.py'],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    fixes_applied.append(f"Restarted {process}")
            except:
                pass
        
        # Fix 2: Clean up temporary files
        temp_files = [f for f in os.listdir('.') if f.endswith('.tmp') or f.endswith('.pyc')]
        if temp_files:
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                    fixes_applied.append(f"Removed {temp_file}")
                except:
                    pass
        
        if fixes_applied:
            print(f"✅ Applied {len(fixes_applied)} fixes")
        else:
            print("✅ No fixes needed")
    
    def validate_empire_health(self):
        """Validate overall empire health"""
        print("🏥 Validating empire health...")
        
        health_checks = {
            'twitter_connection': self.check_twitter_health(),
            'content_generation': self.check_content_health(),
            'process_health': self.check_process_health()
        }
        
        healthy_components = sum(health_checks.values())
        total_components = len(health_checks)
        
        health_percentage = (healthy_components / total_components) * 100
        
        print(f"🏥 Empire Health: {health_percentage:.0f}% ({healthy_components}/{total_components})")
        
        return health_percentage >= 80
    
    def check_twitter_health(self):
        """Check Twitter API health"""
        try:
            from twitter_posting_agent import TwitterPostingAgent
            agent = TwitterPostingAgent()
            return agent.client is not None
        except:
            return False
    
    def check_content_health(self):
        """Check content generation health"""
        content_files = [f for f in os.listdir('.') if f.startswith('smart_viral_thread_')]
        return len(content_files) > 0
    
    def check_process_health(self):
        """Check critical process health"""
        critical_processes = ['autonomous_operations_manager', 'strategic_advisor_agent']
        running_count = 0
        
        for process in critical_processes:
            try:
                result = subprocess.run(['pgrep', '-f', process],
                                      capture_output=True, text=True)
                if result.stdout.strip():
                    running_count += 1
            except:
                pass
        
        return running_count >= 1

if __name__ == "__main__":
    debug_agent = CodeDebugAgent()
    
    print("\n🔧 CODE DEBUG AGENT ARCHITECTURE:")
    print("=" * 40)
    print("📝 Syntax error detection")
    print("📦 Dependency checking")
    print("📋 Runtime error monitoring")
    print("🔧 Auto-fix common issues")
    print("🏥 Empire health validation")
    
    debug_agent.run_continuous_debugging()
