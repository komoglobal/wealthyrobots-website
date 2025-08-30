#!/usr/bin/env python3
"""
AGENT COORDINATOR
PURPOSE: Coordinate all agents, ensure quality, and manage fixes
CATEGORY: System Management
STATUS: Active - Enhanced
FREQUENCY: Continuous
"""

import os
import json
import subprocess
import time
from datetime import datetime
import importlib.util
import sys

class AgentCoordinator:
    def __init__(self):
        self.agents = {}
        self.test_results = {}
        self.fixes_applied = []
        self.agent_status = {}
        
        self.available_agents = {
            "enhanced_visual_testing": "enhanced_visual_testing_agent.py",
            "website_builder": "comprehensive_website_builder_agent.py",
            "content_generator": "optimized_content_agent.py",
            "seo_optimizer": "seo_optimizer_agent.py",
            "affiliate_manager": "smart_affiliate_agent.py",
            "social_media": "social_media_agent.py",
            "orchestrator": "live_orchestrator.py",
            "pagespeed": "pagespeed_budget_agent.py",
            "competitor_watcher": "competitor_watcher_agent.py",
            "optimizer": "optimizer_agent.py"
        }
        
        self.load_agents()
    
    def load_agents(self):
        print("🔧 LOADING AGENTS")
        print("=" * 30)
        for agent_name, agent_file in self.available_agents.items():
            if os.path.exists(agent_file):
                try:
                    spec = importlib.util.spec_from_file_location(agent_name, agent_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.agents[agent_name] = {
                        "file": agent_file,
                        "module": module,
                        "status": "loaded",
                        "last_run": None,
                        "success_count": 0,
                        "error_count": 0
                    }
                    print(f"✅ Loaded: {agent_name}")
                except Exception as e:
                    print(f"❌ Failed to load {agent_name}: {e}")
                    self.agents[agent_name] = {"file": agent_file, "status": "error", "error": str(e)}
            else:
                print(f"⚠️ Agent file not found: {agent_file}")
    
    def run_agent(self, agent_name, method_name="main"):
        if agent_name not in self.agents:
            return {"error": f"Agent {agent_name} not found"}
        agent = self.agents[agent_name]
        if agent["status"] != "loaded":
            return {"error": f"Agent {agent_name} not properly loaded"}
        try:
            print(f"🚀 Running {agent_name}...")
            if hasattr(agent["module"], method_name):
                result = getattr(agent["module"], method_name)()
            else:
                # try to run default .run()
                if hasattr(agent["module"], agent_name.title().replace('_','')):
                    cls = getattr(agent["module"], agent_name.title().replace('_',''))
                    inst = cls()
                    result = inst.run()
                elif hasattr(agent["module"], 'main'):
                    result = agent["module"].main()
                elif hasattr(agent["module"], 'PageSpeedBudgetAgent'):
                    result = agent["module"].PageSpeedBudgetAgent().run()
                elif hasattr(agent["module"], 'CompetitorWatcher'):
                    result = agent["module"].CompetitorWatcher().run()
                else:
                    result = {"error": f"No runnable entry in {agent_name}"}
            agent["last_run"] = datetime.now().isoformat()
            if "error" not in result:
                agent["success_count"] += 1
                agent["status"] = "success"
            else:
                agent["error_count"] += 1
                agent["status"] = "error"
            return result
        except Exception as e:
            agent["error_count"] += 1
            agent["status"] = "error"
            return {"error": f"Error running {agent_name}: {str(e)}"}

    def run_performance_and_competitors(self):
        print("\n📈 PERFORMANCE & COMPETITOR CHECKS")
        print("=" * 40)
        self.run_agent("pagespeed")
        self.run_agent("competitor_watcher")
    
    def run_optimizer(self):
        print("\n🧹 REPOSITORY OPTIMIZER")
        print("=" * 30)
        return self.run_agent("optimizer", "main")
    
    def run_enhanced_visual_test(self):
        """Run the enhanced visual testing agent"""
        return self.run_agent("enhanced_visual_testing", "main")
    
    def run_website_builder(self):
        """Run the website builder agent"""
        return self.run_agent("website_builder", "main")
    
    def coordinate_quality_assurance(self):
        """Coordinate quality assurance across all agents"""
        print("🔍 COORDINATING QUALITY ASSURANCE")
        print("=" * 40)
        
        # Step 1: Run visual testing
        print("\n1️⃣ Running Enhanced Visual Testing...")
        visual_test_result = self.run_enhanced_visual_test()
        
        if "error" in visual_test_result:
            print(f"❌ Visual testing failed: {visual_test_result['error']}")
            return visual_test_result
        
        # Step 2: Analyze results and coordinate fixes
        print("\n2️⃣ Analyzing Test Results...")
        if visual_test_result.get("overall_score", 0) < 90:
            print("⚠️ Issues detected - coordinating fixes...")
            
            # Run website builder to fix issues
            print("\n3️⃣ Running Website Builder to Fix Issues...")
            builder_result = self.run_website_builder()
            
            if "error" not in builder_result:
                print("✅ Website builder completed successfully")
                
                # Run visual testing again to verify fixes
                print("\n4️⃣ Re-testing After Fixes...")
                retest_result = self.run_enhanced_visual_test()
                
                if retest_result.get("overall_score", 0) >= 90:
                    print("🎉 All issues resolved!")
                else:
                    print(f"⚠️ Some issues remain: Score {retest_result.get('overall_score', 0)}/100")
            else:
                print(f"❌ Website builder failed: {builder_result['error']}")
        else:
            print("✅ Website is in good condition!")
        
        return visual_test_result
    
    def run_continuous_monitoring(self):
        """Run continuous monitoring of all agents"""
        print("🔄 CONTINUOUS MONITORING")
        print("=" * 30)
        
        while True:
            try:
                # Check all agents
                for agent_name, agent in self.agents.items():
                    if agent["status"] == "error":
                        print(f"⚠️ Agent {agent_name} has errors - attempting recovery...")
                        
                        # Try to reload the agent
                        self.load_agents()
                
                # Run quality assurance
                qa_result = self.coordinate_quality_assurance()
                
                # Log results
                self.log_monitoring_results(qa_result)
                
                # Wait before next cycle
                print("⏰ Waiting 30 minutes before next monitoring cycle...")
                time.sleep(1800)  # 30 minutes
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    def log_monitoring_results(self, results):
        """Log monitoring results"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_status": {name: agent["status"] for name, agent in self.agents.items()},
            "test_results": results,
            "fixes_applied": self.fixes_applied
        }
        
        # Save to log file
        log_filename = f"agent_coordination_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_filename, 'w') as f:
            json.dump(log_entry, f, indent=2)
        
        print(f"📄 Monitoring log saved: {log_filename}")
    
    def get_agent_status(self):
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                "status": agent["status"],
                "last_run": agent.get("last_run"),
                "success_count": agent.get("success_count", 0),
                "error_count": agent.get("error_count", 0)
            }
        return status
    
    def run_comprehensive_coordination(self):
        """Run comprehensive agent coordination"""
        print("🚀 AGENT COORDINATOR - COMPREHENSIVE COORDINATION")
        print("=" * 60)
        
        # Step 1: Load and verify all agents
        print("\n1️⃣ Loading and Verifying Agents...")
        self.load_agents()
        
        # Step 2: Run quality assurance
        print("\n2️⃣ Running Quality Assurance...")
        qa_result = self.coordinate_quality_assurance()
        
        # Step 3: Generate coordination report
        print("\n3️⃣ Generating Coordination Report...")
        report = {
            "timestamp": datetime.now().isoformat(),
            "coordination_type": "comprehensive_agent_coordination",
            "agent_status": self.get_agent_status(),
            "qa_results": qa_result,
            "fixes_applied": self.fixes_applied,
            "recommendations": self.generate_recommendations()
        }
        
        # Save report
        report_filename = f"agent_coordination_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Coordination report saved: {report_filename}")
        print(f"🎉 Comprehensive coordination completed!")
        
        return report
    
    def generate_recommendations(self):
        """Generate recommendations based on agent status"""
        recommendations = []
        
        # Check agent health
        error_agents = [name for name, agent in self.agents.items() if agent["status"] == "error"]
        if error_agents:
            recommendations.append(f"🚨 Fix agents with errors: {', '.join(error_agents)}")
        
        # Check for successful agents
        success_agents = [name for name, agent in self.agents.items() if agent["status"] == "success"]
        if len(success_agents) >= 5:
            recommendations.append("✅ Most agents are working correctly")
        
        # Check for agents that haven't run recently
        current_time = datetime.now()
        for name, agent in self.agents.items():
            if agent.get("last_run"):
                last_run = datetime.fromisoformat(agent["last_run"])
                if (current_time - last_run).total_seconds() > 3600:  # 1 hour
                    recommendations.append(f"⏰ Agent {name} hasn't run recently")
        
        return recommendations

def main():
    """Main function to run the agent coordinator"""
    coordinator = AgentCoordinator()
    
    # Run comprehensive coordination
    report = coordinator.run_comprehensive_coordination()
    
    if "error" in report:
        print(f"❌ Coordination failed: {report['error']}")
    else:
        print(f"✅ Coordination completed successfully!")

if __name__ == "__main__":
    main()
