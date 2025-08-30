#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: Optimized Live Orchestrator
PURPOSE: Master coordinator managing all empire agents with enhanced workflow management and CEO integration
CATEGORY: Core Control
STATUS: Active - Optimized
FREQUENCY: Continuous
"""

import json
import time
import os
import logging
from datetime import datetime, timedelta
import subprocess
import glob
import sys

# Import optimized agents
try:
    from optimized_content_agent import OptimizedContentAgent
    from smart_affiliate_agent import SmartAffiliateAgent
    from social_media_agent import SocialMediaAgent
    CONTENT_AGENT_AVAILABLE = True
    print("✅ Optimized agents imported successfully")
except ImportError as e:
    print(f"⚠️ Some optimized agents not available: {e}")
    CONTENT_AGENT_AVAILABLE = False

class OptimizedLiveOrchestrator:
    def __init__(self):
        self.config_file = 'optimized_config.json'
        self.cycle_count = 0
        self.last_run = {}
        
        # Initialize optimized agents
        if CONTENT_AGENT_AVAILABLE:
            self.content_agent = OptimizedContentAgent()
            print("✅ Optimized content agent initialized")
        else:
            self.content_agent = None
            print("⚠️ Content agent not available - using fallback")
        
        self.load_config()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup enhanced logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('optimized_orchestrator.log'),
                logging.StreamHandler()
            ]
        )
    
    def load_config(self):
        """Load optimized configuration"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                "posting_enabled": True,
                "content_strategy": "80_20_value_affiliate",
                "emergency_mode": False,
                "daily_budget": 100,
                "agent_coordination": True,
                "performance_monitoring": True,
                "auto_optimization": True
            }
            self.save_config()
    
    def save_config(self):
        """Save optimized configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def should_create_content(self):
        """Enhanced content creation logic"""
        now = datetime.now()
        
        # Check if enough time has passed since last content creation
        last_content = self.last_run.get('content_creation')
        if last_content:
            last_time = datetime.fromisoformat(last_content)
            if (now - last_time).total_seconds() < 3600:  # 1 hour minimum
                return False
        
        # Check if we're in optimal posting hours
        hour = now.hour
        optimal_hours = [8, 12, 17, 20]  # Optimal posting times
        if hour not in optimal_hours:
            return False
        
        return True
    
    def create_optimized_content(self):
        """Create content using optimized agent"""
        if not self.content_agent:
            print("⚠️ Content agent not available")
            return False
        
        try:
            print("🎯 Creating optimized content...")
            report = self.content_agent.run_optimized_cycle()
            
            self.last_run['content_creation'] = datetime.now().isoformat()
            self.cycle_count += 1
            
            # Log success
            logging.info(f"Content creation cycle {self.cycle_count} completed successfully")
            
            return True
            
        except Exception as e:
            logging.error(f"Content creation failed: {e}")
            return False
    
    def run_optimized_cycle(self):
        """Run optimized orchestration cycle"""
        print("🔄 OPTIMIZED ORCHESTRATOR CYCLE")
        print("=" * 40)
        
        try:
            # Check if content should be created
            if self.should_create_content():
                success = self.create_optimized_content()
                if success:
                    print("✅ Content creation successful")
                else:
                    print("❌ Content creation failed")
            else:
                print("⏰ Not time for content creation")
            
            # Update cycle count
            self.cycle_count += 1
            
            # Log cycle completion
            cycle_data = {
                "timestamp": datetime.now().isoformat(),
                "cycle": self.cycle_count,
                "content_agent_used": CONTENT_AGENT_AVAILABLE,
                "config_status": "active"
            }
            
            logging.info(f"Optimized cycle {self.cycle_count} completed")
            
            return cycle_data
            
        except Exception as e:
            logging.error(f"Optimized cycle failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_continuous(self):
        """Run continuous optimized orchestration"""
        print("🚀 STARTING OPTIMIZED CONTINUOUS ORCHESTRATION")
        print("=" * 50)
        
        while True:
            try:
                cycle_data = self.run_optimized_cycle()
                print(f"✅ Cycle {cycle_data.get('cycle', 'unknown')} completed")
                
                # Wait 30 minutes before next cycle
                time.sleep(1800)
                
            except KeyboardInterrupt:
                print("\n🛑 Optimized orchestration stopped by user")
                break
            except Exception as e:
                logging.error(f"Continuous orchestration error: {e}")
                time.sleep(300)  # Wait 5 minutes on error

def main():
    orchestrator = OptimizedLiveOrchestrator()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--continuous":
            orchestrator.run_continuous()
        elif sys.argv[1] == "--status":
            print(f"Optimized Orchestrator Status: Active (Cycle {orchestrator.cycle_count})")
        else:
            orchestrator.run_optimized_cycle()
    else:
        orchestrator.run_optimized_cycle()

if __name__ == "__main__":
    main()
