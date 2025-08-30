#!/usr/bin/env python3
"""
Performance Metrics Tracker - WealthyRobot Empire
Tracks and analyzes agent performance across multiple dimensions
"""

import time
import json
import os
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import statistics
from collections import defaultdict

class MetricType(Enum):
    RESPONSE_TIME = "response_time"
    SUCCESS_RATE = "success_rate"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    RESOURCE_USAGE = "resource_usage"
    CUSTOM = "custom"

class PerformanceLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    CRITICAL = "critical"

@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    name: str
    value: Any
    timestamp: datetime
    metric_type: MetricType
    agent_name: str
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentPerformanceProfile:
    """Performance profile for an agent"""
    agent_name: str
    metrics: List[PerformanceMetric] = field(default_factory=list)
    summary_stats: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = None
    performance_level: PerformanceLevel = PerformanceLevel.AVERAGE

    def add_metric(self, metric: PerformanceMetric):
        """Add a metric to this agent's profile"""
        self.metrics.append(metric)
        self.last_updated = datetime.now()
        self._update_summary_stats()

    def _update_summary_stats(self):
        """Update summary statistics"""
        if not self.metrics:
            return

        # Group metrics by type
        metrics_by_type = defaultdict(list)

        for metric in self.metrics:
            if isinstance(metric.value, (int, float)):
                metrics_by_type[metric.metric_type.value].append(metric.value)

        # Calculate statistics for each type
        for metric_type, values in metrics_by_type.items():
            if len(values) > 1:
                self.summary_stats[f"{metric_type}_mean"] = statistics.mean(values)
                self.summary_stats[f"{metric_type}_median"] = statistics.median(values)
                self.summary_stats[f"{metric_type}_std_dev"] = statistics.stdev(values)
                self.summary_stats[f"{metric_type}_min"] = min(values)
                self.summary_stats[f"{metric_type}_max"] = max(values)
            else:
                self.summary_stats[f"{metric_type}_value"] = values[0]

        # Calculate overall performance level
        self.performance_level = self._calculate_performance_level()

    def _calculate_performance_level(self) -> PerformanceLevel:
        """Calculate overall performance level"""
        if not self.summary_stats:
            return PerformanceLevel.AVERAGE

        score = 0
        factors = 0

        # Response time scoring (lower is better)
        if "response_time_mean" in self.summary_stats:
            response_time = self.summary_stats["response_time_mean"]
            if response_time < 0.5:
                score += 5
            elif response_time < 1.0:
                score += 4
            elif response_time < 2.0:
                score += 3
            elif response_time < 5.0:
                score += 2
            else:
                score += 1
            factors += 1

        # Success rate scoring (higher is better)
        if "success_rate_mean" in self.summary_stats:
            success_rate = self.summary_stats["success_rate_mean"]
            if success_rate > 0.95:
                score += 5
            elif success_rate > 0.90:
                score += 4
            elif success_rate > 0.80:
                score += 3
            elif success_rate > 0.70:
                score += 2
            else:
                score += 1
            factors += 1

        # Error rate scoring (lower is better)
        if "error_rate_mean" in self.summary_stats:
            error_rate = self.summary_stats["error_rate_mean"]
            if error_rate < 0.01:
                score += 5
            elif error_rate < 0.05:
                score += 4
            elif error_rate < 0.10:
                score += 3
            elif error_rate < 0.20:
                score += 2
            else:
                score += 1
            factors += 1

        if factors == 0:
            return PerformanceLevel.AVERAGE

        average_score = score / factors

        if average_score >= 4.5:
            return PerformanceLevel.EXCELLENT
        elif average_score >= 3.5:
            return PerformanceLevel.GOOD
        elif average_score >= 2.5:
            return PerformanceLevel.AVERAGE
        elif average_score >= 1.5:
            return PerformanceLevel.POOR
        else:
            return PerformanceLevel.CRITICAL

