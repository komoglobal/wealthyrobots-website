#!/usr/bin/env python3
"""
Resource Pooling and Circuit Breaker System for AGI Optimization
=================================================================

Implements resource pooling, circuit breakers, and load balancing for AGI stability.
Provides fault tolerance and resource management capabilities.
"""

import asyncio
import threading
import time
import logging
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import psutil
import os

T = TypeVar('T')

class CircuitBreakerState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    expected_exception: tuple = (Exception,)

@dataclass
class CircuitBreakerMetrics:
    """Metrics for circuit breaker"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    consecutive_failures: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None

class CircuitBreaker:
    """Circuit breaker implementation"""

    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitBreakerState.CLOSED
        self.metrics = CircuitBreakerMetrics()
        self._lock = threading.RLock()
        self.logger = logging.getLogger(f"CircuitBreaker.{name}")

    def __call__(self, func: Callable) -> Callable:
        """Decorator to apply circuit breaker to a function"""
        async def async_wrapper(*args, **kwargs):
            return await self._execute_async(func, *args, **kwargs)

        def sync_wrapper(*args, **kwargs):
            return self._execute_sync(func, *args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    async def _execute_async(self, func: Callable, *args, **kwargs) -> Any:
        """Execute async function with circuit breaker"""
        if not await self._should_allow_request():
            raise Exception(f"Circuit breaker {self.name} is OPEN")

        try:
            result = await func(*args, **kwargs)
            await self._record_success()
            return result
        except self.config.expected_exception as e:
            await self._record_failure()
            raise e

    def _execute_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Execute sync function with circuit breaker"""
        if not self._should_allow_request():
            raise Exception(f"Circuit breaker {self.name} is OPEN")

        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except self.config.expected_exception as e:
            self._record_failure()
            raise e

    async def _should_allow_request(self) -> bool:
        """Determine if request should be allowed"""
        with self._lock:
            if self.state == CircuitBreakerState.CLOSED:
                return True
            elif self.state == CircuitBreakerState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitBreakerState.HALF_OPEN
                    self.logger.info(f"Circuit breaker {self.name} moved to HALF_OPEN")
                    return True
                return False
            elif self.state == CircuitBreakerState.HALF_OPEN:
                return True
            return False

    def _should_allow_request(self) -> bool:
        """Sync version of _should_allow_request"""
        with self._lock:
            if self.state == CircuitBreakerState.CLOSED:
                return True
            elif self.state == CircuitBreakerState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitBreakerState.HALF_OPEN
                    self.logger.info(f"Circuit breaker {self.name} moved to HALF_OPEN")
                    return True
                return False
            elif self.state == CircuitBreakerState.HALF_OPEN:
                return True
            return False

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit"""
        if self.metrics.last_failure_time is None:
            return True

        time_since_failure = time.time() - self.metrics.last_failure_time
        return time_since_failure >= self.config.recovery_timeout

    async def _record_success(self):
        """Record successful request"""
        with self._lock:
            self.metrics.successful_requests += 1
            self.metrics.total_requests += 1
            self.metrics.consecutive_failures = 0
            self.metrics.last_success_time = time.time()

            if self.state == CircuitBreakerState.HALF_OPEN:
                self.state = CircuitBreakerState.CLOSED
                self.logger.info(f"Circuit breaker {self.name} reset to CLOSED")

    def _record_success(self):
        """Sync version of _record_success"""
        with self._lock:
            self.metrics.successful_requests += 1
            self.metrics.total_requests += 1
            self.metrics.consecutive_failures = 0
            self.metrics.last_success_time = time.time()

            if self.state == CircuitBreakerState.HALF_OPEN:
                self.state = CircuitBreakerState.CLOSED
                self.logger.info(f"Circuit breaker {self.name} reset to CLOSED")

    async def _record_failure(self):
        """Record failed request"""
        with self._lock:
            self.metrics.failed_requests += 1
            self.metrics.total_requests += 1
            self.metrics.consecutive_failures += 1
            self.metrics.last_failure_time = time.time()

            if (self.state == CircuitBreakerState.HALF_OPEN or
                self.metrics.consecutive_failures >= self.config.failure_threshold):
                self.state = CircuitBreakerState.OPEN
                self.logger.warning(f"Circuit breaker {self.name} opened due to {self.metrics.consecutive_failures} consecutive failures")

    def _record_failure(self):
        """Sync version of _record_failure"""
        with self._lock:
            self.metrics.failed_requests += 1
            self.metrics.total_requests += 1
            self.metrics.consecutive_failures += 1
            self.metrics.last_failure_time = time.time()

            if (self.state == CircuitBreakerState.HALF_OPEN or
                self.metrics.consecutive_failures >= self.config.failure_threshold):
                self.state = CircuitBreakerState.OPEN
                self.logger.warning(f"Circuit breaker {self.name} opened due to {self.metrics.consecutive_failures} consecutive failures")

    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        with self._lock:
            success_rate = (self.metrics.successful_requests /
                          self.metrics.total_requests) if self.metrics.total_requests > 0 else 0

            return {
                "name": self.name,
                "state": self.state.value,
                "metrics": {
                    "total_requests": self.metrics.total_requests,
                    "successful_requests": self.metrics.successful_requests,
                    "failed_requests": self.metrics.failed_requests,
                    "success_rate": success_rate,
                    "consecutive_failures": self.metrics.consecutive_failures,
                    "last_failure_time": self.metrics.last_failure_time,
                    "last_success_time": self.metrics.last_success_time
                }
            }

@dataclass
class ResourcePoolConfig:
    """Configuration for resource pool"""
    max_resources: int = 10
    min_resources: int = 2
    resource_timeout: float = 30.0
    health_check_interval: float = 60.0

class ResourcePool:
    """Generic resource pool implementation"""

    def __init__(self, name: str, resource_factory: Callable[[], Any],
                 config: ResourcePoolConfig = None):
        self.name = name
        self.resource_factory = resource_factory
        self.config = config or ResourcePoolConfig()

        self.available_resources: List[Any] = []
        self.in_use_resources: Dict[str, Dict[str, Any]] = {}
        self.resource_health: Dict[str, bool] = {}

        self._lock = threading.RLock()
        self._resource_id_counter = 0
        self.logger = logging.getLogger(f"ResourcePool.{name}")

        # Initialize minimum resources
        self._initialize_pool()

    def _initialize_pool(self):
        """Initialize the resource pool"""
        for _ in range(self.config.min_resources):
            try:
                resource = self.resource_factory()
                resource_id = self._get_next_resource_id()
                self.available_resources.append({
                    'id': resource_id,
                    'resource': resource,
                    'created_at': time.time()
                })
                self.resource_health[resource_id] = True
                self.logger.debug(f"Created resource {resource_id}")
            except Exception as e:
                self.logger.error(f"Failed to create initial resource: {e}")

    def acquire_resource(self, timeout: float = None) -> Optional[Any]:
        """Acquire a resource from the pool"""
        timeout = timeout or self.config.resource_timeout

        with self._lock:
            start_time = time.time()

            while time.time() - start_time < timeout:
                # Try to get available resource
                if self.available_resources:
                    resource_info = self.available_resources.pop(0)
                    resource_id = resource_info['id']
                    resource = resource_info['resource']

                    # Health check
                    if self._is_resource_healthy(resource):
                        self.in_use_resources[resource_id] = {
                            'resource': resource,
                            'acquired_at': time.time()
                        }
                        self.logger.debug(f"Acquired resource {resource_id}")
                        return resource
                    else:
                        # Resource is unhealthy, remove it
                        self.resource_health[resource_id] = False
                        self.logger.warning(f"Removed unhealthy resource {resource_id}")

                # Create new resource if under max limit
                if len(self.available_resources) + len(self.in_use_resources) < self.config.max_resources:
                    try:
                        resource = self.resource_factory()
                        resource_id = self._get_next_resource_id()
                        self.in_use_resources[resource_id] = {
                            'resource': resource,
                            'acquired_at': time.time()
                        }
                        self.resource_health[resource_id] = True
                        self.logger.debug(f"Created and acquired new resource {resource_id}")
                        return resource
                    except Exception as e:
                        self.logger.error(f"Failed to create new resource: {e}")

                # Wait a bit before retrying
                time.sleep(0.1)

            self.logger.warning("Resource acquisition timeout")
            return None

    def release_resource(self, resource: Any):
        """Release a resource back to the pool"""
        with self._lock:
            # Find the resource in use
            for resource_id, resource_info in self.in_use_resources.items():
                if resource_info['resource'] is resource:
                    # Move back to available pool
                    self.available_resources.append({
                        'id': resource_id,
                        'resource': resource,
                        'created_at': resource_info.get('created_at', time.time())
                    })
                    del self.in_use_resources[resource_id]
                    self.logger.debug(f"Released resource {resource_id}")
                    return

            self.logger.warning("Attempted to release unknown resource")

    def _is_resource_healthy(self, resource: Any) -> bool:
        """Check if a resource is healthy (override in subclasses)"""
        return True

    def _get_next_resource_id(self) -> str:
        """Get next unique resource ID"""
        with self._lock:
            self._resource_id_counter += 1
            return f"{self.name}_{self._resource_id_counter}"

    def get_pool_status(self) -> Dict[str, Any]:
        """Get pool status"""
        with self._lock:
            return {
                "name": self.name,
                "available_resources": len(self.available_resources),
                "in_use_resources": len(self.in_use_resources),
                "total_resources": len(self.available_resources) + len(self.in_use_resources),
                "max_resources": self.config.max_resources,
                "healthy_resources": sum(1 for healthy in self.resource_health.values() if healthy),
                "unhealthy_resources": sum(1 for healthy in self.resource_health.values() if not healthy)
            }

class SystemResourceMonitor:
    """Monitor system resources"""

    def __init__(self, monitoring_interval: float = 30.0):
        self.monitoring_interval = monitoring_interval
        self.resource_history: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        self.logger = logging.getLogger("SystemResourceMonitor")

    def get_current_resources(self) -> Dict[str, Any]:
        """Get current system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            resources = {
                "timestamp": time.time(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory.used / (1024**3),
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "disk_used_gb": disk.used / (1024**3),
                "disk_free_gb": disk.free / (1024**3)
            }

            with self._lock:
                self.resource_history.append(resources)
                # Keep only last 100 entries
                if len(self.resource_history) > 100:
                    self.resource_history = self.resource_history[-100:]

            return resources

        except Exception as e:
            self.logger.error(f"Failed to get system resources: {e}")
            return {}

    def is_system_overloaded(self, cpu_threshold: float = 90.0,
                           memory_threshold: float = 90.0) -> bool:
        """Check if system is overloaded"""
        resources = self.get_current_resources()
        if not resources:
            return False

        return (resources.get('cpu_percent', 0) > cpu_threshold or
                resources.get('memory_percent', 0) > memory_threshold)

    def get_resource_trends(self) -> Dict[str, Any]:
        """Get resource usage trends"""
        with self._lock:
            if len(self.resource_history) < 2:
                return {"error": "Not enough data for trends"}

            recent = self.resource_history[-10:]  # Last 10 readings

            def calculate_trend(values):
                if len(values) < 2:
                    return 0
                return (values[-1] - values[0]) / len(values)

            cpu_values = [r.get('cpu_percent', 0) for r in recent]
            memory_values = [r.get('memory_percent', 0) for r in recent]

            return {
                "cpu_trend": calculate_trend(cpu_values),
                "memory_trend": calculate_trend(memory_values),
                "avg_cpu": sum(cpu_values) / len(cpu_values),
                "avg_memory": sum(memory_values) / len(memory_values),
                "data_points": len(recent)
            }

# Global instances
circuit_breaker_registry: Dict[str, CircuitBreaker] = {}
resource_pool_registry: Dict[str, ResourcePool] = {}
system_monitor = SystemResourceMonitor()

def get_or_create_circuit_breaker(name: str, config: CircuitBreakerConfig = None) -> CircuitBreaker:
    """Get or create a circuit breaker"""
    if name not in circuit_breaker_registry:
        circuit_breaker_registry[name] = CircuitBreaker(name, config)
    return circuit_breaker_registry[name]

def get_or_create_resource_pool(name: str, resource_factory: Callable[[], Any],
                               config: ResourcePoolConfig = None) -> ResourcePool:
    """Get or create a resource pool"""
    if name not in resource_pool_registry:
        resource_pool_registry[name] = ResourcePool(name, resource_factory, config)
    return resource_pool_registry[name]

def demonstrate_resource_pooling():
    """Demonstrate resource pooling and circuit breaker capabilities"""
    print("🛡️ AGI RESOURCE POOLING & CIRCUIT BREAKER SYSTEM")
    print("=" * 55)

    # Create circuit breaker
    api_circuit_breaker = get_or_create_circuit_breaker(
        "api_calls",
        CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30.0)
    )

    # Create resource pool
    def create_database_connection():
        # Simulate database connection
        return {"connection_id": f"conn_{time.time()}", "status": "active"}

    db_pool = get_or_create_resource_pool(
        "database_connections",
        create_database_connection,
        ResourcePoolConfig(max_resources=5, min_resources=2)
    )

    print("   🔬 Testing Circuit Breaker...")
    @api_circuit_breaker
    def simulate_api_call(success: bool = True):
        if not success:
            raise Exception("API call failed")
        return {"data": "success"}

    # Test successful calls
    for i in range(3):
        try:
            result = simulate_api_call(True)
            print(f"   ✅ API call {i+1} succeeded")
        except Exception as e:
            print(f"   ❌ API call {i+1} failed: {e}")

    # Test failures
    for i in range(4):
        try:
            result = simulate_api_call(False)
            print(f"   ✅ API call failed {i+1} succeeded")
        except Exception as e:
            print(f"   ❌ API call failed {i+1}: {e}")

    # Test circuit breaker open
    try:
        result = simulate_api_call(True)
        print("   ⚠️ Circuit breaker should be open")
    except Exception as e:
        print(f"   🛡️ Circuit breaker working: {e}")

    print("   🔬 Testing Resource Pool...")
    # Test resource pool
    resources = []
    for i in range(3):
        resource = db_pool.acquire_resource()
        if resource:
            resources.append(resource)
            print(f"   📦 Acquired resource {i+1}: {resource['connection_id']}")

    # Release resources
    for i, resource in enumerate(resources):
        db_pool.release_resource(resource)
        print(f"   🔄 Released resource {i+1}")

    # Check pool status
    status = db_pool.get_pool_status()
    print(f"   📊 Pool status: {status['available_resources']}/{status['total_resources']} available")

    print("   🔬 Testing System Resource Monitoring...")
    # Test system monitoring
    resources = system_monitor.get_current_resources()
    print(f"   📈 CPU: {resources.get('cpu_percent', 'N/A')}%")
    print(f"   📈 Memory: {resources.get('memory_percent', 'N/A')}%")

    trends = system_monitor.get_resource_trends()
    print(f"   📊 Resource trends: {trends}")

    print("   ✅ Resource pooling and circuit breaker system operational!")

if __name__ == "__main__":
    demonstrate_resource_pooling()
