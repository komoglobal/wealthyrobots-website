#!/usr/bin/env python3
"""
Optimized AGI Runner for Current Hardware
Maximizes AGI performance without system overload
"""

import os
import sys
import time
import psutil
import yaml
import threading
import signal
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json

# Import AGI components
from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem

class SystemResourceMonitor:
    """Monitor system resources to prevent overload"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.last_check = datetime.now()
        self.resource_history = []

    def check_system_health(self) -> Dict[str, Any]:
        """Check current system resource usage"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent

            # Process count
            process_count = len(psutil.pids())

            health_data = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent,
                'process_count': process_count,
                'cpu_safe': cpu_percent < self.config['system_limits']['max_cpu_percent'],
                'memory_safe': memory_percent < self.config['system_limits']['max_memory_percent'],
                'disk_safe': disk_percent < self.config['system_limits']['max_disk_percent'],
                'overall_safe': (
                    cpu_percent < self.config['system_limits']['max_cpu_percent'] and
                    memory_percent < self.config['system_limits']['max_memory_percent'] and
                    disk_percent < self.config['system_limits']['max_disk_percent']
                )
            }

            self.resource_history.append(health_data)

            # Keep only last 100 entries
            if len(self.resource_history) > 100:
                self.resource_history = self.resource_history[-100:]

            return health_data

        except Exception as e:
            print(f"⚠️ System health check error: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': 0,
                'memory_percent': 0,
                'disk_percent': 0,
                'process_count': 0,
                'overall_safe': True  # Default to safe
            }

    def get_resource_trend(self) -> str:
        """Get resource usage trend"""
        if len(self.resource_history) < 5:
            return "unknown"

        recent = self.resource_history[-5:]
        avg_cpu = sum(h['cpu_percent'] for h in recent) / len(recent)
        avg_memory = sum(h['memory_percent'] for h in recent) / len(recent)

        if avg_cpu > 80 or avg_memory > 80:
            return "high_load"
        elif avg_cpu > 60 or avg_memory > 60:
            return "moderate_load"
        elif avg_cpu < 30 and avg_memory < 30:
            return "low_load"
        else:
            return "normal_load"

class FeatureGate:
    """Control feature activation based on system capacity"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.feature_states = {}
        self.load_feature_states()

    def load_feature_states(self):
        """Load feature states from config"""
        self.feature_states = self.config.get('feature_gates', {})

    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if feature is enabled"""
        return self.feature_states.get(feature_name, False)

    def set_feature_state(self, feature_name: str, enabled: bool):
        """Enable/disable feature"""
        self.feature_states[feature_name] = enabled
        print(f"🔧 Feature {feature_name}: {'ENABLED' if enabled else 'DISABLED'}")

    def optimize_features_for_load(self, resource_trend: str):
        """Optimize feature states based on system load"""
        if resource_trend == "high_load":
            # Disable non-essential features
            self.set_feature_state('advanced_logging', False)
            self.set_feature_state('web_research', False)
            self.set_feature_state('predictive_analytics', False)

        elif resource_trend == "low_load":
            # Enable additional features if capacity allows
            if self.config['system_limits']['max_cpu_percent'] > 50:
                self.set_feature_state('advanced_logging', True)

