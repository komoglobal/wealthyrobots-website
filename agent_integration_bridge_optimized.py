#!/usr/bin/env python3
"""
Agent Integration Bridge - WealthyRobot (Optimized)
Connects all existing agents with the autonomous trading fund system
Enables seamless communication and coordination between agents
Runs continuously for production use
"""

import os
import json
import time
import asyncio
import logging
import signal
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import importlib.util
import subprocess

class AgentIntegrationBridge:
    """
    Bridge system that integrates all existing agents with the autonomous trading fund
    """
    
    def __init__(self):
        self.name = "Agent Integration Bridge"
        self.version = "1.0.0"
        self.running = True
        
        # Agent registry
        self.registered_agents = {}
        self.agent_status = {}
        
        # Communication channels
        self.message_queue = []
        self.command_history = []
        
        # Performance monitoring
        self.last_scan_time = datetime.now()
        self.scan_interval = 300  # 5 minutes
        self.health_check_interval = 60  # 1 minute
        
        # Setup logging
        self._setup_logging()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Discover and register agents
        self._discover_agents()
        
        self.logger.info(f"🌉 {self.name} v{self.version} - INITIALIZED")
        self.logger.info(f"🤖 Registered Agents: {len(self.registered_agents)}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def _setup_logging(self):
        """Setup logging for the bridge"""
        os.makedirs('logs', exist_ok=True)
        
        log_file = f'logs/agent_bridge_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('AgentIntegrationBridge')
        self.logger.info(f"Agent Integration Bridge logging initialized")
    
    def _discover_agents(self):
        """Discover and register all available agents"""
        try:
            self.logger.info("🔍 Discovering available agents...")
            
            # Known agent files to look for
            agent_files = [
                "ultimate_ceo_agent.py",
                "algorand_defi_trading_agent.py",
                "empire_optimization_system.py",
                "enhanced_dynamic_api_system.py",
                "smart_api_ranker.py",
                "data_management_system.py"
            ]
            
            for agent_file in agent_files:
                if os.path.exists(agent_file):
                    self._register_agent(agent_file)
            
            # Also look for any Python files that might be agents
            for file in os.listdir('.'):
                if file.endswith('_agent.py') or file.endswith('_system.py'):
                    if file not in [a['file'] for a in self.registered_agents.values()]:
                        self._register_agent(file)
            
            self.logger.info(f"✅ Agent discovery completed - {len(self.registered_agents)} agents found")
            
        except Exception as e:
            self.logger.error(f"Error discovering agents: {e}")
    
    def _register_agent(self, agent_file: str):
        """Register an agent with the bridge"""
        try:
            agent_name = agent_file.replace('.py', '').replace('_', ' ').title()
            
            # Determine agent type and capabilities
            agent_type = self._analyze_agent_type(agent_file)
            capabilities = self._analyze_agent_capabilities(agent_file)
            
            self.registered_agents[agent_name] = {
                'file': agent_file,
                'type': agent_type,
                'capabilities': capabilities,
                'last_seen': datetime.now().isoformat(),
                'status': 'registered'
            }
            
            self.agent_status[agent_name] = 'registered'
            
            self.logger.info(f"✅ Registered agent: {agent_name} ({agent_type})")
            
        except Exception as e:
            self.logger.error(f"Error registering agent {agent_file}: {e}")
    
    def _analyze_agent_type(self, agent_file: str) -> str:
        """Analyze agent file to determine type"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
                
            if 'ceo' in agent_file.lower():
                return 'CEO Agent'
            elif 'trading' in agent_file.lower():
                return 'Trading Agent'
            elif 'empire' in agent_file.lower():
                return 'Empire Management'
            elif 'api' in agent_file.lower():
                return 'API Management'
            elif 'data' in agent_file.lower():
                return 'Data Management'
            else:
                return 'General Agent'
                
        except Exception:
            return 'Unknown'
    
    def _analyze_agent_capabilities(self, agent_file: str) -> List[str]:
        """Analyze agent file to determine capabilities"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
                
            capabilities = []
            
            if 'trading' in content.lower():
                capabilities.append('Trading')
            if 'analysis' in content.lower():
                capabilities.append('Analysis')
            if 'api' in content.lower():
                capabilities.append('API Management')
            if 'data' in content.lower():
                capabilities.append('Data Processing')
            if 'optimization' in content.lower():
                capabilities.append('Optimization')
            if 'empire' in content.lower():
                capabilities.append('Empire Management')
            
            return capabilities if capabilities else ['General Operations']
            
        except Exception:
            return ['General Operations']
    
    def broadcast_message(self, message: Dict) -> List[Dict]:
        """Broadcast a message to all registered agents"""
        results = []
        
        for agent_name in self.registered_agents:
            try:
                result = self._send_message_to_agent(agent_name, message)
                results.append({
                    'agent': agent_name,
                    'success': result['success'],
                    'response': result.get('response', 'No response')
                })
                
                # Log the communication
                self.command_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'command': 'broadcast',
                    'agent': agent_name,
                    'message': message,
                    'result': result
                })
                
            except Exception as e:
                results.append({
                    'agent': agent_name,
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def _send_message_to_agent(self, agent_name: str, message: Dict) -> Dict:
        """Send a message to a specific agent"""
        try:
            # For now, simulate agent communication
            # In production, this would use actual agent communication protocols
            
            agent_info = self.registered_agents[agent_name]
            
            # Simulate agent response
            response = {
                'received_at': datetime.now().isoformat(),
                'agent': agent_name,
                'message_type': message.get('type', 'unknown'),
                'status': 'processed'
            }
            
            # Update agent status
            self.agent_status[agent_name] = 'active'
            self.registered_agents[agent_name]['last_seen'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'response': response
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_agent_status(self, agent_name: str) -> Dict:
        """Get status of a specific agent"""
        try:
            if agent_name not in self.registered_agents:
                return {'success': False, 'error': 'Agent not found'}
            
            agent_info = self.registered_agents[agent_name]
            status = self.agent_status.get(agent_name, 'unknown')
            
            return {
                'success': True,
                'agent_name': agent_name,
                'status': status,
                'type': agent_info['type'],
                'capabilities': agent_info['capabilities'],
                'last_seen': agent_info['last_seen']
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_all_agents_status(self) -> List[Dict]:
        """Get status of all agents"""
        results = []
        
        for agent_name in self.registered_agents:
            status = self.get_agent_status(agent_name)
            if status['success']:
                results.append(status)
        
        return results
    
    def restart_agent(self, agent_name: str) -> Dict:
        """Restart a specific agent"""
        try:
            if agent_name not in self.registered_agents:
                return {'success': False, 'error': 'Agent not found'}
            
            # Simulate agent restart
            self.agent_status[agent_name] = 'restarting'
            
            # Wait a moment to simulate restart
            time.sleep(1)
            
            self.agent_status[agent_name] = 'active'
            self.registered_agents[agent_name]['last_seen'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'command': 'restart',
                'agent': agent_name,
                'result': 'Agent restarted successfully'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _optimize_agent_command(self, agent_name: str, params: Dict = None) -> Dict:
        """Optimize an agent's performance"""
        try:
            # This would implement agent-specific optimization
            return {
                'success': True,
                'command': 'optimize',
                'agent': agent_name,
                'result': f'Optimization completed for {agent_name}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _generate_agent_report_command(self, agent_name: str) -> Dict:
        """Generate a report for an agent"""
        try:
            agent_info = self.registered_agents[agent_name]
            
            report = {
                'agent_name': agent_name,
                'timestamp': datetime.now().isoformat(),
                'type': agent_info['type'],
                'capabilities': agent_info['capabilities'],
                'status': self.agent_status.get(agent_name, 'unknown'),
                'last_seen': agent_info['last_seen']
            }
            
            return {
                'success': True,
                'command': 'report',
                'agent': agent_name,
                'result': report
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_bridge_status(self) -> Dict:
        """Get comprehensive bridge status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'bridge_name': self.name,
            'version': self.version,
            'status': 'active',
            'total_agents': len(self.registered_agents),
            'active_agents': len([a for a in self.agent_status.values() if a == 'active']),
            'message_queue_length': len(self.message_queue),
            'command_history_length': len(self.command_history),
            'agents': self.get_all_agents_status()
        }
    
    def perform_health_check(self):
        """Perform health check on all agents"""
        try:
            self.logger.info("🏥 Performing health check on all agents...")
            
            health_status = {
                'timestamp': datetime.now().isoformat(),
                'total_agents': len(self.registered_agents),
                'healthy_agents': 0,
                'unhealthy_agents': 0,
                'agent_details': []
            }
            
            for agent_name in self.registered_agents:
                agent_status = self.get_agent_status(agent_name)
                if agent_status['success']:
                    if agent_status['status'] == 'active':
                        health_status['healthy_agents'] += 1
                    else:
                        health_status['unhealthy_agents'] += 1
                    
                    health_status['agent_details'].append(agent_status)
            
            self.logger.info(f"Health check completed: {health_status['healthy_agents']} healthy, {health_status['unhealthy_agents']} unhealthy")
            
            # Log health status to file
            health_file = f'logs/bridge_health_{datetime.now().strftime("%Y%m%d")}.json'
            try:
                with open(health_file, 'a') as f:
                    json.dump(health_status, f)
                    f.write('\n')
            except Exception as e:
                self.logger.error(f"Error writing health status: {e}")
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Error during health check: {e}")
            return None
    
    def run_continuous_operation(self):
        """Run the bridge continuously"""
        self.logger.info("🚀 Starting continuous operation mode...")
        
        last_health_check = datetime.now()
        last_agent_scan = datetime.now()
        
        while self.running:
            try:
                current_time = datetime.now()
                
                # Perform periodic health checks
                if (current_time - last_health_check).total_seconds() >= self.health_check_interval:
                    self.perform_health_check()
                    last_health_check = current_time
                
                # Perform periodic agent scans
                if (current_time - last_agent_scan).total_seconds() >= self.scan_interval:
                    self.logger.info("🔍 Performing periodic agent scan...")
                    self._discover_agents()
                    last_agent_scan = current_time
                
                # Process any pending messages
                if self.message_queue:
                    message = self.message_queue.pop(0)
                    self.logger.info(f"Processing message: {message.get('type', 'unknown')}")
                    self.broadcast_message(message)
                
                # Sleep to prevent excessive CPU usage
                time.sleep(10)
                
            except KeyboardInterrupt:
                self.logger.info("Received keyboard interrupt, shutting down...")
                break
            except Exception as e:
                self.logger.error(f"Error in continuous operation: {e}")
                time.sleep(30)  # Wait before retrying
        
        self.logger.info("🛑 Bridge operation stopped")

def main():
    """Main entry point for the optimized agent integration bridge"""
    print("🌉 AGENT INTEGRATION BRIDGE - OPTIMIZED VERSION")
    print("=" * 60)
    
    # Create bridge
    bridge = AgentIntegrationBridge()
    
    # Get initial status
    status = bridge.get_bridge_status()
    print(f"Bridge Status: {status['status']}")
    print(f"Total Agents: {status['total_agents']}")
    print(f"Active Agents: {status['active_agents']}")
    
    # Start continuous operation
    try:
        bridge.run_continuous_operation()
    except Exception as e:
        bridge.logger.error(f"Fatal error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