class PerformanceTracker:
    """Central performance tracking system"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self.agent_profiles: Dict[str, AgentPerformanceProfile] = {}
        self.performance_file = "performance_metrics.json"
        self.max_metrics_per_agent = 1000
        self.auto_save_interval = 300  # 5 minutes

        # Load existing performance data
        self._load_performance_data()

        # Start auto-save thread
        self._start_auto_save()

    def _load_performance_data(self):
        """Load existing performance data from file"""
        try:
            if os.path.exists(self.performance_file):
                with open(self.performance_file, 'r') as f:
                    data = json.load(f)

                for agent_name, profile_data in data.get('agent_profiles', {}).items():
                    profile = AgentPerformanceProfile(
                        agent_name=agent_name,
                        last_updated=datetime.fromisoformat(profile_data['last_updated']) if profile_data.get('last_updated') else None,
                        performance_level=PerformanceLevel(profile_data.get('performance_level', 'average'))
                    )

                    # Load summary stats
                    profile.summary_stats = profile_data.get('summary_stats', {})

                    # Load recent metrics (last 100 to avoid memory issues)
                    metrics_data = profile_data.get('recent_metrics', [])
                    for metric_data in metrics_data[-100:]:
                        metric = PerformanceMetric(
                            name=metric_data['name'],
                            value=metric_data['value'],
                            timestamp=datetime.fromisoformat(metric_data['timestamp']),
                            metric_type=MetricType(metric_data['metric_type']),
                            agent_name=agent_name,
                            context=metric_data.get('context', {})
                        )
                        profile.metrics.append(metric)

                    self.agent_profiles[agent_name] = profile

                print(f"✅ Loaded performance data for {len(self.agent_profiles)} agents")

        except Exception as e:
            print(f"⚠️ Error loading performance data: {e}")

    def _start_auto_save(self):
        """Start background auto-save thread"""
        def auto_save_worker():
            while True:
                time.sleep(self.auto_save_interval)
                try:
                    self.save_performance_data()
                except Exception as e:
                    print(f"❌ Auto-save error: {e}")

        thread = threading.Thread(target=auto_save_worker, daemon=True)
        thread.start()

    def track_metric(self, agent_name: str, metric_name: str, value: Any,
                    metric_type: MetricType = MetricType.CUSTOM,
                    context: Dict[str, Any] = None):
        """Track a performance metric"""

        if context is None:
            context = {}

        # Create metric
        metric = PerformanceMetric(
            name=metric_name,
            value=value,
            timestamp=datetime.now(),
            metric_type=metric_type,
            agent_name=agent_name,
            context=context
        )

        # Get or create agent profile
        if agent_name not in self.agent_profiles:
            self.agent_profiles[agent_name] = AgentPerformanceProfile(agent_name=agent_name)

        profile = self.agent_profiles[agent_name]

        # Add metric to profile
        profile.add_metric(metric)

        # Limit number of metrics per agent
        if len(profile.metrics) > self.max_metrics_per_agent:
            profile.metrics = profile.metrics[-self.max_metrics_per_agent:]

    def track_response_time(self, agent_name: str, operation: str, response_time: float,
                           context: Dict[str, Any] = None):
        """Track response time for an operation"""
        self.track_metric(
            agent_name=agent_name,
            metric_name=f"response_time_{operation}",
            value=response_time,
            metric_type=MetricType.RESPONSE_TIME,
            context=context or {}
        )

    def track_success_rate(self, agent_name: str, operation: str, success: bool,
                          context: Dict[str, Any] = None):
        """Track success/failure of an operation"""
        success_rate = 1.0 if success else 0.0
        self.track_metric(
            agent_name=agent_name,
            metric_name=f"success_rate_{operation}",
            value=success_rate,
            metric_type=MetricType.SUCCESS_RATE,
            context=context or {}
        )

    def track_throughput(self, agent_name: str, operation: str, items_processed: int,
                        time_taken: float, context: Dict[str, Any] = None):
        """Track throughput (items per second)"""
        throughput = items_processed / time_taken if time_taken > 0 else 0
        self.track_metric(
            agent_name=agent_name,
            metric_name=f"throughput_{operation}",
            value=throughput,
            metric_type=MetricType.THROUGHPUT,
            context=context or {}
        )

    def track_error(self, agent_name: str, operation: str, error_type: str = "general",
                   context: Dict[str, Any] = None):
        """Track an error occurrence"""
        self.track_metric(
            agent_name=agent_name,
            metric_name=f"error_{operation}",
            value=1,  # Count of errors
            metric_type=MetricType.ERROR_RATE,
            context=context or {"error_type": error_type}
        )

    def get_agent_performance(self, agent_name: str) -> Optional[AgentPerformanceProfile]:
        """Get performance profile for an agent"""
        return self.agent_profiles.get(agent_name)

    def get_all_performance_profiles(self) -> Dict[str, AgentPerformanceProfile]:
        """Get all performance profiles"""
        return self.agent_profiles.copy()

    def get_system_performance_summary(self) -> Dict[str, Any]:
        """Get overall system performance summary"""
        if not self.agent_profiles:
            return {"status": "no_data"}

        summary = {
            "total_agents": len(self.agent_profiles),
            "performance_distribution": {},
            "top_performers": [],
            "needs_attention": [],
            "timestamp": datetime.now().isoformat()
        }

        # Count performance levels
        level_counts = defaultdict(int)
        for profile in self.agent_profiles.values():
            level_counts[profile.performance_level.value] += 1

        summary["performance_distribution"] = dict(level_counts)

        # Sort agents by performance
        sorted_agents = sorted(
            self.agent_profiles.values(),
            key=lambda p: self._performance_score(p.performance_level),
            reverse=True
        )

        # Top performers
        summary["top_performers"] = [
            {
                "agent_name": profile.agent_name,
                "performance_level": profile.performance_level.value,
                "last_updated": profile.last_updated.isoformat() if profile.last_updated else None
            }
            for profile in sorted_agents[:5]
        ]

        # Agents needing attention (poor or critical performance)
        summary["needs_attention"] = [
            {
                "agent_name": profile.agent_name,
                "performance_level": profile.performance_level.value,
                "last_updated": profile.last_updated.isoformat() if profile.last_updated else None
            }
            for profile in sorted_agents
            if profile.performance_level in [PerformanceLevel.POOR, PerformanceLevel.CRITICAL]
        ]

        return summary

    def _performance_score(self, level: PerformanceLevel) -> int:
        """Convert performance level to numeric score for sorting"""
        scores = {
            PerformanceLevel.EXCELLENT: 5,
            PerformanceLevel.GOOD: 4,
            PerformanceLevel.AVERAGE: 3,
            PerformanceLevel.POOR: 2,
            PerformanceLevel.CRITICAL: 1
        }
        return scores.get(level, 3)

    def save_performance_data(self, filename: str = None):
        """Save performance data to file"""
        if filename is None:
            filename = self.performance_file

        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "agent_profiles": {}
            }

            for agent_name, profile in self.agent_profiles.items():
                profile_data = {
                    "last_updated": profile.last_updated.isoformat() if profile.last_updated else None,
                    "performance_level": profile.performance_level.value,
                    "summary_stats": profile.summary_stats,
                    "recent_metrics": [
                        {
                            "name": metric.name,
                            "value": metric.value,
                            "timestamp": metric.timestamp.isoformat(),
                            "metric_type": metric.metric_type.value,
                            "context": metric.context
                        }
                        for metric in profile.metrics[-100:]  # Save last 100 metrics
                    ]
                }
                data["agent_profiles"][agent_name] = profile_data

            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)

            print(f"✅ Performance data saved to {filename}")

        except Exception as e:
            print(f"❌ Error saving performance data: {e}")

    def cleanup_old_metrics(self, days_to_keep: int = 30):
        """Clean up old metrics to save space"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        for profile in self.agent_profiles.values():
            original_count = len(profile.metrics)
            profile.metrics = [
                metric for metric in profile.metrics
                if metric.timestamp > cutoff_date
            ]

            if len(profile.metrics) != original_count:
                profile._update_summary_stats()
                removed_count = original_count - len(profile.metrics)
                print(f"🧹 Cleaned up {removed_count} old metrics for {profile.agent_name}")