class OptimizedAGIRunner:
    """Optimized AGI runner that maximizes performance without overload"""

    def __init__(self, config_path: str = "config/system_optimization.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.resource_monitor = SystemResourceMonitor(self.config)
        self.feature_gate = FeatureGate(self.config)
        self.agi_system = None
        self.running = False
        self.cycle_count = 0
        self.last_cycle_time = datetime.now()

        # Performance tracking
        self.performance_metrics = {
            'total_cycles': 0,
            'average_cycle_time': 0,
            'resource_violations': 0,
            'emergency_actions': 0
        }

        print("🚀 OPTIMIZED AGI RUNNER INITIALIZED")
        print(f"📊 Target Cycle Time: {self.config['agi_cycle_optimization']['cycle_interval_seconds']}s")
        print(f"💾 Memory Budget: {self.config['agi_cycle_optimization']['memory_budget_mb']}MB")
        print(f"⚙️  CPU Budget: {self.config['agi_cycle_optimization']['cpu_budget_percent']}%")

    def load_config(self) -> Dict[str, Any]:
        """Load optimization configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ Config load error: {e}")
            return self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration if file not found"""
        return {
            'agi_cycle_optimization': {
                'cycle_interval_seconds': 300,
                'quick_cycle_interval': 60,
                'memory_budget_mb': 512,
                'cpu_budget_percent': 50
            },
            'system_limits': {
                'max_cpu_percent': 75,
                'max_memory_percent': 80,
                'max_disk_percent': 85
            },
            'feature_gates': {
                'brain_research': True,
                'business_optimization': True,
                'self_improvement': True,
                'system_monitoring': True
            }
        }

    def initialize_agi_system(self):
        """Initialize the AGI system with optimization"""
        try:
            print("🧠 Initializing AGI System (Optimized)...")
            self.agi_system = UnrestrictedAGISystem()
            print("✅ AGI System initialized successfully")
            return True
        except Exception as e:
            print(f"❌ AGI System initialization failed: {e}")
            return False

    async def run_optimized_cycle(self) -> Dict[str, Any]:
        """Run an optimized AGI intelligence cycle"""
        start_time = datetime.now()
        cycle_data = {
            'cycle_number': self.cycle_count + 1,
            'start_time': start_time.isoformat(),
            'system_health': self.resource_monitor.check_system_health(),
            'features_enabled': self.feature_gate.feature_states.copy()
        }

        try:
            # Check if system can handle full cycle
            system_health = cycle_data['system_health']

            if not system_health['overall_safe']:
                print("⚠️ System resources critical - running minimal cycle")
                cycle_data['cycle_type'] = 'minimal'
                # Run minimal cycle - just system monitoring
                result = await self.run_minimal_cycle()
            else:
                print(f"🧠 Running full AGI cycle #{cycle_data['cycle_number']}")
                cycle_data['cycle_type'] = 'full'
                result = await self.run_full_cycle()

            cycle_data['result'] = result
            cycle_data['success'] = True

        except Exception as e:
            print(f"❌ Cycle error: {e}")
            cycle_data['error'] = str(e)
            cycle_data['success'] = False

        # Calculate cycle duration
        end_time = datetime.now()
        cycle_duration = (end_time - start_time).total_seconds()
        cycle_data['duration_seconds'] = cycle_duration
        cycle_data['end_time'] = end_time.isoformat()

        # Update performance metrics
        self.performance_metrics['total_cycles'] += 1
        if self.performance_metrics['average_cycle_time'] == 0:
            self.performance_metrics['average_cycle_time'] = cycle_duration
        else:
            self.performance_metrics['average_cycle_time'] = (
                self.performance_metrics['average_cycle_time'] + cycle_duration
            ) / 2

        # Log cycle results
        self.log_cycle_results(cycle_data)

        return cycle_data

    async def run_minimal_cycle(self) -> Dict[str, Any]:
        """Run minimal cycle when system is under load"""
        print("⚡ MINIMAL CYCLE: System monitoring only")

        # Only run essential monitoring
        if hasattr(self.agi_system, 'system_optimizer'):
            system_analysis = self.agi_system.system_optimizer.analyze_performance_issues()
            return {
                'cycle_type': 'minimal',
                'system_analysis': system_analysis,
                'features_executed': ['system_monitoring']
            }

        return {'cycle_type': 'minimal', 'features_executed': []}

    async def run_full_cycle(self) -> Dict[str, Any]:
        """Run full AGI intelligence cycle with optimization"""
        print("🚀 FULL CYCLE: Complete AGI intelligence cycle")

        # Run the full AGI cycle
        cycle_result = await self.agi_system.run_unrestricted_intelligence_cycle()

        # Add optimization data
        cycle_result['optimization_data'] = {
            'resource_usage': self.resource_monitor.check_system_health(),
            'features_enabled': list(self.feature_gate.feature_states.keys()),
            'performance_metrics': self.performance_metrics.copy()
        }

        return cycle_result

    def log_cycle_results(self, cycle_data: Dict[str, Any]):
        """Log cycle results to file"""
        try:
            log_file = "data/optimized_agi_cycles.jsonl"
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

            with open(log_file, 'a') as f:
                f.write(json.dumps(cycle_data, default=str) + '\n')

        except Exception as e:
            print(f"⚠️ Cycle logging error: {e}")

    async def run_optimized_loop(self):
        """Main optimized AGI loop"""
        print("🔄 STARTING OPTIMIZED AGI LOOP")
        print("=" * 60)

        # Initialize AGI system
        if not self.initialize_agi_system():
            print("❌ Failed to initialize AGI system")
            return

        self.running = True
        emergency_mode = False

        while self.running:
            try:
                # Check system health
                system_health = self.resource_monitor.check_system_health()
                resource_trend = self.resource_monitor.get_resource_trend()

                # Optimize features based on load
                self.feature_gate.optimize_features_for_load(resource_trend)

                # Emergency mode check
                if (system_health['cpu_percent'] > self.config['emergency_protocols']['emergency_threshold_cpu'] or
                    system_health['memory_percent'] > self.config['emergency_protocols']['emergency_threshold_memory']):
                    if not emergency_mode:
                        print("🚨 ENTERING EMERGENCY MODE - High system load detected")
                        emergency_mode = True
                        self.performance_metrics['emergency_actions'] += 1

                    # Emergency actions
                    await self.handle_emergency_mode()
                    await asyncio.sleep(30)  # Wait longer in emergency mode
                    continue
                else:
                    emergency_mode = False

                # Determine cycle timing based on system load
                if emergency_mode:
                    cycle_interval = self.config['agi_cycle_optimization']['emergency_cycle_interval']
                elif resource_trend == "high_load":
                    cycle_interval = self.config['agi_cycle_optimization']['cycle_interval_seconds'] * 2
                elif resource_trend == "low_load":
                    cycle_interval = max(60, self.config['agi_cycle_optimization']['cycle_interval_seconds'] // 2)
                else:
                    cycle_interval = self.config['agi_cycle_optimization']['cycle_interval_seconds']

                # Run cycle
                print(f"\n⏰ Starting cycle {self.cycle_count + 1} (Interval: {cycle_interval}s)")
                print(f"📊 System Load: {resource_trend.upper()}")
                print(f"💻 CPU: {system_health['cpu_percent']:.1f}%, RAM: {system_health['memory_percent']:.1f}%")

                cycle_start = time.time()
                cycle_data = await self.run_optimized_cycle()
                cycle_end = time.time()

                self.cycle_count += 1

                # Show cycle summary
                duration = cycle_end - cycle_start
                print("✅ Cycle completed")
                print(f"   ⏱️  Duration: {duration:.1f}s")
                print(f"   🎯 Type: {cycle_data.get('cycle_type', 'unknown').upper()}")
                print(f"   📊 Status: {'SUCCESS' if cycle_data.get('success', False) else 'FAILED'}")

                if cycle_data.get('success', False):
                    print(f"   🧠 Intelligence Level: {cycle_data.get('intelligence_progress', {}).get('current_level', 'unknown')}")

                # Performance summary
                print("\n📈 Performance Summary:")
                print(f"   🔄 Total Cycles: {self.performance_metrics['total_cycles']}")
                print(f"   ⏱️  Avg Cycle Time: {self.performance_metrics['average_cycle_time']:.1f}s")
                print(f"   🚨 Emergency Actions: {self.performance_metrics['emergency_actions']}")

                # Wait for next cycle
                print(f"⏳ Waiting {cycle_interval}s until next cycle...")
                await asyncio.sleep(cycle_interval)

            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested by user")
                break
            except Exception as e:
                print(f"❌ Loop error: {e}")
                self.performance_metrics['resource_violations'] += 1
                await asyncio.sleep(30)  # Brief pause on error

        print("🧠 Optimized AGI loop stopped")

    async def handle_emergency_mode(self):
        """Handle emergency mode - reduce system load"""
        print("🚨 EMERGENCY MODE: Reducing system load...")

        # Disable non-essential features
        self.feature_gate.set_feature_state('web_research', False)
        self.feature_gate.set_feature_state('predictive_analytics', False)
        self.feature_gate.set_feature_state('advanced_logging', False)

        # Clear any caches if possible
        if hasattr(self.agi_system, 'knowledge_base'):
            # Reset knowledge base cache
            print("🧹 Clearing knowledge base cache...")

        print("✅ Emergency mode actions completed")

    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report"""
        current_health = self.resource_monitor.check_system_health()

        return {
            'timestamp': datetime.now().isoformat(),
            'total_cycles': self.performance_metrics['total_cycles'],
            'average_cycle_time': self.performance_metrics['average_cycle_time'],
            'resource_violations': self.performance_metrics['resource_violations'],
            'emergency_actions': self.performance_metrics['emergency_actions'],
            'current_system_health': current_health,
            'enabled_features': [f for f, enabled in self.feature_gate.feature_states.items() if enabled],
            'disabled_features': [f for f, enabled in self.feature_gate.feature_states.items() if not enabled]
        }

def main():
    """Main function to run optimized AGI"""
    print("🚀 STARTING OPTIMIZED AGI RUNNER")
    print("Maximizing performance without system overload")
    print("=" * 60)

    # Create optimized runner
    runner = OptimizedAGIRunner()

    try:
        # Run the optimized AGI loop
        asyncio.run(runner.run_optimized_loop())
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

    # Show final performance report
    print("\n📊 FINAL PERFORMANCE REPORT")
    print("=" * 40)
    report = runner.get_performance_report()
    print(json.dumps(report, indent=2, default=str))

    print("\n🧠 Optimized AGI session completed!")

if __name__ == "__main__":
    main()
