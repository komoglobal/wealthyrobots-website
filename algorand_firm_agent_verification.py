#!/usr/bin/env python3
"""
ALGORAND FIRM AGENT VERIFICATION SYSTEM
Comprehensive verification of all trading firm agents and their operational status
"""

import asyncio
import json
import subprocess
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('algorand_firm_verification.log'),
        logging.StreamHandler()
    ]
)

class AlgorandFirmAgentVerification:
    def __init__(self):
        print("🔍 ALGORAND FIRM AGENT VERIFICATION SYSTEM - INITIALIZING...")
        print("✅ Verifying all trading firm agents and their operational status")
        
        # Agent definitions and expected services
        self.expected_agents = {
            'paper_trading': {
                'service_name': 'algofund-paper.service',
                'process_pattern': 'algofund.run_paper_service',
                'log_file': 'logs/algofund-paper.out',
                'expected_status': 'active',
                'critical': True
            },
            'live_trading': {
                'service_name': 'algofund-live.service',
                'process_pattern': 'algofund.orchestrator',
                'log_file': 'logs/algofund-live.out',
                'expected_status': 'active',
                'critical': True
            },
            'fund_manager': {
                'service_name': 'fund-manager.service',
                'process_pattern': 'algofund.agents.fund_manager',
                'log_file': 'logs/algofund-live.out',
                'expected_status': 'active',
                'critical': True
            },
            'trading_floor': {
                'service_name': 'trading-floor.service',
                'process_pattern': 'algofund.agents.trading_floor',
                'log_file': 'logs/algofund-live.out',
                'expected_status': 'active',
                'critical': False
            },
            'slack_bot': {
                'service_name': 'slack-bot.service',
                'process_pattern': 'algofund.agents.slack_bot',
                'log_file': 'logs/algofund-live.out',
                'expected_status': 'active',
                'critical': False
            },
            'defillama_scanner': {
                'service_name': 'defillama-scanner.service',
                'process_pattern': 'algofund.agents.defillama_scanner',
                'log_file': 'logs/algofund-live.out',
                'expected_status': 'active',
                'critical': False
            },
            'daily_reporting': {
                'service_name': 'algofund-report-daily.service',
                'process_pattern': 'algofund.report_daily',
                'log_file': 'logs/algofund-report-daily.out',
                'expected_status': 'active',
                'critical': False
            }
        }
        
        # Verification results
        self.verification_results = {
            'timestamp': None,
            'overall_status': 'unknown',
            'agents_status': {},
            'system_health': {
                'total_agents': 0,
                'active_agents': 0,
                'critical_agents_active': 0,
                'total_critical_agents': 0
            },
            'performance_metrics': {},
            'recommendations': []
        }
        
        print("✅ Algorand Firm Agent Verification System initialized")
    
    async def run_comprehensive_verification(self):
        """Run comprehensive verification of all firm agents"""
        print("🚀 Starting comprehensive firm agent verification...")
        
        try:
            # 1. Verify systemd services
            await self.verify_systemd_services()
            
            # 2. Verify running processes
            await self.verify_running_processes()
            
            # 3. Verify log file activity
            await self.verify_log_activity()
            
            # 4. Verify agent communication
            await self.verify_agent_communication()
            
            # 5. Verify performance metrics
            await self.verify_performance_metrics()
            
            # 6. Generate verification report
            await self.generate_verification_report()
            
            # 7. Display verification summary
            self.display_verification_summary()
            
        except Exception as e:
            logging.error(f"Error in comprehensive verification: {e}")
            raise
    
    async def verify_systemd_services(self):
        """Verify systemd services are properly configured and running"""
        print("🔧 Verifying systemd services...")
        
        try:
            for agent_name, agent_config in self.expected_agents.items():
                service_name = agent_config['service_name']
                
                # Check service status
                result = subprocess.run(
                    ['systemctl', 'is-active', service_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                service_status = result.stdout.strip()
                is_active = service_status == 'active'
                
                # Check if service is enabled
                result_enabled = subprocess.run(
                    ['systemctl', 'is-enabled', service_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                is_enabled = result_enabled.stdout.strip() == 'enabled'
                
                # Store results
                self.verification_results['agents_status'][agent_name] = {
                    'service_name': service_name,
                    'service_status': service_status,
                    'service_enabled': is_enabled,
                    'is_active': is_active,
                    'critical': agent_config['critical'],
                    'verification_time': datetime.now().isoformat()
                }
                
                if is_active:
                    self.verification_results['system_health']['active_agents'] += 1
                    if agent_config['critical']:
                        self.verification_results['system_health']['critical_agents_active'] += 1
                
                if agent_config['critical']:
                    self.verification_results['system_health']['total_critical_agents'] += 1
                
                self.verification_results['system_health']['total_agents'] += 1
                
                status_icon = "✅" if is_active else "❌"
                print(f"  {status_icon} {agent_name}: {service_status} (enabled: {is_enabled})")
                
        except Exception as e:
            logging.error(f"Error verifying systemd services: {e}")
    
    async def verify_running_processes(self):
        """Verify that expected processes are actually running"""
        print("🔄 Verifying running processes...")
        
        try:
            for agent_name, agent_config in self.expected_agents.items():
                process_pattern = agent_config['process_pattern']
                
                # Check if process is running
                result = subprocess.run(
                    ['pgrep', '-f', process_pattern],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                is_running = result.returncode == 0
                process_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                
                # Update verification results
                if agent_name in self.verification_results['agents_status']:
                    self.verification_results['agents_status'][agent_name].update({
                        'process_running': is_running,
                        'process_count': process_count,
                        'process_pattern': process_pattern
                    })
                
                status_icon = "✅" if is_running else "❌"
                print(f"  {status_icon} {agent_name}: {process_count} process(es) running")
                
        except Exception as e:
            logging.error(f"Error verifying running processes: {e}")
    
    async def verify_log_activity(self):
        """Verify that log files are being actively updated"""
        print("📝 Verifying log file activity...")
        
        try:
            for agent_name, agent_config in self.expected_agents.items():
                log_file = agent_config['log_file']
                
                if not os.path.exists(log_file):
                    log_status = "missing"
                    is_active = False
                else:
                    # Check if log file was modified in last 10 minutes
                    stat = os.stat(log_file)
                    time_since_modification = time.time() - stat.st_mtime
                    
                    if time_since_modification < 600:  # 10 minutes
                        log_status = "active"
                        is_active = True
                    elif time_since_modification < 3600:  # 1 hour
                        log_status = "stale"
                        is_active = False
                    else:
                        log_status = "inactive"
                        is_active = False
                
                # Update verification results
                if agent_name in self.verification_results['agents_status']:
                    self.verification_results['agents_status'][agent_name].update({
                        'log_status': log_status,
                        'log_active': is_active,
                        'log_file': log_file,
                        'last_log_update': time.time() - (time.time() - stat.st_mtime) if os.path.exists(log_file) else None
                    })
                
                status_icon = "✅" if is_active else "⚠️" if log_status == "stale" else "❌"
                print(f"  {status_icon} {agent_name}: {log_status}")
                
        except Exception as e:
            logging.error(f"Error verifying log activity: {e}")
    
    async def verify_agent_communication(self):
        """Verify that agents can communicate with each other"""
        print("💬 Verifying agent communication...")
        
        try:
            # Check if agents are writing to shared log files
            communication_status = {}
            
            for agent_name, agent_config in self.expected_agents.items():
                log_file = agent_config['log_file']
                
                if os.path.exists(log_file):
                    # Check for recent activity in logs
                    result = subprocess.run(
                        ['tail', '-10', log_file],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0 and result.stdout.strip():
                        # Check for JSON metrics (indicates active communication)
                        has_json_metrics = any(
                            line.strip().startswith('{') and line.strip().endswith('}')
                            for line in result.stdout.split('\n')
                            if line.strip()
                        )
                        
                        communication_status[agent_name] = {
                            'can_write_logs': True,
                            'has_json_metrics': has_json_metrics,
                            'communication_active': has_json_metrics
                        }
                    else:
                        communication_status[agent_name] = {
                            'can_write_logs': False,
                            'has_json_metrics': False,
                            'communication_active': False
                        }
                else:
                    communication_status[agent_name] = {
                        'can_write_logs': False,
                        'has_json_metrics': False,
                        'communication_active': False
                    }
                
                # Update verification results
                if agent_name in self.verification_results['agents_status']:
                    self.verification_results['agents_status'][agent_name].update(
                        communication_status[agent_name]
                    )
                
                status_icon = "✅" if communication_status[agent_name]['communication_active'] else "❌"
                print(f"  {status_icon} {agent_name}: communication {'active' if communication_status[agent_name]['communication_active'] else 'inactive'}")
                
        except Exception as e:
            logging.error(f"Error verifying agent communication: {e}")
    
    async def verify_performance_metrics(self):
        """Verify performance metrics and system health"""
        print("📊 Verifying performance metrics...")
        
        try:
            # Calculate overall system health
            total_agents = self.verification_results['system_health']['total_agents']
            active_agents = self.verification_results['system_health']['active_agents']
            critical_active = self.verification_results['system_health']['critical_agents_active']
            total_critical = self.verification_results['system_health']['total_critical_agents']
            
            # Calculate health percentages
            overall_health = (active_agents / total_agents * 100) if total_agents > 0 else 0
            critical_health = (critical_active / total_critical * 100) if total_critical > 0 else 0
            
            # Determine overall status
            if critical_health == 100 and overall_health >= 80:
                overall_status = 'excellent'
            elif critical_health == 100 and overall_health >= 60:
                overall_status = 'good'
            elif critical_health >= 80:
                overall_status = 'fair'
            else:
                overall_status = 'critical'
            
            # Store performance metrics
            self.verification_results['performance_metrics'] = {
                'overall_health_percentage': overall_health,
                'critical_health_percentage': critical_health,
                'agent_uptime': overall_health,
                'critical_agent_uptime': critical_health
            }
            
            self.verification_results['overall_status'] = overall_status
            self.verification_results['timestamp'] = datetime.now().isoformat()
            
            # Generate recommendations
            await self.generate_recommendations()
            
        except Exception as e:
            logging.error(f"Error verifying performance metrics: {e}")
    
    async def generate_recommendations(self):
        """Generate recommendations based on verification results"""
        try:
            recommendations = []
            
            # Check for inactive critical agents
            for agent_name, agent_status in self.verification_results['agents_status'].items():
                if agent_status.get('critical', False) and not agent_status.get('is_active', False):
                    recommendations.append({
                        'priority': 'critical',
                        'action': f'Restart {agent_name} service immediately',
                        'reason': 'Critical agent is inactive',
                        'agent': agent_name
                    })
            
            # Check for stale logs
            for agent_name, agent_status in self.verification_results['agents_status'].items():
                if agent_status.get('log_status') == 'stale':
                    recommendations.append({
                        'priority': 'warning',
                        'action': f'Investigate {agent_name} log activity',
                        'reason': 'Log file not recently updated',
                        'agent': agent_name
                    })
            
            # Check for communication issues
            for agent_name, agent_status in self.verification_results['agents_status'].items():
                if not agent_status.get('communication_active', False):
                    recommendations.append({
                        'priority': 'medium',
                        'action': f'Check {agent_name} communication',
                        'reason': 'Agent not generating metrics',
                        'agent': agent_name
                    })
            
            # Overall system recommendations
            if self.verification_results['overall_status'] == 'critical':
                recommendations.append({
                    'priority': 'critical',
                    'action': 'Immediate system intervention required',
                    'reason': 'Critical agents are down',
                    'agent': 'system'
                })
            elif self.verification_results['overall_status'] == 'fair':
                recommendations.append({
                    'priority': 'medium',
                    'action': 'Schedule maintenance window',
                    'reason': 'System health below optimal levels',
                    'agent': 'system'
                })
            
            self.verification_results['recommendations'] = recommendations
            
        except Exception as e:
            logging.error(f"Error generating recommendations: {e}")
    
    async def generate_verification_report(self):
        """Generate comprehensive verification report"""
        try:
            # Save detailed report
            with open('algorand_firm_verification_report.json', 'w') as f:
                json.dump(self.verification_results, f, indent=2, default=str)
            
            # Save summary report
            summary = {
                'timestamp': self.verification_results['timestamp'],
                'overall_status': self.verification_results['overall_status'],
                'system_health': self.verification_results['system_health'],
                'performance_metrics': self.verification_results['performance_metrics'],
                'critical_issues': [
                    rec for rec in self.verification_results['recommendations']
                    if rec['priority'] == 'critical'
                ]
            }
            
            with open('algorand_firm_status_summary.json', 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            
            logging.info("📊 Verification report generated successfully")
            
        except Exception as e:
            logging.error(f"Error generating verification report: {e}")
    
    def display_verification_summary(self):
        """Display verification summary to console"""
        print("\n" + "="*80)
        print("🎯 ALGORAND FIRM AGENT VERIFICATION SUMMARY")
        print("="*80)
        
        # Overall status
        status_icon = {
            'excellent': '🟢',
            'good': '🟡',
            'fair': '🟠',
            'critical': '🔴'
        }.get(self.verification_results['overall_status'], '⚪')
        
        print(f"\n📊 Overall System Status: {status_icon} {self.verification_results['overall_status'].upper()}")
        print(f"🏥 System Health: {self.verification_results['performance_metrics']['overall_health_percentage']:.1f}%")
        print(f"🚨 Critical Agents: {self.verification_results['performance_metrics']['critical_health_percentage']:.1f}%")
        
        # Agent status summary
        print(f"\n🤖 Agent Status Summary:")
        print(f"   Total Agents: {self.verification_results['system_health']['total_agents']}")
        print(f"   Active Agents: {self.verification_results['system_health']['active_agents']}")
        print(f"   Critical Agents Active: {self.verification_results['system_health']['critical_agents_active']}/{self.verification_results['system_health']['total_critical_agents']}")
        
        # Critical issues
        critical_issues = [
            rec for rec in self.verification_results['recommendations']
            if rec['priority'] == 'critical'
        ]
        
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES REQUIRING IMMEDIATE ATTENTION:")
            for issue in critical_issues:
                print(f"   ❌ {issue['action']} - {issue['reason']}")
        else:
            print(f"\n✅ No critical issues detected")
        
        # Recommendations
        if self.verification_results['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in self.verification_results['recommendations']:
                priority_icon = {
                    'critical': '🔴',
                    'warning': '🟡',
                    'medium': '🟠',
                    'low': '🟢'
                }.get(rec['priority'], '⚪')
                
                print(f"   {priority_icon} {rec['action']}")
        
        print(f"\n📁 Reports saved to:")
        print(f"   - algorand_firm_verification_report.json (detailed)")
        print(f"   - algorand_firm_status_summary.json (summary)")
        print("="*80)
    
    def get_verification_status(self) -> Dict:
        """Get current verification status"""
        return self.verification_results

async def main():
    """Main function to run the Algorand firm agent verification"""
    print("🚀 Starting Algorand Firm Agent Verification...")
    
    try:
        # Initialize verification system
        verification_system = AlgorandFirmAgentVerification()
        
        # Run comprehensive verification
        await verification_system.run_comprehensive_verification()
        
    except Exception as e:
        logging.error(f"Fatal error in verification: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
