#!/usr/bin/env python3
"""
WealthyRobot Fully Autonomous Service (Simplified)
Runs the entire empire automatically without any manual intervention
No external dependencies required
"""

import os
import sys
import time
import signal
import subprocess
import json
from datetime import datetime
import glob

class WealthyRobotAutonomousServiceSimple:
    def __init__(self):
        self.service_name = "WealthyRobot Autonomous Empire (Simple)"
        self.version = "1.0 - Fully Autonomous"
        self.running = True
        self.cycle_count = 0
        self.start_time = datetime.now()
        self.last_health_check = datetime.now()
        self.health_check_interval = 300  # 5 minutes
        
        # Signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self.graceful_shutdown)
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        
        print(f"🚀 {self.service_name} v{self.version}")
        print("🎯 FULLY AUTONOMOUS MODE - NO MANUAL INTERVENTION NEEDED")
        print("💡 Simplified version - no external dependencies")
        print("=" * 70)
        
    def graceful_shutdown(self, signum, frame):
        """Graceful shutdown on system signals"""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
        self.stop_all_processes()
        sys.exit(0)
    
    def stop_all_processes(self):
        """Stop all running empire processes"""
        print("🛑 Stopping all empire processes...")
        
        # Find and stop Python processes related to the empire
        try:
            # Use ps and grep to find processes
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'python3' in line and any(keyword in line for keyword in ['agent.py', 'orchestrator', 'claude']):
                        parts = line.split()
                        if len(parts) > 1:
                            pid = parts[1]
                            try:
                                os.kill(int(pid), signal.SIGTERM)
                                print(f"🛑 Stopped process {pid}")
                            except (ValueError, ProcessLookupError):
                                pass
        except Exception as e:
            print(f"⚠️ Process stopping error: {e}")
        
        print("✅ All processes stopped")
    
    def start_empire_orchestrator(self):
        """Start the main empire orchestrator"""
        try:
            print("🎮 Starting Empire Orchestrator...")
            # Start orchestrator in background
            subprocess.Popen([
                sys.executable, 'live_orchestrator.py'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ Empire Orchestrator started")
            return True
        except Exception as e:
            print(f"❌ Failed to start orchestrator: {e}")
            return False
    
    def start_claude_autonomous(self):
        """Start Claude's autonomous thinking process"""
        try:
            print("🧠 Starting Claude Autonomous Mode...")
            # Start Claude in background
            subprocess.Popen([
                sys.executable, 'claude_full_autonomous.py'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ Claude Autonomous Mode started")
            return True
        except Exception as e:
            print(f"❌ Failed to start Claude: {e}")
            return False
    
    def start_continuous_agents(self):
        """Start all continuous background agents"""
        continuous_agents = [
            'continuous_empire_optimizer.py',
            'continuous_automation_agent.py',
            'code_debug_agent.py',
            'strategic_advisor_agent.py'
        ]
        
        started_count = 0
        for agent in continuous_agents:
            if os.path.exists(agent):
                try:
                    print(f"🤖 Starting {agent}...")
                    subprocess.Popen([
                        sys.executable, agent
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    started_count += 1
                    time.sleep(1)  # Brief pause between starts
                except Exception as e:
                    print(f"❌ Failed to start {agent}: {e}")
        
        print(f"✅ Started {started_count} continuous agents")
        return started_count
    
    def check_empire_health(self):
        """Check overall empire health and restart if needed"""
        current_time = datetime.now()
        
        # Check if health check is due
        if (current_time - self.last_health_check).total_seconds() < self.health_check_interval:
            return True
        
        self.last_health_check = current_time
        print(f"\n🏥 EMPIRE HEALTH CHECK #{self.cycle_count}")
        print("-" * 40)
        
        # Check if key processes are running
        health_status = self.assess_process_health()
        
        if not health_status['healthy']:
            print("🚨 Health issues detected, restarting critical components...")
            self.restart_critical_components()
        
        return health_status['healthy']
    
    def assess_process_health(self):
        """Assess the health of running empire processes"""
        health_status = {
            'healthy': True,
            'issues': [],
            'processes_running': 0
        }
        
        # Check for Python processes running empire code
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                empire_processes = 0
                for line in lines:
                    if 'python3' in line and any(keyword in line for keyword in ['agent.py', 'orchestrator', 'claude']):
                        empire_processes += 1
                
                health_status['processes_running'] = empire_processes
                
                # Health thresholds
                if empire_processes < 3:  # Should have at least 3 processes running
                    health_status['healthy'] = False
                    health_status['issues'].append(f"Low process count: {empire_processes}")
        except Exception as e:
            health_status['issues'].append(f"Process check error: {e}")
            health_status['healthy'] = False
        
        # Check for recent content generation
        recent_content = len([f for f in os.listdir('.') if f.startswith('smart_viral_thread_') and 
                            (datetime.now() - datetime.fromtimestamp(os.path.getctime(f))).total_seconds() < 3600])
        
        if recent_content == 0:
            health_status['issues'].append("No recent content generation")
            health_status['healthy'] = False
        
        # Check for recent CEO reports
        if os.path.exists('ultimate_ceo_report.json'):
            try:
                with open('ultimate_ceo_report.json', 'r') as f:
                    ceo_data = json.load(f)
                    last_action = ceo_data.get('last_action_time', 'unknown')
                    if last_action != 'unknown':
                        # Check if CEO has been active recently
                        pass  # Add time-based validation if needed
            except:
                health_status['issues'].append("CEO report corrupted")
                health_status['healthy'] = False
        
        # Report health status
        print(f"🤖 Empire Processes: {health_status['processes_running']}")
        print(f"📝 Recent Content: {recent_content}")
        print(f"🏥 Health Status: {'✅ Healthy' if health_status['healthy'] else '❌ Issues Detected'}")
        
        if health_status['issues']:
            for issue in health_status['issues']:
                print(f"  ⚠️ {issue}")
        
        return health_status
    
    def restart_critical_components(self):
        """Restart critical components if health issues detected"""
        print("🔄 Restarting critical components...")
        
        # Stop existing processes
        self.stop_all_processes()
        time.sleep(5)  # Wait for processes to stop
        
        # Restart core components
        self.start_empire_orchestrator()
        time.sleep(3)
        self.start_claude_autonomous()
        time.sleep(3)
        self.start_continuous_agents()
        
        print("✅ Critical components restarted")
    
    def run_autonomous_service(self):
        """Main autonomous service loop"""
        print("🚀 Starting WealthyRobot Autonomous Service...")
        print("🎯 This service will run FOREVER without manual intervention")
        print("🔄 Press Ctrl+C to stop (but it will restart on system boot)")
        print("=" * 70)
        
        # Initial startup
        print("\n🚀 PHASE 1: Initial Empire Startup")
        print("-" * 35)
        
        if not self.start_empire_orchestrator():
            print("❌ Critical failure: Cannot start orchestrator")
            return False
        
        time.sleep(5)  # Wait for orchestrator to initialize
        
        if not self.start_claude_autonomous():
            print("❌ Critical failure: Cannot start Claude")
            return False
        
        time.sleep(3)  # Wait for Claude to initialize
        
        self.start_continuous_agents()
        
        print("\n✅ Initial startup complete!")
        print("🔄 Entering continuous autonomous operation...")
        
        # Main service loop
        while self.running:
            try:
                self.cycle_count += 1
                current_time = datetime.now()
                uptime = current_time - self.start_time
                
                print(f"\n🔄 AUTONOMOUS SERVICE CYCLE #{self.cycle_count}")
                print(f"⏰ {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"⏱️ Uptime: {str(uptime).split('.')[0]}")
                print("-" * 50)
                
                # Health check
                if not self.check_empire_health():
                    print("🚨 Health check failed, attempting recovery...")
                    self.restart_critical_components()
                
                # Service status report
                self.generate_service_report()
                
                # Wait for next cycle
                print(f"⏳ Next service cycle in 10 minutes...")
                print("💡 Empire continues operating autonomously...")
                
                # Sleep for 10 minutes, but check for shutdown signals
                for _ in range(600):  # 600 seconds = 10 minutes
                    if not self.running:
                        break
                    time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n🛑 Service interrupted by user")
                break
            except Exception as e:
                print(f"⚠️ Service error: {e}")
                print("🔄 Attempting recovery...")
                time.sleep(30)  # Brief pause before recovery
        
        print("\n🛑 WealthyRobot Autonomous Service stopping...")
        self.stop_all_processes()
        return True
    
    def generate_service_report(self):
        """Generate and save service status report"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'cycle_count': self.cycle_count,
                'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
                'service_status': 'running' if self.running else 'stopping',
                'last_health_check': self.last_health_check.isoformat()
            }
            
            with open('autonomous_service_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            print("📊 Service report generated")
        except Exception as e:
            print(f"⚠️ Failed to generate service report: {e}")

def main():
    """Main entry point"""
    service = WealthyRobotAutonomousServiceSimple()
    
    try:
        success = service.run_autonomous_service()
        if success:
            print("✅ Service completed successfully")
        else:
            print("❌ Service failed")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Critical service error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

