#!/usr/bin/env python3
"""
Process Optimization System
Intelligent process pooling and lifecycle management
"""

import os
import psutil
import time
import signal
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading
import json
from pathlib import Path
import resource
import multiprocessing

class ProcessOptimizer:
    def __init__(self, workspace_path: str = "/home/ubuntu/wealthyrobot"):
        self.workspace_path = Path(workspace_path)
        self.process_pool = {}
        self.process_limits = {
            "max_python_processes": 10,
            "max_total_processes": 50,
            "max_memory_percent": 70,  # Max 70% of system memory
            "max_cpu_percent": 80,     # Max 80% CPU usage
            "process_timeout": 3600,   # 1 hour max runtime
            "memory_limit_mb": 500     # 500MB per process
        }

        self.monitoring_active = False
        self.optimization_stats = {
            "processes_killed": 0,
            "memory_freed_mb": 0,
            "cpu_optimized": 0,
            "processes_pooled": 0
        }

        print("⚙️ PROCESS OPTIMIZER INITIALIZED")
        print("=" * 50)

    def analyze_current_processes(self) -> Dict[str, any]:
        """Analyze current system processes"""
        print("🔍 ANALYZING CURRENT PROCESSES...")

        process_info = {
            "python_processes": [],
            "high_memory_processes": [],
            "high_cpu_processes": [],
            "idle_processes": [],
            "total_processes": 0,
            "system_memory": {},
            "system_cpu": {}
        }

        try:
            # Get system-wide stats
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)

            process_info["system_memory"] = {
                "total_gb": memory.total / (1024**3),
                "used_gb": memory.used / (1024**3),
                "available_gb": memory.available / (1024**3),
                "percent_used": memory.percent
            }

            process_info["system_cpu"] = {
                "percent_used": cpu_percent,
                "cpu_count": psutil.cpu_count()
            }

            # Analyze individual processes
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info', 'create_time', 'status']):
                try:
                    info = proc.info
                    process_info["total_processes"] += 1

                    # Track Python processes specifically
                    if 'python' in info['name'].lower():
                        python_info = {
                            "pid": info['pid'],
                            "name": info['name'],
                            "cpu_percent": info['cpu_percent'] or 0,
                            "memory_mb": (info['memory_info'].rss / (1024 * 1024)) if info['memory_info'] else 0,
                            "memory_percent": info['memory_percent'] or 0,
                            "status": info['status'],
                            "age_hours": (time.time() - info['create_time']) / 3600 if info['create_time'] else 0
                        }
                        process_info["python_processes"].append(python_info)

                    # Track high resource usage processes
                    if info['memory_percent'] and info['memory_percent'] > 5:  # >5% memory
                        process_info["high_memory_processes"].append({
                            "pid": info['pid'],
                            "name": info['name'],
                            "memory_percent": info['memory_percent'],
                            "memory_mb": (info['memory_info'].rss / (1024 * 1024)) if info['memory_info'] else 0
                        })

                    if info['cpu_percent'] and info['cpu_percent'] > 10:  # >10% CPU
                        process_info["high_cpu_processes"].append({
                            "pid": info['pid'],
                            "name": info['name'],
                            "cpu_percent": info['cpu_percent']
                        })

                    # Track idle processes
                    if info['cpu_percent'] is not None and info['cpu_percent'] < 0.1 and info['status'] == 'sleeping':
                        process_info["idle_processes"].append({
                            "pid": info['pid'],
                            "name": info['name'],
                            "cpu_percent": info['cpu_percent'],
                            "age_hours": (time.time() - info['create_time']) / 3600 if info['create_time'] else 0
                        })

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        except Exception as e:
            print(f"❌ Error analyzing processes: {e}")

        # Sort by resource usage
        process_info["python_processes"].sort(key=lambda x: x['memory_mb'], reverse=True)
        process_info["high_memory_processes"].sort(key=lambda x: x['memory_percent'], reverse=True)
        process_info["high_cpu_processes"].sort(key=lambda x: x['cpu_percent'], reverse=True)

        print(f"📊 Found {len(process_info['python_processes'])} Python processes")
        print(f"🧠 High memory: {len(process_info['high_memory_processes'])} processes")
        print(f"⚡ High CPU: {len(process_info['high_cpu_processes'])} processes")
        print(f"😴 Idle: {len(process_info['idle_processes'])} processes")

        return process_info

    def implement_process_pooling(self):
        """Implement intelligent process pooling"""
        print("🏊 IMPLEMENTING PROCESS POOLING...")

        process_info = self.analyze_current_processes()
        python_processes = process_info["python_processes"]

        if len(python_processes) <= self.process_limits["max_python_processes"]:
            print("✅ Python process count within limits")
            return

        # Identify processes that can be pooled
        pool_candidates = []
        for proc in python_processes[self.process_limits["max_python_processes"]:]:
            # Skip critical processes
            if any(keyword in proc['name'].lower() for keyword in ['autonomous', 'monitor', 'optimizer']):
                continue

            # Check if process is old enough to consider pooling
            if proc['age_hours'] > 1:  # Older than 1 hour
                pool_candidates.append(proc)

        if not pool_candidates:
            print("⚠️ No suitable processes for pooling")
            return

        # Create process pool configuration
        pool_config = {
            "pool_name": f"process_pool_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "max_workers": min(len(pool_candidates), self.process_limits["max_python_processes"]),
            "pooled_processes": pool_candidates[:self.process_limits["max_python_processes"]],
            "pool_strategy": "round_robin",
            "created": datetime.now().isoformat()
        }

        # Save pool configuration
        pool_config_path = self.workspace_path / f"{pool_config['pool_name']}.json"
        with open(pool_config_path, 'w') as f:
            json.dump(pool_config, f, indent=2)

        # Terminate excess processes
        terminated_count = 0
        for proc in pool_candidates[self.process_limits["max_python_processes"]:]:
            try:
                os.kill(proc['pid'], signal.SIGTERM)
                terminated_count += 1
                self.optimization_stats["processes_killed"] += 1
                print(f"🛑 Terminated process {proc['pid']} ({proc['name']})")
                time.sleep(0.1)  # Brief pause between terminations
            except (ProcessLookupError, PermissionError):
                continue

        print(f"✅ Process pooling implemented: {terminated_count} processes terminated")
        print(f"📋 Pool configuration: {pool_config_path}")

        return pool_config

    def optimize_memory_usage(self):
        """Optimize memory usage across processes"""
        print("🧠 OPTIMIZING MEMORY USAGE...")

        process_info = self.analyze_current_processes()
        high_memory_processes = process_info["high_memory_processes"]

        memory_optimized = 0

        # Check system memory usage
        system_memory = process_info["system_memory"]
        if system_memory["percent_used"] > self.process_limits["max_memory_percent"]:
            print(f"⚠️ High system memory usage: {system_memory['percent_used']:.1f}%")

            # Kill high memory processes
            for proc in high_memory_processes[:5]:  # Top 5 memory hogs
                if proc["memory_percent"] > 10:  # >10% memory usage
                    try:
                        os.kill(proc['pid'], signal.SIGTERM)
                        memory_optimized += proc["memory_mb"]
                        self.optimization_stats["processes_killed"] += 1
                        self.optimization_stats["memory_freed_mb"] += proc["memory_mb"]
                        print(f"🛑 Killed high-memory process {proc['pid']}: {proc['memory_mb']:.1f} MB")
                        time.sleep(1)  # Wait for cleanup
                    except (ProcessLookupError, PermissionError):
                        continue

        if memory_optimized > 0:
            print(f"💾 Memory freed: {memory_optimized:.1f} MB")
        else:
            print("✅ Memory usage within acceptable limits")

        return memory_optimized

    def optimize_cpu_usage(self):
        """Optimize CPU usage"""
        print("⚡ OPTIMIZING CPU USAGE...")

        process_info = self.analyze_current_processes()
        high_cpu_processes = process_info["high_cpu_processes"]

        cpu_optimized = 0

        # Check system CPU usage
        system_cpu = process_info["system_cpu"]
        if system_cpu["percent_used"] > self.process_limits["max_cpu_percent"]:
            print(f"⚠️ High system CPU usage: {system_cpu['percent_used']:.1f}%")

            # Nice high CPU processes (reduce priority)
            for proc in high_cpu_processes[:3]:  # Top 3 CPU hogs
                try:
                    # Reduce priority (increase nice value)
                    os.system(f"renice +10 -p {proc['pid']} >/dev/null 2>&1")
                    cpu_optimized += 1
                    self.optimization_stats["cpu_optimized"] += 1
                    print(f"🐌 Reduced priority for high-CPU process {proc['pid']}")
                except Exception:
                    continue

        if cpu_optimized > 0:
            print(f"✅ CPU optimization applied to {cpu_optimized} processes")
        else:
            print("✅ CPU usage within acceptable limits")

        return cpu_optimized

    def clean_idle_processes(self):
        """Clean up idle processes"""
        print("😴 CLEANING IDLE PROCESSES...")

        process_info = self.analyze_current_processes()
        idle_processes = process_info["idle_processes"]

        cleaned_count = 0

        for proc in idle_processes:
            # Only clean very old idle processes (>24 hours)
            if proc["age_hours"] > 24:
                try:
                    os.kill(proc['pid'], signal.SIGTERM)
                    cleaned_count += 1
                    self.optimization_stats["processes_killed"] += 1
                    print(f"🧹 Cleaned idle process {proc['pid']} (age: {proc['age_hours']:.1f}h)")
                    time.sleep(0.5)
                except (ProcessLookupError, PermissionError):
                    continue

        if cleaned_count > 0:
            print(f"🧹 Cleaned {cleaned_count} idle processes")
        else:
            print("✅ No old idle processes to clean")

        return cleaned_count

    def implement_resource_limits(self):
        """Implement resource limits for processes"""
        print("📏 IMPLEMENTING RESOURCE LIMITS...")

        # Set system-wide resource limits
        try:
            # Set memory limit
            memory_limit = self.process_limits["memory_limit_mb"] * 1024 * 1024  # Convert to bytes
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

            # Set CPU time limit
            cpu_limit = self.process_limits["process_timeout"]
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))

            print("✅ Resource limits implemented")
            print(f"   🧠 Memory limit: {self.process_limits['memory_limit_mb']} MB")
            print(f"   ⏰ CPU time limit: {self.process_limits['process_timeout']} seconds")

        except Exception as e:
            print(f"⚠️ Could not set resource limits: {e}")

    def start_process_monitoring(self):
        """Start continuous process monitoring"""
        print("👁️ STARTING PROCESS MONITORING...")

        self.monitoring_active = True

        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Periodic optimization
                    self.optimize_memory_usage()
                    self.optimize_cpu_usage()
                    self.clean_idle_processes()

                    # Check if we need to implement pooling
                    process_info = self.analyze_current_processes()
                    if len(process_info["python_processes"]) > self.process_limits["max_python_processes"]:
                        self.implement_process_pooling()

                    time.sleep(300)  # Check every 5 minutes

                except Exception as e:
                    print(f"⚠️ Monitoring error: {e}")
                    time.sleep(60)

        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

        print("✅ Process monitoring started")

    def stop_process_monitoring(self):
        """Stop process monitoring"""
        self.monitoring_active = False
        print("🛑 Process monitoring stopped")

    def create_process_manager_service(self):
        """Create a system service for process management"""
        print("🔧 CREATING PROCESS MANAGER SERVICE...")

        service_content = f'''#!/bin/bash
# Process Manager Service
# Monitors and optimizes system processes

while true; do
    # Run process optimization
    cd /home/ubuntu/wealthyrobot
    python3 process_optimizer.py --monitor-only

    # Wait before next check
    sleep 600  # 10 minutes
done
'''

        service_path = self.workspace_path / "process_manager_service.sh"
        with open(service_path, 'w') as f:
            f.write(service_content)

        # Make executable
        os.chmod(service_path, 0o755)

        print(f"✅ Process manager service created: {service_path}")
        print("   To start: ./process_manager_service.sh &")
        return service_path

    def generate_process_report(self) -> str:
        """Generate comprehensive process optimization report"""
        print("📊 GENERATING PROCESS OPTIMIZATION REPORT...")

        final_analysis = self.analyze_current_processes()

        report = {
            "timestamp": datetime.now().isoformat(),
            "optimization_summary": {
                "processes_killed": self.optimization_stats["processes_killed"],
                "memory_freed_mb": self.optimization_stats["memory_freed_mb"],
                "cpu_optimized": self.optimization_stats["cpu_optimized"],
                "processes_pooled": self.optimization_stats["processes_pooled"]
            },
            "current_state": {
                "total_processes": final_analysis["total_processes"],
                "python_processes": len(final_analysis["python_processes"]),
                "high_memory_processes": len(final_analysis["high_memory_processes"]),
                "high_cpu_processes": len(final_analysis["high_cpu_processes"]),
                "idle_processes": len(final_analysis["idle_processes"])
            },
            "system_resources": {
                "memory": final_analysis["system_memory"],
                "cpu": final_analysis["system_cpu"]
            },
            "recommendations": self._generate_process_recommendations(final_analysis)
        }

        report_path = self.workspace_path / f"process_optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📄 Process optimization report: {report_path}")
        return str(report_path)

    def _generate_process_recommendations(self, analysis: Dict[str, any]) -> List[str]:
        """Generate process optimization recommendations"""
        recommendations = []

        if len(analysis["python_processes"]) > self.process_limits["max_python_processes"]:
            recommendations.append(f"Reduce Python processes from {len(analysis['python_processes'])} to {self.process_limits['max_python_processes']}")

        if analysis["system_memory"]["percent_used"] > self.process_limits["max_memory_percent"]:
            recommendations.append(f"Memory usage ({analysis['system_memory']['percent_used']}%) exceeds limit ({self.process_limits['max_memory_percent']}%)")

        if analysis["system_cpu"]["percent_used"] > self.process_limits["max_cpu_percent"]:
            recommendations.append(f"CPU usage ({analysis['system_cpu']['percent_used']}%) exceeds limit ({self.process_limits['max_cpu_percent']}%)")

        if len(analysis["idle_processes"]) > 10:
            recommendations.append(f"Clean up {len(analysis['idle_processes'])} idle processes")

        if not recommendations:
            recommendations.append("System process usage is within acceptable limits")

        return recommendations

    def run_full_optimization(self):
        """Run complete process optimization suite"""
        print("🚀 RUNNING FULL PROCESS OPTIMIZATION")
        print("=" * 60)

        start_time = time.time()

        # Implement resource limits
        self.implement_resource_limits()

        # Run optimization phases
        self.implement_process_pooling()
        memory_optimized = self.optimize_memory_usage()
        cpu_optimized = self.optimize_cpu_usage()
        idle_cleaned = self.clean_idle_processes()

        # Create monitoring service
        self.create_process_manager_service()

        # Generate report
        report_path = self.generate_process_report()

        duration = time.time() - start_time

        print("\\n📊 PROCESS OPTIMIZATION COMPLETE!")
        print("=" * 50)
        print(f"🕐 Duration: {duration:.1f} seconds")
        print(f"💾 Memory freed: {self.optimization_stats['memory_freed_mb']:.1f} MB")
        print(f"⚡ CPU optimized: {self.optimization_stats['cpu_optimized']} processes")
        print(f"🧹 Processes cleaned: {self.optimization_stats['processes_killed']} processes")
        print(f"📄 Report: {report_path}")

        # Start monitoring
        self.start_process_monitoring()
        print("👁️ Continuous monitoring started")

def main():
    """Main execution function"""
    optimizer = ProcessOptimizer()

    if len(os.sys.argv) > 1 and os.sys.argv[1] == "--monitor-only":
        # Monitoring mode
        optimizer.start_process_monitoring()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            optimizer.stop_process_monitoring()
    else:
        # Full optimization mode
        optimizer.run_full_optimization()

if __name__ == "__main__":
    main()
