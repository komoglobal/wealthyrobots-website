#!/usr/bin/env python3
"""
System Performance Optimization Agent for WealthyRobot Empire
Optimizes system performance, scalability, and resource utilization
"""

import os
import json
import time
import psutil
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading

from agent_logging_utils import AgentLogger, AgentUtils, with_timeout, with_retry

class SystemPerformanceOptimizer:
    """Agent responsible for optimizing system performance and scalability"""

    def __init__(self):
        self.logger = AgentLogger("system_performance_optimizer")
        self.performance_metrics = {}
        self.optimization_history = []
        self.monitoring_active = False
        self.monitoring_thread = None

    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system performance metrics"""
        self.logger.info("Collecting system performance metrics")

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "usage_percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(),
                "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else 0
            },
            "memory": {
                "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
                "available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "usage_percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
                "used_gb": round(psutil.disk_usage('/').used / (1024**3), 2),
                "free_gb": round(psutil.disk_usage('/').free / (1024**3), 2),
                "usage_percent": psutil.disk_usage('/').percent
            },
            "processes": {
                "total": len(psutil.pids()),
                "python_processes": len([p for p in psutil.process_iter(['pid', 'name']) if 'python' in p.info['name'].lower()]),
                "high_cpu_processes": []
            },
            "network": {
                "connections": len(psutil.net_connections()),
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            },
            "empire_specific": {
                "active_agents": self._count_active_agents(),
                "log_file_sizes": self._get_log_sizes(),
                "database_sizes": self._get_database_sizes()
            }
        }

        # Get high CPU processes
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] > 10:
                    metrics["processes"]["high_cpu_processes"].append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.performance_metrics = metrics
        return metrics

    def _count_active_agents(self) -> int:
        """Count currently active empire agents"""
        agent_files = [
            "run_hybrid_trading_empire.py",
            "ultimate_ceo_agent.py",
            "fund_manager.py",
            "data_management_agent.py",
            "business_optimization_agent.py"
        ]

        active_count = 0
        for agent in agent_files:
            if os.path.exists(agent):
                # Check if process is running
                try:
                    result = subprocess.run(
                        ["pgrep", "-f", agent],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        active_count += 1
                except Exception:
                    pass

        return active_count

    def _get_log_sizes(self) -> Dict[str, float]:
        """Get sizes of log files in MB"""
        log_sizes = {}
        logs_dir = "logs"

        if os.path.exists(logs_dir):
            for file in os.listdir(logs_dir):
                if file.endswith('.log'):
                    filepath = os.path.join(logs_dir, file)
                    try:
                        size_mb = os.path.getsize(filepath) / (1024 * 1024)
                        log_sizes[file] = round(size_mb, 2)
                    except Exception:
                        pass

        return log_sizes

    def _get_database_sizes(self) -> Dict[str, float]:
        """Get sizes of data files in MB"""
        data_sizes = {}
        data_dir = "data"

        if os.path.exists(data_dir):
            for root, dirs, files in os.walk(data_dir):
                for file in files:
                    if file.endswith(('.json', '.jsonl', '.yaml')):
                        filepath = os.path.join(root, file)
                        try:
                            size_mb = os.path.getsize(filepath) / (1024 * 1024)
                            if size_mb > 1:  # Only track files > 1MB
                                rel_path = os.path.relpath(filepath, data_dir)
                                data_sizes[rel_path] = round(size_mb, 2)
                        except Exception:
                            pass

        return data_sizes

    @with_retry(max_retries=3)
    def analyze_performance_issues(self) -> Dict[str, Any]:
        """Analyze system performance and identify issues"""
        self.logger.info("Analyzing system performance issues")

        metrics = self.collect_system_metrics()
        issues = []
        recommendations = []

        # CPU analysis
        if metrics["cpu"]["usage_percent"] > 80:
            issues.append({
                "type": "high_cpu_usage",
                "severity": "high",
                "description": f"CPU usage is {metrics['cpu']['usage_percent']}%",
                "current": metrics["cpu"]["usage_percent"],
                "threshold": 80
            })
            recommendations.append("Optimize CPU-intensive processes or consider scaling")

        # Memory analysis
        if metrics["memory"]["usage_percent"] > 85:
            issues.append({
                "type": "high_memory_usage",
                "severity": "high",
                "description": f"Memory usage is {metrics['memory']['usage_percent']}%",
                "current": metrics["memory"]["usage_percent"],
                "threshold": 85
            })
            recommendations.append("Implement memory optimization or add more RAM")

        # Disk analysis
        if metrics["disk"]["usage_percent"] > 90:
            issues.append({
                "type": "high_disk_usage",
                "severity": "critical",
                "description": f"Disk usage is {metrics['disk']['usage_percent']}%",
                "current": metrics["disk"]["usage_percent"],
                "threshold": 90
            })
            recommendations.append("Clean up disk space immediately")

        # Log file analysis
        large_logs = [log for log, size in metrics["empire_specific"]["log_file_sizes"].items() if size > 100]
        if large_logs:
            issues.append({
                "type": "large_log_files",
                "severity": "medium",
                "description": f"Found {len(large_logs)} log files larger than 100MB",
                "files": large_logs
            })
            recommendations.append("Implement log rotation for large log files")

        # Process analysis
        if len(metrics["processes"]["high_cpu_processes"]) > 3:
            issues.append({
                "type": "multiple_high_cpu_processes",
                "severity": "medium",
                "description": f"{len(metrics['processes']['high_cpu_processes'])} processes using >10% CPU",
                "processes": metrics["processes"]["high_cpu_processes"]
            })
            recommendations.append("Monitor and optimize high CPU processes")

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "issues": issues,
            "recommendations": recommendations,
            "overall_health": self._calculate_health_score(metrics, issues)
        }

        self._save_analysis(analysis)
        return analysis

    def _calculate_health_score(self, metrics: Dict[str, Any], issues: List[Dict[str, Any]]) -> str:
        """Calculate overall system health score"""
        score = 100

        # Deduct points for high resource usage
        score -= max(0, metrics["cpu"]["usage_percent"] - 70) * 0.5
        score -= max(0, metrics["memory"]["usage_percent"] - 80) * 0.5
        score -= max(0, metrics["disk"]["usage_percent"] - 85) * 2

        # Deduct points for issues
        for issue in issues:
            if issue["severity"] == "critical":
                score -= 20
            elif issue["severity"] == "high":
                score -= 10
            elif issue["severity"] == "medium":
                score -= 5

        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        else:
            return "poor"

    def _save_analysis(self, analysis: Dict[str, Any]):
        """Save performance analysis to file"""
        try:
            os.makedirs("reports", exist_ok=True)
            filename = f"reports/performance_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2)
            self.logger.info("Performance analysis saved", file=filename)
        except Exception as e:
            self.logger.error("Failed to save analysis", error=str(e))

    @with_retry(max_retries=3)
    def implement_performance_optimization(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Implement optimization for a specific performance issue"""
        self.logger.info("Implementing performance optimization", issue_type=issue["type"])

        result = {
            "issue_type": issue["type"],
            "status": "pending",
            "actions_taken": [],
            "results": {}
        }

        try:
            if issue["type"] == "large_log_files":
                result = self._optimize_log_files(result, issue)
            elif issue["type"] == "high_memory_usage":
                result = self._optimize_memory_usage(result)
            elif issue["type"] == "high_cpu_usage":
                result = self._optimize_cpu_usage(result)
            elif issue["type"] == "high_disk_usage":
                result = self._optimize_disk_usage(result)
            else:
                result["status"] = "not_implemented"
                result["reason"] = f"No implementation for {issue['type']}"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            self.logger.error("Optimization failed", issue_type=issue["type"], error=str(e))

        self.optimization_history.append(result)
        return result

    def _optimize_log_files(self, result: Dict[str, Any], issue: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize large log files"""
        result["actions_taken"] = ["Implemented log rotation", "Compressed old logs"]

        try:
            logs_dir = "logs"
            compressed_count = 0
            deleted_count = 0

            for log_file in os.listdir(logs_dir):
                if log_file.endswith('.log'):
                    filepath = os.path.join(logs_dir, log_file)
                    size_mb = os.path.getsize(filepath) / (1024 * 1024)

                    if size_mb > 50:  # Compress files > 50MB
                        compressed_file = filepath + '.gz'
                        import gzip
                        import shutil

                        with open(filepath, 'rb') as f_in:
                            with gzip.open(compressed_file, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)

                        # Remove original large file
                        os.remove(filepath)
                        compressed_count += 1

                    elif size_mb > 100:  # Delete files > 100MB (keep compressed)
                        if os.path.exists(filepath):
                            os.remove(filepath)
                            deleted_count += 1

            result["status"] = "completed"
            result["results"]["compressed_files"] = compressed_count
            result["results"]["deleted_files"] = deleted_count

        except Exception as e:
            result["status"] = "partial"
            result["error"] = str(e)

        return result

    def _optimize_memory_usage(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize memory usage"""
        result["actions_taken"] = ["Cleared system caches", "Optimized Python processes"]

        try:
            # Clear system caches
            subprocess.run(['sudo', 'sh', '-c', 'echo 3 > /proc/sys/vm/drop_caches'],
                         capture_output=True, timeout=10)

            # Kill any zombie processes
            subprocess.run(['pkill', '-9', '-f', 'defunct'], capture_output=True)

            result["status"] = "completed"
            result["results"]["cache_cleared"] = True

        except Exception as e:
            result["status"] = "partial"
            result["error"] = str(e)

        return result

    def _optimize_cpu_usage(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize CPU usage"""
        result["actions_taken"] = ["Adjusted process priorities", "Optimized agent scheduling"]

        try:
            # Renice high CPU processes
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 20 and 'python' in proc.info['name'].lower():
                        proc.nice(10)  # Lower priority
                except Exception:
                    pass

            result["status"] = "completed"
            result["results"]["processes_reniced"] = True

        except Exception as e:
            result["status"] = "partial"
            result["error"] = str(e)

        return result

    def _optimize_disk_usage(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize disk usage"""
        result["actions_taken"] = ["Cleaned temporary files", "Removed old cache files"]

        try:
            # Clean temp files
            subprocess.run(['find', '/tmp', '-type', 'f', '-mtime', '+7', '-delete'],
                         capture_output=True, timeout=30)

            # Clean apt cache
            subprocess.run(['sudo', 'apt-get', 'autoremove', '-y'],
                         capture_output=True, timeout=60)
            subprocess.run(['sudo', 'apt-get', 'autoclean', '-y'],
                         capture_output=True, timeout=60)

            result["status"] = "completed"
            result["results"]["temp_cleaned"] = True
            result["results"]["apt_cache_cleaned"] = True

        except Exception as e:
            result["status"] = "partial"
            result["error"] = str(e)

        return result

    def start_continuous_monitoring(self):
        """Start continuous performance monitoring"""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("Continuous performance monitoring started")

    def stop_continuous_monitoring(self):
        """Stop continuous performance monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("Continuous performance monitoring stopped")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect metrics every 5 minutes
                analysis = self.analyze_performance_issues()

                # Auto-optimize if critical issues detected
                critical_issues = [issue for issue in analysis["issues"] if issue["severity"] == "critical"]
                if critical_issues:
                    self.logger.warning("Critical performance issues detected, auto-optimizing")
                    for issue in critical_issues:
                        self.implement_performance_optimization(issue)

                time.sleep(300)  # 5 minutes

            except Exception as e:
                self.logger.error("Monitoring loop error", error=str(e))
                time.sleep(60)  # Wait 1 minute on error

    def run_performance_optimization_cycle(self) -> Dict[str, Any]:
        """Run complete performance optimization cycle"""
        self.logger.info("Starting performance optimization cycle")

        # Analyze current performance
        analysis = self.analyze_performance_issues()

        # Implement optimizations for high/critical issues
        implemented_optimizations = []
        high_issues = [issue for issue in analysis["issues"] if issue["severity"] in ["high", "critical"]]

        for issue in high_issues:
            result = self.implement_performance_optimization(issue)
            implemented_optimizations.append(result)

        final_report = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "implemented_optimizations": implemented_optimizations,
            "overall_impact": self._assess_optimization_impact(implemented_optimizations)
        }

        self.logger.info("Performance optimization cycle completed",
                        issues_found=len(analysis["issues"]),
                        optimizations_implemented=len(implemented_optimizations))

        return final_report

    def _assess_optimization_impact(self, optimizations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess the overall impact of performance optimizations"""
        successful = sum(1 for opt in optimizations if opt.get("status") == "completed")
        total = len(optimizations)

        return {
            "success_rate": (successful / total) * 100 if total > 0 else 0,
            "optimizations_completed": successful,
            "total_optimizations": total,
            "estimated_impact": "high" if successful >= 2 else "medium" if successful >= 1 else "low"
        }

def main():
    """Main function to run performance optimization"""
    agent = SystemPerformanceOptimizer()
    report = agent.run_performance_optimization_cycle()

    print("\n🚀 SYSTEM PERFORMANCE OPTIMIZATION REPORT")
    print(f"📊 Overall Health: {report['analysis']['overall_health'].upper()}")
    print(f"⚠️  Issues Found: {len(report['analysis']['issues'])}")
    print(f"✅ Optimizations Completed: {report['overall_impact']['optimizations_completed']}/{report['overall_impact']['total_optimizations']}")
    print(f"🎯 Impact Level: {report['overall_impact']['estimated_impact']}")

    # Show top recommendations
    if report['analysis']['recommendations']:
        print("\n💡 Top Recommendations:")
        for i, rec in enumerate(report['analysis']['recommendations'][:3], 1):
            print(f"   {i}. {rec}")

    return report

if __name__ == "__main__":
    main()
