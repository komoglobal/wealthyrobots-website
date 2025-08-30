#!/usr/bin/env python3
"""
Agent Coordination System - WealthyRobot
Coordinates all trading agents and manages the autonomous trading empire
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
import yaml
import threading
from dataclasses import dataclass
import importlib.util

@dataclass
class AgentStatus:
    """Represents the status of an agent"""
    name: str
    status: str  # 'running', 'stopped', 'error'
    last_heartbeat: datetime
    performance_metrics: Dict[str, Any]
    error_count: int
    uptime: timedelta

class AgentCoordinator:
    """Coordinates all trading agents"""
    
    def __init__(self):
        self.name = "WealthyRobot Agent Coordinator"
        self.version = "1.0.0"
        self.running = True
        
        # Agent registry
        self.agents = {}
        self.agent_status = {}
        
        # Performance tracking
        self.total_opportunities = 0
        self.total_trades = 0
        self.successful_trades = 0
        self.start_time = datetime.now()
        
        # Setup logging
        self._setup_logging()
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Discover and register agents
        self._discover_agents()
        
        self.logger.info(f"🌉 {self.name} v{self.version} - INITIALIZED")
        self.logger.info(f"🤖 Registered Agents: {len(self.agents)}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def _setup_logging(self):
        """Setup logging system"""
        os.makedirs('logs', exist_ok=True)
        
        log_file = f'logs/agent_coordinator_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('AgentCoordinator')
    
    def _discover_agents(self):
        """Discover and register available agents"""
        try:
            self.logger.info("🔍 Discovering available agents...")
            
            # Known agent files to look for
            agent_files = [
                "autonomous_trading_empire.py",
                "real_defi_integration.py",
                "unified_trading_system.py",
                "multi_protocol_trading_system.py",
                "agent_integration_bridge_optimized.py"
            ]
            
            for agent_file in agent_files:
                if os.path.exists(agent_file):
                    self._register_agent(agent_file)
            
            # Also look for any Python files that might be agents
            for file in os.listdir('.'):
                if file.endswith('.py') and 'agent' in file.lower() and file not in agent_files:
                    self._register_agent(file)
            
            self.logger.info(f"✅ Discovered {len(self.agents)} agents")
            
        except Exception as e:
            self.logger.error(f"❌ Error discovering agents: {e}")
    
    def _register_agent(self, agent_file: str):
        """Register an agent"""
        try:
            agent_name = agent_file.replace('.py', '').replace('_', ' ').title()
            
            self.agents[agent_name] = {
                'file': agent_file,
                'status': 'discovered',
                'last_heartbeat': datetime.now(),
                'performance_metrics': {},
                'error_count': 0
            }
            
            self.logger.info(f"✅ Registered agent: {agent_name}")
            
        except Exception as e:
            self.logger.error(f"❌ Error registering agent {agent_file}: {e}")
    
    async def start_agent(self, agent_name: str) -> bool:
        """Start an agent"""
        try:
            if agent_name not in self.agents:
                self.logger.error(f"❌ Agent {agent_name} not found")
                return False
            
            agent_info = self.agents[agent_name]
            agent_file = agent_info['file']
            
            self.logger.info(f"🚀 Starting agent: {agent_name}")
            
            # Start agent in a separate process
            process = await asyncio.create_subprocess_exec(
                'python3', agent_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Store process reference
            agent_info['process'] = process
            agent_info['status'] = 'starting'
            
            # Wait a bit for startup
            await asyncio.sleep(5)
            
            # Check if process is still running
            if process.returncode is None:
                agent_info['status'] = 'running'
                agent_info['start_time'] = datetime.now()
                self.logger.info(f"✅ Agent {agent_name} started successfully")
                return True
            else:
                agent_info['status'] = 'error'
                agent_info['error_count'] += 1
                self.logger.error(f"❌ Agent {agent_name} failed to start")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error starting agent {agent_name}: {e}")
            if agent_name in self.agents:
                self.agents[agent_name]['status'] = 'error'
                self.agents[agent_name]['error_count'] += 1
            return False
    
    async def stop_agent(self, agent_name: str) -> bool:
        """Stop an agent"""
        try:
            if agent_name not in self.agents:
                self.logger.error(f"❌ Agent {agent_name} not found")
                return False
            
            agent_info = self.agents[agent_name]
            
            if 'process' in agent_info and agent_info['process']:
                self.logger.info(f"🛑 Stopping agent: {agent_name}")
                
                # Terminate process
                agent_info['process'].terminate()
                
                # Wait for termination
                try:
                    await asyncio.wait_for(agent_info['process'].wait(), timeout=10)
                except asyncio.TimeoutError:
                    # Force kill if needed
                    agent_info['process'].kill()
                
                agent_info['status'] = 'stopped'
                self.logger.info(f"✅ Agent {agent_name} stopped")
                return True
            else:
                self.logger.warning(f"⚠️ Agent {agent_name} not running")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error stopping agent {agent_name}: {e}")
            return False
    
    async def restart_agent(self, agent_name: str) -> bool:
        """Restart an agent"""
        try:
            self.logger.info(f"🔄 Restarting agent: {agent_name}")
            
            # Stop first
            if await self.stop_agent(agent_name):
                await asyncio.sleep(2)  # Wait a bit
                
                # Start again
                return await self.start_agent(agent_name)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error restarting agent {agent_name}: {e}")
            return False
    
    async def monitor_agents(self):
        """Monitor all agents for health and performance"""
        while self.running:
            try:
                self.logger.info("📊 Monitoring agent health...")
                
                for agent_name, agent_info in self.agents.items():
                    # Check agent status
                    if agent_info['status'] == 'running':
                        # Check if process is still alive
                        if 'process' in agent_info and agent_info['process']:
                            if agent_info['process'].returncode is not None:
                                # Process died
                                agent_info['status'] = 'error'
                                agent_info['error_count'] += 1
                                self.logger.warning(f"⚠️ Agent {agent_name} process died")
                                
                                # Auto-restart if error count < 3
                                if agent_info['error_count'] < 3:
                                    self.logger.info(f"🔄 Auto-restarting agent {agent_name}")
                                    await self.restart_agent(agent_name)
                    
                    # Update uptime
                    if 'start_time' in agent_info:
                        agent_info['uptime'] = datetime.now() - agent_info['start_time']
                    
                    # Update last heartbeat
                    agent_info['last_heartbeat'] = datetime.now()
                
                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"❌ Error in agent monitoring: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def coordinate_trading_activities(self):
        """Coordinate trading activities across all agents"""
        while self.running:
            try:
                self.logger.info("🎯 Coordinating trading activities...")
                
                # Get status of all agents
                running_agents = [name for name, info in self.agents.items() if info['status'] == 'running']
                
                if len(running_agents) < 2:
                    self.logger.warning("⚠️ Insufficient agents running, starting more...")
                    
                    # Start key agents if not running
                    key_agents = ['autonomous_trading_empire', 'real_defi_integration']
                    
                    for agent in key_agents:
                        if agent not in running_agents:
                            await self.start_agent(agent)
                
                # Coordinate opportunity sharing
                await self._share_opportunities()
                
                # Coordinate risk management
                await self._coordinate_risk_management()
                
                # Wait before next coordination
                await asyncio.sleep(60)  # Coordinate every minute
                
            except Exception as e:
                self.logger.error(f"❌ Error in trading coordination: {e}")
                await asyncio.sleep(120)  # Wait longer on error
    
    async def _share_opportunities(self):
        """Share opportunities between agents"""
        try:
            # This would implement opportunity sharing logic
            # For now, just log that we're sharing
            self.logger.info("📤 Sharing opportunities between agents...")
            
        except Exception as e:
            self.logger.error(f"❌ Error sharing opportunities: {e}")
    
    async def _coordinate_risk_management(self):
        """Coordinate risk management across agents"""
        try:
            # This would implement risk coordination logic
            # For now, just log that we're coordinating
            self.logger.info("🛡️ Coordinating risk management...")
            
        except Exception as e:
            self.logger.error(f"❌ Error coordinating risk management: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        running_agents = [name for name, info in self.agents.items() if info['status'] == 'running']
        error_agents = [name for name, info in self.agents.items() if info['status'] == 'error']
        
        return {
            'name': self.name,
            'version': self.version,
            'status': 'running' if self.running else 'stopped',
            'uptime': str(datetime.now() - self.start_time),
            'total_agents': len(self.agents),
            'running_agents': len(running_agents),
            'error_agents': len(error_agents),
            'agent_status': {name: info['status'] for name, info in self.agents.items()},
            'total_opportunities': self.total_opportunities,
            'total_trades': self.total_trades,
            'successful_trades': self.successful_trades,
            'success_rate': self.successful_trades / max(self.total_trades, 1)
        }
    
    async def run(self):
        """Main coordination loop"""
        self.logger.info("🚀 Starting agent coordination system...")
        
        try:
            # Start monitoring and coordination tasks
            tasks = [
                self.monitor_agents(),
                self.coordinate_trading_activities()
            ]
            
            # Start key agents
            key_agents = ['autonomous_trading_empire', 'real_defi_integration']
            for agent in key_agents:
                if agent in self.agents:
                    await self.start_agent(agent)
            
            # Run coordination tasks
            await asyncio.gather(*tasks)
            
        except Exception as e:
            self.logger.error(f"❌ Fatal error in coordination system: {e}")
        finally:
            self.logger.info("🛑 Agent coordination system shutdown complete")

async def main():
    """Main entry point"""
    coordinator = AgentCoordinator()
    
    try:
        # Run the coordinator
        await coordinator.run()
        
    except KeyboardInterrupt:
        coordinator.logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        coordinator.logger.error(f"Fatal error: {e}")
    finally:
        coordinator.running = False

if __name__ == "__main__":
    asyncio.run(main())
