#!/usr/bin/env python3
"""
Dynamic Algorand API System
Automatically switches between multiple endpoints for optimal performance and security
"""

import requests
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class DynamicAlgorandAPI:
    def __init__(self):
        self.endpoints = {
            'algonode': {
                'algod': 'https://mainnet-api.algonode.cloud',
                'indexer': 'https://mainnet-idx.algonode.cloud',
                'priority': 1,
                'last_check': None,
                'status': 'unknown',
                'response_time': None
            },
            'nodely': {
                'algod': 'https://mainnet-api.4160.nodely.dev',
                'indexer': 'https://mainnet-idx.4160.nodely.dev',
                'priority': 2,
                'last_check': None,
                'status': 'unknown',
                'response_time': None
            },
            'purestake': {
                'algod': 'https://mainnet-api.purestake.io',
                'indexer': 'https://mainnet-idx.purestake.io',
                'priority': 3,
                'last_check': None,
                'status': 'unknown',
                'response_time': None
            },
            'algorand_foundation': {
                'algod': 'https://mainnet-api.algorand.cloud',
                'indexer': 'https://mainnet-idx.algorand.cloud',
                'priority': 4,
                'last_check': None,
                'status': 'unknown',
                'response_time': None
            }
        }
        
        self.current_primary = 'algonode'
        self.current_backup = 'nodely'
        self.health_check_interval = 300  # 5 minutes
        self.last_health_check = None
        
        print("🚀 Dynamic Algorand API System Initialized")
        print(f"📡 Primary: {self.current_primary}")
        print(f"🔄 Backup: {self.current_backup}")
    
    def health_check_endpoint(self, name: str, endpoint_data: Dict) -> Dict:
        """Check health of a specific endpoint"""
        try:
            start_time = time.time()
            
            # Test algod endpoint
            algod_response = requests.get(f"{endpoint_data['algod']}/v2/status", timeout=10)
            algod_status = algod_response.status_code == 200
            
            # Test indexer endpoint
            try:
                indexer_response = requests.get(f"{endpoint_data['indexer']}/v2/health", timeout=10)
                indexer_status = indexer_response.status_code == 200
            except:
                indexer_status = False
            
            response_time = time.time() - start_time
            
            status = 'healthy' if (algod_status and indexer_status) else 'degraded' if algod_status else 'down'
            
            return {
                'status': status,
                'response_time': response_time,
                'last_check': datetime.now(),
                'algod_ok': algod_status,
                'indexer_ok': indexer_status
            }
            
        except Exception as e:
            return {
                'status': 'down',
                'response_time': None,
                'last_check': datetime.now(),
                'error': str(e),
                'algod_ok': False,
                'indexer_ok': False
            }
    
    def perform_health_check(self) -> None:
        """Perform health check on all endpoints"""
        if (self.last_health_check and 
            datetime.now() - self.last_health_check < timedelta(seconds=self.health_check_interval)):
            return
        
        print("🏥 Performing endpoint health check...")
        
        for name, endpoint_data in self.endpoints.items():
            health = self.health_check_endpoint(name, endpoint_data)
            self.endpoints[name].update(health)
            
            status_emoji = "✅" if health['status'] == 'healthy' else "⚠️" if health['status'] == 'degraded' else "❌"
            response_time = health.get('response_time')
            response_str = f"{response_time:.3f}s" if response_time is not None else "N/A"
            print(f"   {status_emoji} {name}: {health['status']} ({response_str})")
        
        self.last_health_check = datetime.now()
        self._update_primary_endpoints()
    
    def _update_primary_endpoints(self) -> None:
        """Update primary and backup endpoints based on health and performance"""
        healthy_endpoints = []
        
        for name, data in self.endpoints.items():
            if data['status'] == 'healthy':
                healthy_endpoints.append((name, data))
        
        if not healthy_endpoints:
            print("❌ No healthy endpoints available!")
            return
        
        # Sort by response time and priority
        healthy_endpoints.sort(key=lambda x: (x[1]['response_time'] or float('inf'), x[1]['priority']))
        
        new_primary = healthy_endpoints[0][0]
        new_backup = healthy_endpoints[1][0] if len(healthy_endpoints) > 1 else healthy_endpoints[0][0]
        
        if new_primary != self.current_primary:
            print(f"🔄 Switching primary endpoint: {self.current_primary} → {new_primary}")
            self.current_primary = new_primary
        
        if new_backup != self.current_backup:
            print(f"🔄 Switching backup endpoint: {self.current_backup} → {new_backup}")
            self.current_backup = new_backup
    
    def get_current_endpoints(self) -> Tuple[str, str]:
        """Get current primary and backup endpoints"""
        self.perform_health_check()
        
        primary = self.endpoints[self.current_primary]
        backup = self.endpoints[self.current_backup]
        
        return primary['algod'], primary['indexer']
    
    def get_endpoint_status(self) -> Dict:
        """Get current endpoint status"""
        return {
            'primary': {
                'name': self.current_primary,
                'algod': self.endpoints[self.current_primary]['algod'],
                'indexer': self.endpoints[self.current_primary]['indexer'],
                'status': self.endpoints[self.current_primary]['status']
            },
            'backup': {
                'name': self.current_backup,
                'algod': self.endpoints[self.current_backup]['algod'],
                'indexer': self.endpoints[self.current_backup]['indexer'],
                'status': self.endpoints[self.current_backup]['status']
            },
            'all_endpoints': self.endpoints
        }
    
    def test_connection(self) -> bool:
        """Test current connection"""
        try:
            algod_url, indexer_url = self.get_current_endpoints()
            
            print(f"🔗 Testing connection to: {algod_url}")
            
            response = requests.get(f"{algod_url}/v2/status", timeout=10)
            if response.status_code == 200:
                network_info = response.json()
                print(f"✅ Connected! Last Round: {network_info.get('last-round', 'N/A')}")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

def main():
    """Test the dynamic API system"""
    api = DynamicAlgorandAPI()
    
    print("\n🧪 Testing Dynamic API System...")
    print("=" * 50)
    
    # Test connection
    if api.test_connection():
        print("✅ Dynamic API system working!")
        
        # Show status
        status = api.get_endpoint_status()
        print(f"\n📊 Current Status:")
        print(f"   Primary: {status['primary']['name']} ({status['primary']['status']})")
        print(f"   Backup: {status['backup']['name']} ({status['backup']['status']})")
        
        # Show all endpoints
        print(f"\n🌐 All Endpoints:")
        for name, data in status['all_endpoints'].items():
            emoji = "✅" if data['status'] == 'healthy' else "⚠️" if data['status'] == 'degraded' else "❌"
            print(f"   {emoji} {name}: {data['status']}")
    else:
        print("❌ Dynamic API system failed!")

if __name__ == "__main__":
    main()
