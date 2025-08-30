#!/usr/bin/env python3
"""
AUTOMATED TIKTOK SYSTEM ORCHESTRATOR
Coordinates all components for fully automated operation
"""

import json
import time
import schedule
from datetime import datetime
from typing import Dict, List

class AutomatedTikTokOrchestrator:
    def __init__(self):
        self.system_status = "running"
        self.automation_cycles = 0
        self.total_revenue_generated = 0.0
        self.content_pipeline = []
        
    def run_complete_automation_cycle(self) -> Dict:
        """Run one complete automation cycle"""
        
        print("🤖 RUNNING COMPLETE AUTOMATED TIKTOK CYCLE")
        print("=" * 50)
        
        cycle_start = datetime.now()
        
        # 1. Content Discovery
        print("🔍 Step 1: Content Discovery")
        from content_discovery_agent import ContentDiscoveryAgent
        discovery_agent = ContentDiscoveryAgent()
        discovery_results = discovery_agent.run_discovery_cycle()
        
        # 2. Automated Editing
        print("✂️ Step 2: Automated Editing")
        from automated_editing_agent import AutomatedEditingAgent
        editing_agent = AutomatedEditingAgent()
        
        # Get processed content from discovery
        discovered_content = discovery_results.get("processed_content", [])
        print(f"📊 Content to process: {len(discovered_content)} items")
        
        editing_results = editing_agent.run_editing_cycle(discovered_content)
        
        # 3. TikTok Integration
        print("📱 Step 3: TikTok Integration")
        from tiktok_integration_agent import TikTokIntegrationAgent
        tiktok_agent = TikTokIntegrationAgent()
        posting_results = tiktok_agent.run_posting_cycle(editing_results.get("edited_content", []))
        
        # 4. Revenue Optimization
        print("💰 Step 4: Revenue Optimization")
        from revenue_optimization_agent import RevenueOptimizationAgent
        revenue_agent = RevenueOptimizationAgent()
        revenue_results = revenue_agent.run_revenue_optimization_cycle(posting_results.get("posted_content", []))
        
        # 5. Performance Monitoring
        print("📊 Step 5: Performance Monitoring")
        from performance_monitoring_agent import PerformanceMonitoringAgent
        monitoring_agent = PerformanceMonitoringAgent()
        monitoring_results = monitoring_agent.run_monitoring_cycle([c["post"]["post_id"] for c in posting_results.get("posted_content", [])])
        
        # Calculate cycle results
        cycle_end = datetime.now()
        cycle_duration = (cycle_end - cycle_start).total_seconds()
        
        cycle_results = {
            "cycle_number": self.automation_cycles + 1,
            "timestamp": datetime.now().isoformat(),
            "cycle_duration_seconds": cycle_duration,
            "discovery_results": discovery_results,
            "editing_results": editing_results,
            "posting_results": posting_results,
            "revenue_results": revenue_results,
            "monitoring_results": monitoring_results,
            "cycle_success": True
        }
        
        # Update system metrics
        self.automation_cycles += 1
        self.total_revenue_generated += revenue_results.get("total_revenue_generated", 0)
        
        # Save cycle results
        with open(f"automation_cycle_{self.automation_cycles}.json", "w") as f:
            json.dump(cycle_results, f, indent=2)
        
        print(f"✅ Automation cycle {self.automation_cycles} completed in {cycle_duration:.1f} seconds")
        print(f"💰 Total revenue generated: ${self.total_revenue_generated:.2f}")
        
        return cycle_results
    
    def start_automated_operation(self):
        """Start fully automated operation"""
        
        print("🚀 STARTING FULLY AUTOMATED TIKTOK OPERATION")
        print("=" * 50)
        
        # Schedule automation cycles
        schedule.every(4).hours.do(self.run_complete_automation_cycle)
        schedule.every().day.at("09:00").do(self.run_complete_automation_cycle)
        schedule.every().day.at("15:00").do(self.run_complete_automation_cycle)
        schedule.every().day.at("21:00").do(self.run_complete_automation_cycle)
        
        # Run initial cycle
        self.run_complete_automation_cycle()
        
        # Keep running
        while self.system_status == "running":
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_automation(self):
        """Stop automated operation"""
        
        self.system_status = "stopped"
        print("⏹️ Automated operation stopped")
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        
        return {
            "system_status": self.system_status,
            "automation_cycles": self.automation_cycles,
            "total_revenue_generated": self.total_revenue_generated,
            "last_cycle": datetime.now().isoformat(),
            "next_scheduled_cycle": "4 hours from now"
        }

def main():
    """Main function to run the automated system"""
    
    print("🎬 AUTOMATED TIKTOK PROFIT SYSTEM")
    print("=" * 40)
    
    orchestrator = AutomatedTikTokOrchestrator()
    
    try:
        orchestrator.start_automated_operation()
    except KeyboardInterrupt:
        print("\n⏹️ Stopping automation...")
        orchestrator.stop_automation()
    except Exception as e:
        print(f"❌ Error in automation: {e}")
        orchestrator.stop_automation()

if __name__ == "__main__":
    main()
