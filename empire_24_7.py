import time
import os
from datetime import datetime

def run_empire_24_7():
    """Run your 16-agent autonomous empire 24/7"""
    print("👑 STARTING 24/7 AUTONOMOUS EMPIRE OPERATION")
    print("=" * 50)
    print("🤖 16 Agents working continuously")
    print("📊 Generating business intelligence non-stop")
    print("💰 Creating value while you sleep!")
    
    cycle = 0
    
    while True:
        try:
            cycle += 1
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n🔄 Empire Cycle #{cycle} - {timestamp}")
            
            # Run CEO strategic decisions
            print("👑 CEO: Making strategic decisions...")
            os.system("python3 -c 'from ultimate_ceo_agent import UltimateAutonomousCEO; ceo = UltimateAutonomousCEO(); ceo.run_ultimate_ceo_cycle()'")
            
            # Run all 16 agents
            print("🤖 Running all 16 autonomous agents...")
            os.system("python3 run_all_agents.py")
            
            # Run live orchestrator cycle
            print("🎮 Running live orchestrator integration...")
            os.system("python3 -c 'from live_orchestrator import LiveAutonomousOrchestrator; o = LiveAutonomousOrchestrator(); o.run_full_automation_cycle()'")
            
            print(f"✅ Empire Cycle #{cycle} Complete!")
            print("💰 Your empire generated value this cycle!")
            print("⏰ Next cycle in 30 minutes...")
            
            # Wait 30 minutes between cycles
            time.sleep(1800)
            
        except KeyboardInterrupt:
            print(f"\n👋 Stopping autonomous empire after {cycle} cycles...")
            break
        except Exception as e:
            print(f"⚠️ Empire error (cycle {cycle}): {e}")
            print("🔄 Restarting in 5 minutes...")
            time.sleep(300)

if __name__ == "__main__":
    run_empire_24_7()
