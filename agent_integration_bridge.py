#!/usr/bin/env python3
"""
Agent Integration Bridge - WealthyRobot
Connects all existing agents with the autonomous trading fund system
Enables seamless communication and coordination between agents
"""

import os
import json
import time
import asyncio
import logging
from datetime import datetime
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
        
        # Agent registry
        self.registered_agents = {}
        self.agent_status = {}
        
        # Communication channels
        self.message_queue = []
        self.command_history = []
        
        # Setup logging
        self._setup_logging()
        
        # Discover and register agents
        self._discover_agents()
        
        print(f"🌉 {self.name} v{self.version} - INITIALIZED")
        print(f"🤖 Registered Agents: {len(self.registered_agents)}")
    
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
            print("🔍 Discovering available agents...")
            
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
            
            print(f"✅ Agent discovery completed - {len(self.registered_agents)} agents found")
            
        except Exception as e:
            self.logger.error(f"Error discovering agents: {e}")
    
    def _register_agent(self, agent_file: str):
        """Register an agent with the bridge"""
        try:
            agent_name = agent_file.replace('.py', '').replace('_', ' ').title()
            
            # Determine agent type and capabilities
            agent_type = self._analyze_agent_type(agent_file)
            capabilities = self._analyze_agent_capabilities(agent_file)
            
            agent_info = {
                'name': agent_name,
                'file': agent_file,
                'type': agent_type,
                'capabilities': capabilities,
                'status': 'registered',
                'last_seen': datetime.now().isoformat(),
                'communication_protocol': 'python_module'
            }
            
            self.registered_agents[agent_name] = agent_info
            self.agent_status[agent_name] = 'active'
            
            self.logger.info(f"Agent registered: {agent_name} ({agent_file})")
            print(f"✅ Registered: {agent_name}")
            
        except Exception as e:
            self.logger.error(f"Error registering agent {agent_file}: {e}")
    
    def _analyze_agent_type(self, agent_file: str) -> str:
        """Analyze agent file to determine its type"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
                
            if 'ceo' in agent_file.lower():
                return 'strategic_decision'
            elif 'trading' in agent_file.lower():
                return 'trading_execution'
            elif 'optimization' in agent_file.lower():
                return 'system_optimization'
            elif 'api' in agent_file.lower():
                return 'api_management'
            elif 'data' in agent_file.lower():
                return 'data_management'
            else:
                return 'general_purpose'
                
        except Exception:
            return 'unknown'
    
    def _analyze_agent_capabilities(self, agent_file: str) -> List[str]:
        """Analyze agent file to determine its capabilities"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            capabilities = []
            
            # Analyze content for capabilities
            if 'trading' in content.lower():
                capabilities.append('trading_execution')
            if 'risk' in content.lower():
                capabilities.append('risk_management')
            if 'optimization' in content.lower():
                capabilities.append('system_optimization')
            if 'api' in content.lower():
                capabilities.append('api_management')
            if 'data' in content.lower():
                capabilities.append('data_management')
            if 'strategy' in content.lower():
                capabilities.append('strategy_development')
            if 'portfolio' in content.lower():
                capabilities.append('portfolio_management')
            
            return capabilities if capabilities else ['general_purpose']
            
        except Exception:
            return ['general_purpose']
    
    def get_agent_status(self, agent_name: str) -> Dict:
        """Get status of a specific agent"""
        if agent_name in self.registered_agents:
            return {
                'name': agent_name,
                'status': self.agent_status.get(agent_name, 'unknown'),
                'info': self.registered_agents[agent_name],
                'last_seen': self.registered_agents[agent_name]['last_seen']
            }
        return {'error': 'Agent not found'}
    
    def get_all_agents_status(self) -> Dict:
        """Get status of all registered agents"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_agents': len(self.registered_agents),
            'agents': {
                name: {
                    'status': self.agent_status.get(name, 'unknown'),
                    'type': info['type'],
                    'capabilities': info['capabilities'],
                    'last_seen': info['last_seen']
                }
                for name, info in self.registered_agents.items()
            }
        }
    
    def send_message_to_agent(self, agent_name: str, message: Dict) -> bool:
        """Send a message to a specific agent"""
        try:
            if agent_name not in self.registered_agents:
                self.logger.warning(f"Agent {agent_name} not found")
                return False
            
            # Add message to queue
            message_entry = {
                'timestamp': datetime.now().isoformat(),
                'to': agent_name,
                'from': 'bridge',
                'message': message,
                'status': 'queued'
            }
            
            self.message_queue.append(message_entry)
            
            # Try to deliver message
            success = self._deliver_message_to_agent(agent_name, message)
            
            if success:
                message_entry['status'] = 'delivered'
                self.logger.info(f"Message delivered to {agent_name}")
            else:
                message_entry['status'] = 'failed'
                self.logger.warning(f"Failed to deliver message to {agent_name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending message to {agent_name}: {e}")
            return False
    
    def _deliver_message_to_agent(self, agent_name: str, message: Dict) -> bool:
        """Attempt to deliver a message to an agent"""
        try:
            agent_info = self.registered_agents[agent_name]
            agent_file = agent_info['file']
            
            # Try to import and communicate with the agent
            if self._is_agent_accessible(agent_file):
                # For now, we'll just log the message
                # In a full implementation, this would establish proper communication
                self.logger.info(f"Message queued for {agent_name}: {message}")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error delivering message to {agent_name}: {e}")
            return False
    
    def _is_agent_accessible(self, agent_file: str) -> bool:
        """Check if an agent file is accessible and importable"""
        try:
            # Try to import the agent module
            spec = importlib.util.spec_from_file_location("agent_module", agent_file)
            if spec and spec.loader:
                return True
            return False
        except Exception:
            return False
    
    def broadcast_message(self, message: Dict) -> Dict:
        """Broadcast a message to all agents"""
        try:
            results = {}
            
            for agent_name in self.registered_agents:
                success = self.send_message_to_agent(agent_name, message)
                results[agent_name] = 'sent' if success else 'failed'
            
            self.logger.info(f"Broadcast message sent to {len(results)} agents")
            return results
            
        except Exception as e:
            self.logger.error(f"Error broadcasting message: {e}")
            return {'error': str(e)}
    
    def execute_agent_command(self, agent_name: str, command: str, params: Dict = None) -> Dict:
        """Execute a command on a specific agent"""
        try:
            if agent_name not in self.registered_agents:
                return {'error': 'Agent not found'}
            
            # Record command
            command_entry = {
                'timestamp': datetime.now().isoformat(),
                'agent': agent_name,
                'command': command,
                'params': params,
                'status': 'executing'
            }
            
            self.command_history.append(command_entry)
            
            # Execute command based on agent type
            result = self._execute_command_on_agent(agent_name, command, params)
            
            command_entry['status'] = 'completed' if result.get('success') else 'failed'
            command_entry['result'] = result
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing command on {agent_name}: {e}")
            return {'error': str(e)}
    
    def _execute_command_on_agent(self, agent_name: str, command: str, params: Dict = None) -> Dict:
        """Execute a specific command on an agent"""
        try:
            agent_info = self.registered_agents[agent_name]
            agent_type = agent_info['type']
            
            # Handle different command types based on agent type
            if command == 'status':
                return self._get_agent_status_command(agent_name)
            elif command == 'restart':
                return self._restart_agent_command(agent_name)
            elif command == 'optimize':
                return self._optimize_agent_command(agent_name, params)
            elif command == 'report':
                return self._generate_agent_report_command(agent_name)
            else:
                return {'error': f'Unknown command: {command}'}
                
        except Exception as e:
            self.logger.error(f"Error executing command {command} on {agent_name}: {e}")
            return {'error': str(e)}
    
    def _get_agent_status_command(self, agent_name: str) -> Dict:
        """Get detailed status of an agent"""
        try:
            status = self.get_agent_status(agent_name)
            return {
                'success': True,
                'command': 'status',
                'agent': agent_name,
                'result': status
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _restart_agent_command(self, agent_name: str) -> Dict:
        """Restart an agent"""
        try:
            # Update agent status
            self.agent_status[agent_name] = 'restarting'
            
            # Simulate restart process
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

def main():
    """Test the agent integration bridge"""
    print("🌉 AGENT INTEGRATION BRIDGE - TESTING")
    print("=" * 60)
    
    # Create bridge
    bridge = AgentIntegrationBridge()
    
    # Get status
    status = bridge.get_bridge_status()
    print(f"Bridge Status: {status['status']}")
    print(f"Total Agents: {status['total_agents']}")
    print(f"Active Agents: {status['active_agents']}")
    
    # Test communication
    print("\n🧪 Testing agent communication...")
    
    # Broadcast test message
    test_message = {
        'type': 'test',
        'content': 'Hello from the bridge!',
        'timestamp': datetime.now().isoformat()
    }
    
    results = bridge.broadcast_message(test_message)
    print(f"Broadcast results: {results}")
    
    # Get detailed agent status
    print("\n📊 Agent Status:")
    for agent_name in bridge.registered_agents:
        agent_status = bridge.get_agent_status(agent_name)
        print(f"  {agent_name}: {agent_status['status']}")
    
    print("\n✅ Bridge testing completed")

if __name__ == "__main__":
    main()
