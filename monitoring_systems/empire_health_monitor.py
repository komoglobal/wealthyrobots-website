#!/usr/bin/env python3
"""
AGI BUILT: EMPIRE HEALTH MONITOR
Comprehensive empire health monitoring and alerting
"""

import json
import psutil
from datetime import datetime
from typing import Dict, List, Any

class EmpireHealthMonitor:
    """Comprehensive empire health monitoring"""
    
    def __init__(self):
        self.health_log = 'empire_health.log'
        self.alert_thresholds = {
            'cpu_usage': 80,  # 80% CPU usage
            'memory_usage': 85,  # 85% memory usage
            'disk_usage': 90,  # 90% disk usage
            'error_rate': 5  # 5% error rate
        }
        self.health_history = []
        
    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health"""
        health_metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': self._get_cpu_usage(),
            'memory_usage': self._get_memory_usage(),
            'disk_usage': self._get_disk_usage(),
            'network_status': self._get_network_status(),
            'process_count': self._get_process_count(),
            'overall_health': 'unknown'
        }
        
        # Determine overall health
        health_metrics['overall_health'] = self._calculate_overall_health(health_metrics)
        
        # Check for alerts
        alerts = self._check_alerts(health_metrics)
        health_metrics['alerts'] = alerts
        
        # Store in history
        self.health_history.append(health_metrics)
        
        # Log health status
        self._log_health_status(health_metrics)
        
        return health_metrics
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage"""
        try:
            return psutil.cpu_percent(interval=1)
        except ImportError:
            return 0.0
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage"""
        try:
            return psutil.virtual_memory().percent
        except ImportError:
            return 0.0
    
    def _get_disk_usage(self) -> float:
        """Get current disk usage"""
        try:
            return psutil.disk_usage('/').percent
        except ImportError:
            return 0.0
    
    def _get_network_status(self) -> str:
        """Get network status"""
        try:
            # Check if we can reach external services
            import requests
            response = requests.get('https://httpbin.org/get', timeout=5)
            return 'connected' if response.status_code == 200 else 'disconnected'
        except:
            return 'unknown'
    
    def _get_process_count(self) -> int:
        """Get current process count"""
        try:
            return len(psutil.pids())
        except ImportError:
            return 0
    
    def _calculate_overall_health(self, metrics: Dict[str, Any]) -> str:
        """Calculate overall health status"""
        cpu_ok = metrics['cpu_usage'] < self.alert_thresholds['cpu_usage']
        memory_ok = metrics['memory_usage'] < self.alert_thresholds['memory_usage']
        disk_ok = metrics['disk_usage'] < self.alert_thresholds['disk_usage']
        network_ok = metrics['network_status'] == 'connected'
        
        if all([cpu_ok, memory_ok, disk_ok, network_ok]):
            return 'healthy'
        elif any([not cpu_ok, not memory_ok, not disk_ok]):
            return 'critical'
        else:
            return 'warning'
    
    def _check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for alert conditions"""
        alerts = []
        
        if metrics['cpu_usage'] > self.alert_thresholds['cpu_usage']:
            alerts.append({
                'type': 'cpu_high',
                'message': f"CPU usage is {metrics['cpu_usage']:.1f}%",
                'severity': 'warning'
            })
        
        if metrics['memory_usage'] > self.alert_thresholds['memory_usage']:
            alerts.append({
                'type': 'memory_high',
                'message': f"Memory usage is {metrics['memory_usage']:.1f}%",
                'severity': 'warning'
            })
        
        if metrics['disk_usage'] > self.alert_thresholds['disk_usage']:
            alerts.append({
                'type': 'disk_high',
                'message': f"Disk usage is {metrics['disk_usage']:.1f}%",
                'severity': 'critical'
            })
        
        if metrics['network_status'] != 'connected':
            alerts.append({
                'type': 'network_issue',
                'message': f"Network status: {metrics['network_status']}",
                'severity': 'critical'
            })
        
        return alerts
    
    def _log_health_status(self, health_metrics: Dict[str, Any]):
        """Log health status to file"""
        try:
            with open(self.health_log, 'a') as f:
                f.write(json.dumps(health_metrics) + '\n')
        except Exception as e:
            print(f"Error logging health status: {e}")
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health summary"""
        if not self.health_history:
            return {'status': 'no_data'}
        
        recent_health = self.health_history[-1]
        
        return {
            'current_health': recent_health['overall_health'],
            'current_alerts': len(recent_health.get('alerts', [])),
            'last_check': recent_health['timestamp'],
            'health_trend': self._calculate_health_trend()
        }
    
    def _calculate_health_trend(self) -> str:
        """Calculate health trend over time"""
        if len(self.health_history) < 2:
            return 'stable'
        
        recent_health = self.health_history[-5:]  # Last 5 checks
        
        healthy_count = sum(1 for h in recent_health if h['overall_health'] == 'healthy')
        critical_count = sum(1 for h in recent_health if h['overall_health'] == 'critical')
        
        if critical_count > healthy_count:
            return 'declining'
        elif healthy_count > critical_count:
            return 'improving'
        else:
            return 'stable'

# Initialize empire health monitor
empire_health_monitor = EmpireHealthMonitor()