# Global performance tracker instance
performance_tracker = PerformanceTracker()

# Convenience functions for easy performance tracking
def track_response_time(agent_name: str, operation: str, response_time: float, context: Dict[str, Any] = None):
    """Convenience function to track response time"""
    performance_tracker.track_response_time(agent_name, operation, response_time, context)

def track_success(agent_name: str, operation: str, success: bool, context: Dict[str, Any] = None):
    """Convenience function to track success/failure"""
    performance_tracker.track_success_rate(agent_name, operation, success, context)

def track_throughput(agent_name: str, operation: str, items_processed: int, time_taken: float, context: Dict[str, Any] = None):
    """Convenience function to track throughput"""
    performance_tracker.track_throughput(agent_name, operation, items_processed, time_taken, context)

def track_error(agent_name: str, operation: str, error_type: str = "general", context: Dict[str, Any] = None):
    """Convenience function to track errors"""
    performance_tracker.track_error(agent_name, operation, error_type, context)

def get_performance_summary(agent_name: str = None):
    """Get performance summary"""
    if agent_name:
        profile = performance_tracker.get_agent_performance(agent_name)
        return profile.summary_stats if profile else {}
    else:
        return performance_tracker.get_system_performance_summary()

if __name__ == "__main__":
    # Test the performance tracking system
    print("🧪 Testing Performance Tracking System")
    print("=" * 45)

    # Simulate some performance data
    test_agents = ["content_agent", "trading_agent", "website_agent"]

    for agent in test_agents:
        # Response time metrics
        for i in range(10):
            response_time = 0.1 + (i * 0.05) + (0.1 if i % 3 == 0 else 0)  # Simulate some variance
            track_response_time(agent, "process_request", response_time, {"request_id": f"req_{i}"})

        # Success rate metrics
        for i in range(20):
            success = i % 5 != 0  # 80% success rate
            track_success(agent, "data_processing", success, {"batch_size": 100})

        # Error tracking
        for i in range(3):
            track_error(agent, "api_call", "timeout", {"endpoint": "/api/data"})

    # Save performance data
    performance_tracker.save_performance_data()

    # Get performance summaries
    print("\n📊 Performance Summaries:")
    for agent in test_agents:
        profile = performance_tracker.get_agent_performance(agent)
        if profile:
            print(f"\n{agent.upper()}:")
            print(f"  Performance Level: {profile.performance_level.value}")
            print(f"  Metrics Count: {len(profile.metrics)}")
            print(f"  Summary Stats: {profile.summary_stats}")

    # Get system summary
    system_summary = performance_tracker.get_system_performance_summary()
    print("\n🌐 SYSTEM SUMMARY:")
    print(f"  Total Agents: {system_summary['total_agents']}")
    print(f"  Performance Distribution: {system_summary['performance_distribution']}")
    print(f"  Top Performers: {[p['agent_name'] for p in system_summary['top_performers']]}")
    print(f"  Needs Attention: {[p['agent_name'] for p in system_summary['needs_attention']]}")

    print("\n✅ Performance tracking system test complete!")
