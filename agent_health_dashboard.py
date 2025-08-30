#!/usr/bin/env python3
"""
Agent Health Monitoring Dashboard - WealthyRobot Empire
Real-time monitoring and visualization of agent health, performance, and system status
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

# Import our existing systems
try:
    from centralized_logger import CentralizedLogger, logger
    from performance_tracker import PerformanceTracker, performance_tracker
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False

class AgentStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    STARTING = "starting"
    UNKNOWN = "unknown"

class HealthLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class AgentHealth:
    """Health status of an individual agent"""
    name: str
    status: AgentStatus
    last_heartbeat: Optional[datetime]
    uptime: Optional[timedelta]
    error_count: int = 0
    performance_score: float = 0.0
    health_level: HealthLevel = HealthLevel.UNKNOWN
    last_error: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SystemHealth:
    """Overall system health status"""
    timestamp: datetime
    total_agents: int
    running_agents: int
    error_agents: int
    warning_agents: int
    system_uptime: timedelta
    overall_health: HealthLevel
    critical_issues: List[str]
    recommendations: List[str]

class AgentHealthDashboard:
    """Real-time agent health monitoring dashboard"""

    def __init__(self, name='agent_health_dashboard', status='active', last_heartbeat=None, uptime=0):
        self.agents: Dict[str, AgentHealth] = {}
        self.system_start_time = datetime.now()
        self.dashboard_file = "agent_health_dashboard.json"
        self.update_interval = 30  # seconds
        self.is_monitoring = False
        self.monitoring_thread = None

        # Initialize with known agents
        self._discover_agents()

        # Start monitoring if logging is available
        if LOGGING_AVAILABLE:
            self.start_monitoring()

    def _discover_agents(self):
        """Discover all available agents in the system"""
        print("🔍 Discovering agents for health monitoring...")

        # Common agent files to monitor
        agent_files = [
            "agent_coordination_system.py",
            "optimized_content_agent.py",
            "optimized_orchestrator.py",
            "authority_website_manager.py",
            "comprehensive_website_builder_agent.py",
            "smart_affiliate_agent.py",
            "social_media_agent.py",
            "data_analytics_agent.py",
            "performance_tracker.py",
            "centralized_logger.py",
            "automated_backup.py"
        ]

        for agent_file in agent_files:
            if os.path.exists(agent_file):
                agent_name = agent_file.replace('.py', '').replace('_', ' ').title()
                self.agents[agent_name] = AgentHealth(
                    name=agent_name,
                    status=AgentStatus.UNKNOWN,
                    last_heartbeat=None,
                    uptime=None
                )
                print(f"✅ Added to monitoring: {agent_name}")

        print(f"📊 Monitoring {len(self.agents)} agents")

    def update_agent_status(self, agent_name: str, status: AgentStatus,
                           error_message: Optional[str] = None):
        """Update the status of an agent"""
        if agent_name not in self.agents:
            self.agents[agent_name] = AgentHealth(
                name=agent_name,
                status=status,
                last_heartbeat=datetime.now(),
                uptime=None
            )

        agent = self.agents[agent_name]
        agent.status = status
        agent.last_heartbeat = datetime.now()

        if error_message:
            agent.error_count += 1
            agent.last_error = error_message

        # Update uptime
        if status == AgentStatus.RUNNING and agent.last_heartbeat:
            # Simple uptime tracking (would be more sophisticated in production)
            agent.uptime = timedelta(seconds=300)  # Placeholder
        elif status in [AgentStatus.STOPPED, AgentStatus.ERROR]:
            agent.uptime = None

        # Update health level
        calculated_health = self._calculate_agent_health(agent)
        # Ensure it's always a HealthLevel enum
        if isinstance(calculated_health, str):
            try:
                agent.health_level = HealthLevel(calculated_health)
            except ValueError:
                agent.health_level = HealthLevel.UNKNOWN
        else:
            agent.health_level = calculated_health

        # Log the status change
        if LOGGING_AVAILABLE:
            logger.log_agent_activity(
                agent_name,
                f"Status changed to {status.value}",
                {"error": error_message} if error_message else {}
            )

    def _calculate_agent_health(self, agent: AgentHealth) -> HealthLevel:
        """Calculate health level for an agent"""
        try:
            if agent.status == AgentStatus.ERROR:
                return HealthLevel.CRITICAL
            elif agent.status == AgentStatus.STOPPED:
                return HealthLevel.WARNING
            elif agent.status == AgentStatus.RUNNING:
                if agent.error_count > 5:
                    return HealthLevel.WARNING
                elif agent.error_count > 10:
                    return HealthLevel.CRITICAL
                else:
                    return HealthLevel.GOOD
            else:
                return HealthLevel.UNKNOWN
        except Exception as e:
            print(f"Error calculating agent health: {e}")
            return HealthLevel.UNKNOWN

    def get_system_health(self) -> SystemHealth:
        """Get overall system health status"""
        now = datetime.now()
        total_agents = len(self.agents)
        running_agents = sum(1 for agent in self.agents.values() if agent.status == AgentStatus.RUNNING)
        error_agents = sum(1 for agent in self.agents.values() if agent.status == AgentStatus.ERROR)
        warning_agents = sum(1 for agent in self.agents.values() if agent.health_level == HealthLevel.WARNING)

        # Calculate overall health
        if error_agents > 0:
            overall_health = HealthLevel.CRITICAL
        elif warning_agents > 3:
            overall_health = HealthLevel.WARNING
        elif running_agents >= total_agents * 0.8:
            overall_health = HealthLevel.GOOD
        elif running_agents >= total_agents * 0.5:
            overall_health = HealthLevel.WARNING
        else:
            overall_health = HealthLevel.CRITICAL

        # Generate critical issues
        critical_issues = []
        if error_agents > 0:
            critical_issues.append(f"{error_agents} agents in error state")
        if running_agents < total_agents * 0.5:
            critical_issues.append("Less than 50% of agents running")
        if warning_agents > 5:
            critical_issues.append(f"{warning_agents} agents with warnings")

        # Generate recommendations
        recommendations = []
        if error_agents > 0:
            recommendations.append("Investigate and restart failed agents")
        if running_agents < total_agents:
            recommendations.append("Start remaining agents to improve system performance")
        if warning_agents > 0:
            recommendations.append("Monitor agents with warnings for potential issues")

        return SystemHealth(
            timestamp=now,
            total_agents=total_agents,
            running_agents=running_agents,
            error_agents=error_agents,
            warning_agents=warning_agents,
            system_uptime=now - self.system_start_time,
            overall_health=overall_health,
            critical_issues=critical_issues,
            recommendations=recommendations
        )

    def get_agent_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for all agents"""
        if not LOGGING_AVAILABLE:
            return {"status": "performance_tracking_unavailable"}

        try:
            performance_summary = performance_tracker.get_system_performance_summary()
            return performance_summary
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        system_health = self.get_system_health()
        performance_summary = self.get_agent_performance_summary()

        # Agent details
        agent_details = {}
        for name, agent in self.agents.items():
            agent_details[name] = {
                "status": agent.status.value,
                "health_level": agent.health_level.value if hasattr(agent.health_level, 'value') else str(agent.health_level),
                "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None,
                "uptime_seconds": agent.uptime.total_seconds() if agent.uptime else 0,
                "error_count": agent.error_count,
                "last_error": agent.last_error,
                "performance_score": agent.performance_score
            }

        # System metrics
        system_metrics = {
            "agent_status_distribution": {},
            "health_level_distribution": {},
            "error_rate": 0.0,
            "average_uptime": 0.0
        }

        # Calculate distributions
        status_counts = {}
        health_counts = {}
        total_uptime = 0
        uptime_count = 0

        for agent in self.agents.values():
            # Status distribution
            status_counts[agent.status.value] = status_counts.get(agent.status.value, 0) + 1

            # Health distribution
            health_level_str = agent.health_level.value if hasattr(agent.health_level, 'value') else str(agent.health_level)
            health_counts[health_level_str] = health_counts.get(health_level_str, 0) + 1

            # Uptime calculation
            if agent.uptime:
                total_uptime += agent.uptime.total_seconds()
                uptime_count += 1

        system_metrics["agent_status_distribution"] = status_counts
        system_metrics["health_level_distribution"] = health_counts
        system_metrics["error_rate"] = sum(agent.error_count for agent in self.agents.values()) / max(len(self.agents), 1)
        system_metrics["average_uptime"] = total_uptime / max(uptime_count, 1)

        return {
            "timestamp": datetime.now().isoformat(),
            "system_health": {
                "overall_health": system_health.overall_health.value,
                "total_agents": system_health.total_agents,
                "running_agents": system_health.running_agents,
                "error_agents": system_health.error_agents,
                "warning_agents": system_health.warning_agents,
                "system_uptime": system_health.system_uptime.total_seconds(),
                "critical_issues": system_health.critical_issues,
                "recommendations": system_health.recommendations
            },
            "agent_details": agent_details,
            "system_metrics": system_metrics,
            "performance_summary": performance_summary
        }

    def display_dashboard(self):
        """Display the health dashboard in console"""
        print("\n🤖 WEALTHYROBOT EMPIRE - AGENT HEALTH DASHBOARD")
        print("=" * 60)

        system_health = self.get_system_health()

        # System overview
        print(f"📊 System Status: {system_health.overall_health.value.upper()}")
        print(f"⏱️  System Uptime: {system_health.system_uptime}")
        print(f"🤖 Total Agents: {system_health.total_agents}")
        print(f"🟢 Running: {system_health.running_agents}")
        print(f"🔴 Errors: {system_health.error_agents}")
        print(f"🟡 Warnings: {system_health.warning_agents}")
        print()

        # Critical issues
        if system_health.critical_issues:
            print("🚨 CRITICAL ISSUES:")
            for issue in system_health.critical_issues:
                print(f"   • {issue}")
            print()

        # Agent status
        print("📋 AGENT STATUS:")
        for name, agent in sorted(self.agents.items()):
            status_icon = {
                AgentStatus.RUNNING: "🟢",
                AgentStatus.ERROR: "🔴",
                AgentStatus.STOPPED: "⚫",
                AgentStatus.STARTING: "🟡",
                AgentStatus.UNKNOWN: "⚪"
            }.get(agent.status, "⚪")

            health_icon = {
                HealthLevel.EXCELLENT: "💚",
                HealthLevel.GOOD: "💙",
                HealthLevel.WARNING: "💛",
                HealthLevel.CRITICAL: "❤️",
                HealthLevel.UNKNOWN: "🤍"
            }.get(agent.health_level, "🤍")

            uptime_str = f"{agent.uptime.total_seconds():.0f}s" if agent.uptime else "N/A"

            print(f"   {status_icon} {health_icon} {name}")
            print(f"      Status: {agent.status.value} | Health: {agent.health_level.value}")
            print(f"      Uptime: {uptime_str} | Errors: {agent.error_count}")

            if agent.last_error:
                print(f"      Last Error: {agent.last_error[:60]}...")
            print()

        # Recommendations
        if system_health.recommendations:
            print("💡 RECOMMENDATIONS:")
            for rec in system_health.recommendations:
                print(f"   • {rec}")
            print()

        # Performance summary
        if LOGGING_AVAILABLE:
            performance = self.get_agent_performance_summary()
            if performance.get("status") == "success":
                print("📈 PERFORMANCE SUMMARY:")
                print(f"   Top Performers: {len(performance.get('top_performers', []))}")
                print(f"   Needs Attention: {len(performance.get('needs_attention', []))}")
                print(f"   Performance Distribution: {performance.get('performance_distribution', {})}")

    def save_dashboard_data(self):
        """Save dashboard data to file"""
        try:
            report = self.generate_health_report()
            with open(self.dashboard_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"💾 Dashboard data saved to {self.dashboard_file}")
        except Exception as e:
            print(f"❌ Error saving dashboard data: {e}")

    def start_monitoring(self):
        """Start background monitoring"""
        if self.is_monitoring:
            return

        self.is_monitoring = True

        def monitoring_worker():
            while self.is_monitoring:
                try:
                    # Update agent statuses (this would integrate with actual agent monitoring)
                    self._check_agent_statuses()

                    # Save dashboard data
                    self.save_dashboard_data()

                    # Wait before next update
                    time.sleep(self.update_interval)

                except Exception as e:
                    print(f"❌ Monitoring error: {e}")
                    time.sleep(60)  # Wait longer on error

        self.monitoring_thread = threading.Thread(target=monitoring_worker, daemon=True)
        self.monitoring_thread.start()
        print("✅ Agent health monitoring started")

    def stop_monitoring(self):
        """Stop background monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        print("🛑 Agent health monitoring stopped")

    def _check_agent_statuses(self):
        """Check the status of all monitored agents"""
        # This is a simplified version - in production, this would integrate
        # with actual process monitoring, heartbeat systems, etc.

        # Create a copy of agent names to avoid dictionary modification during iteration
        agent_names = list(self.agents.keys())

        for agent_name in agent_names:
            # Get the agent object
            if agent_name not in self.agents:
                continue

            agent = self.agents[agent_name]

            # Simulate status checking - in reality, this would check:
            # - Process status
            # - Heartbeat files
            # - API endpoints
            # - Log activity

            # For now, we'll mark agents as running if they exist
            if agent.status == AgentStatus.UNKNOWN:
                self.update_agent_status(agent_name, AgentStatus.RUNNING)

            # Simulate occasional errors for demonstration
            import random
            if random.random() < 0.05:  # 5% chance of simulated error
                self.update_agent_status(
                    agent_name,
                    AgentStatus.ERROR,
                    f"Simulated error in {agent_name}"
                )
            elif agent.status == AgentStatus.ERROR and random.random() < 0.3:  # 30% chance to recover
                self.update_agent_status(agent_name, AgentStatus.RUNNING)

    def get_health_score(self) -> float:
        """Get overall system health score (0-100)"""
        system_health = self.get_system_health()

        # Base score from agent status
        if system_health.overall_health == HealthLevel.EXCELLENT:
            base_score = 100
        elif system_health.overall_health == HealthLevel.GOOD:
            base_score = 80
        elif system_health.overall_health == HealthLevel.WARNING:
            base_score = 60
        elif system_health.overall_health == HealthLevel.CRITICAL:
            base_score = 40
        else:
            base_score = 50

        # Adjust based on agent ratios
        running_ratio = system_health.running_agents / max(system_health.total_agents, 1)
        error_penalty = (system_health.error_agents / max(system_health.total_agents, 1)) * 30

        score = base_score * running_ratio - error_penalty
        return max(0, min(100, score))

# Global dashboard instance
dashboard = AgentHealthDashboard()

# Convenience functions
def update_agent_status(agent_name: str, status: AgentStatus, error_message: Optional[str] = None):
    """Convenience function to update agent status"""
    dashboard.update_agent_status(agent_name, status, error_message)

def get_system_health():
    """Get current system health"""
    return dashboard.get_system_health()

def display_dashboard():
    """Display the health dashboard"""
    dashboard.display_dashboard()

if __name__ == "__main__":
    print("🧪 Testing Agent Health Dashboard")
    print("=" * 40)

    # Display initial dashboard
    dashboard.display_dashboard()

    # Simulate some status updates
    print("\n🔄 Simulating status updates...")
    update_agent_status("Optimized Content Agent", AgentStatus.RUNNING)
    update_agent_status("Smart Affiliate Agent", AgentStatus.ERROR, "Connection timeout")
    update_agent_status("Authority Website Manager", AgentStatus.RUNNING)
    update_agent_status("Agent Coordination System", AgentStatus.RUNNING)

    # Display updated dashboard
    print("\n📊 Updated Dashboard:")
    dashboard.display_dashboard()

    # Generate and display health report
    report = dashboard.generate_health_report()
    print("\n📋 Health Score: {:.1f}/100".format(dashboard.get_health_score()))

    print("\n✅ Agent health dashboard test complete!")

    # Start monitoring (will run in background)
    print("\n🔄 Starting background monitoring...")
    # Note: In a real scenario, this would run continuously
    # dashboard.start_monitoring()
    # time.sleep(10)  # Let it run for a bit
    # dashboard.stop_monitoring()
