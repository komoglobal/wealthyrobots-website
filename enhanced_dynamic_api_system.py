#!/usr/bin/env python3
"""
Enhanced Dynamic API System with Intelligent Ranking
Includes Pact and Tinyman SDKs with smart endpoint selection
"""

import requests
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading

class EnhancedDynamicAPISystem:
    def __init__(self):
        # Tier 1: Premium APIs (Best performance, highest reliability)
        self.tier1_apis = {
            'algonode': {
                'algod': 'https://mainnet-api.algonode.cloud',
                'indexer': 'https://mainnet-idx.algonode.cloud',
                'priority': 1,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'features': ['high_reliability', 'fast_response', 'no_rate_limit'],
                'score': 0,
                'uptime': 0.99,
                'max_requests_per_second': 1000
            },
            'purestake': {
                'algod': 'https://mainnet-api.purestake.io',
                'indexer': 'https://mainnet-idx.purestake.io',
                'priority': 2,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'features': ['enterprise_grade', 'high_reliability', 'fast_response'],
                'score': 0,
                'uptime': 0.995,
                'max_requests_per_second': 2000
            }
        }
        
        # Tier 2: Good APIs (Reliable with some limitations)
        self.tier2_apis = {
            'nodely': {
                'algod': 'https://mainnet-api.4160.nodely.dev',
                'indexer': 'https://mainnet-idx.4160.nodely.dev',
                'priority': 3,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'features': ['free_tier', 'good_reliability', 'rate_limited'],
                'score': 0,
                'uptime': 0.95,
                'max_requests_per_second': 100
            },
            'algorand_foundation': {
                'algod': 'https://mainnet-api.algorand.cloud',
                'indexer': 'https://mainnet-idx.algorand.cloud',
                'priority': 4,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'features': ['official', 'stable', 'rate_limited'],
                'score': 0,
                'uptime': 0.98,
                'max_requests_per_second': 500
            }
        }
        
        # DeFi Protocol APIs
        self.defi_apis = {
            'pact': {
                'name': 'Pact Finance',
                'api_url': 'https://api.pact.fi',
                'priority': 1,
                'features': ['yield_farming', 'liquidity_pools', 'swaps'],
                'score': 0,
                'last_check': None,
                'status': 'unknown'
            },
            'tinyman': {
                'name': 'Tinyman',
                'api_url': 'https://api.tinyman.org',
                'priority': 2,
                'features': ['amm', 'liquidity_pools', 'swaps'],
                'score': 0,
                'last_check': None,
                'status': 'unknown'
            }
        }
        
        self.current_primary = 'algonode'
        self.current_backup = 'purestake'
        self.health_check_interval = 300  # 5 minutes
        self.last_health_check = None
        self.ranking_lock = threading.Lock()
        
        print("🚀 Enhanced Dynamic API System Initialized")
        print(f"📡 Primary: {self.current_primary} (Tier 1)")
        print(f"🔄 Backup: {self.current_backup} (Tier 1)")
        print("🎯 DeFi Protocols: Pact, Tinyman")
    
    def calculate_api_score(self, api_data: Dict) -> float:
        """Calculate comprehensive API score based on multiple factors"""
        score = 0.0
        
        # Base score from tier
        if api_data in self.tier1_apis.values():
            score += 100  # Tier 1 bonus
        elif api_data in self.tier2_apis.values():
            score += 50   # Tier 2 bonus
        
        # Response time scoring (faster = higher score)
        if api_data.get('response_time'):
            response_time = api_data['response_time']
            if response_time < 0.1:
                score += 30
            elif response_time < 0.5:
                score += 20
            elif response_time < 1.0:
                score += 10
        
        # Uptime scoring
        uptime = api_data.get('uptime', 0.9)
        score += uptime * 50
        
        # Feature scoring
        features = api_data.get('features', [])
        if 'high_reliability' in features:
            score += 25
        if 'fast_response' in features:
            score += 20
        if 'no_rate_limit' in features:
            score += 15
        if 'enterprise_grade' in features:
            score += 20
        
        # Status scoring
        if api_data.get('status') == 'healthy':
            score += 50
        elif api_data.get('status') == 'degraded':
            score += 25
        
        # Priority scoring (lower number = higher priority)
        priority = api_data.get('priority', 10)
        score += (10 - priority) * 5
        
        return score
    
    def health_check_endpoint(self, name: str, endpoint_data: Dict) -> Dict:
        """Enhanced health check with comprehensive metrics"""
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
            
            # Determine status based on both endpoints
            if algod_status and indexer_status:
                status = 'healthy'
            elif algod_status or indexer_status:
                status = 'degraded'
            else:
                status = 'down'
            
            # Calculate score
            endpoint_data.update({
                'status': status,
                'response_time': response_time,
                'last_check': datetime.now(),
                'algod_ok': algod_status,
                'indexer_ok': indexer_status
            })
            
            endpoint_data['score'] = self.calculate_api_score(endpoint_data)
            
            return endpoint_data
            
        except Exception as e:
            endpoint_data.update({
                'status': 'down',
                'response_time': None,
                'last_check': datetime.now(),
                'error': str(e),
                'algod_ok': False,
                'indexer_ok': False,
                'score': 0
            })
            return endpoint_data
    
    def perform_health_check(self) -> None:
        """Perform comprehensive health check on all endpoints"""
        if (self.last_health_check and 
            datetime.now() - self.last_health_check < timedelta(seconds=self.health_check_interval)):
            return
        
        print("🏥 Performing comprehensive endpoint health check...")
        print("=" * 60)
        
        # Check Tier 1 APIs
        print("🥇 TIER 1 APIs (Premium):")
        for name, endpoint_data in self.tier1_apis.items():
            health = self.health_check_endpoint(name, endpoint_data)
            self.tier1_apis[name] = health
            
            status_emoji = "✅" if health['status'] == 'healthy' else "⚠️" if health['status'] == 'degraded' else "❌"
            print(f"   {status_emoji} {name}: {health['status']} | Score: {health['score']:.1f} | Response: {health.get('response_time', 'N/A'):.3f}s")
        
        # Check Tier 2 APIs
        print("\n🥈 TIER 2 APIs (Standard):")
        for name, endpoint_data in self.tier2_apis.items():
            health = self.health_check_endpoint(name, endpoint_data)
            self.tier2_apis[name] = health
            
            status_emoji = "✅" if health['status'] == 'healthy' else "⚠️" if health['status'] == 'degraded' else "❌"
            print(f"   {status_emoji} {name}: {health['status']} | Score: {health['score']:.1f} | Response: {health.get('response_time', 'N/A'):.3f}s")
        
        # Check DeFi APIs
        print("\n🏦 DeFi Protocol APIs:")
        for name, api_data in self.defi_apis.items():
            try:
                # Simple health check for DeFi APIs
                response = requests.get(f"{api_data['api_url']}/health", timeout=5)
                status = 'healthy' if response.status_code == 200 else 'degraded'
                score = 100 if status == 'healthy' else 50
            except:
                status = 'down'
                score = 0
            
            api_data.update({
                'status': status,
                'score': score,
                'last_check': datetime.now()
            })
            
            status_emoji = "✅" if status == 'healthy' else "⚠️" if status == 'degraded' else "❌"
            print(f"   {status_emoji} {api_data['name']}: {status} | Score: {score}")
        
        self.last_health_check = datetime.now()
        self._update_primary_endpoints()
    
    def _update_primary_endpoints(self) -> None:
        """Update primary and backup endpoints based on comprehensive scoring"""
        with self.ranking_lock:
            # Combine all APIs and sort by score
            all_apis = {**self.tier1_apis, **self.tier2_apis}
            healthy_apis = [(name, data) for name, data in all_apis.items() if data['status'] == 'healthy']
            
            if not healthy_apis:
                print("❌ No healthy endpoints available!")
                return
            
            # Sort by score (highest first), then by response time, then by priority
            healthy_apis.sort(key=lambda x: (
                -x[1]['score'],  # Higher score first
                x[1].get('response_time', float('inf')),  # Lower response time first
                x[1]['priority']  # Lower priority number first
            ))
            
            new_primary = healthy_apis[0][0]
            new_backup = healthy_apis[1][0] if len(healthy_apis) > 1 else healthy_apis[0][0]
            
            if new_primary != self.current_primary:
                print(f"\n🔄 Switching primary endpoint: {self.current_primary} → {new_primary}")
                print(f"   Reason: Higher score ({all_apis[new_primary]['score']:.1f} vs {all_apis[self.current_primary]['score']:.1f})")
                self.current_primary = new_primary
            
            if new_backup != self.current_backup:
                print(f"🔄 Switching backup endpoint: {self.current_backup} → {new_backup}")
                self.current_backup = new_backup
    
    def get_current_endpoints(self) -> Tuple[str, str]:
        """Get current primary and backup endpoints"""
        self.perform_health_check()
        
        primary = self.tier1_apis.get(self.current_primary) or self.tier2_apis.get(self.current_primary)
        backup = self.tier1_apis.get(self.current_backup) or self.tier2_apis.get(self.current_backup)
        
        if not primary or not backup:
            print("❌ No valid endpoints available!")
            return None, None
        
        return primary['algod'], primary['indexer']
    
    def get_endpoint_status(self) -> Dict:
        """Get comprehensive endpoint status"""
        return {
            'primary': {
                'name': self.current_primary,
                'algod': self.tier1_apis.get(self.current_primary, {}).get('algod') or 
                         self.tier2_apis.get(self.current_primary, {}).get('algod'),
                'indexer': self.tier1_apis.get(self.current_primary, {}).get('indexer') or 
                           self.tier2_apis.get(self.current_primary, {}).get('indexer'),
                'status': self.tier1_apis.get(self.current_primary, {}).get('status') or 
                          self.tier2_apis.get(self.current_primary, {}).get('status'),
                'score': self.tier1_apis.get(self.current_primary, {}).get('score') or 
                         self.tier2_apis.get(self.current_primary, {}).get('score')
            },
            'backup': {
                'name': self.current_backup,
                'algod': self.tier1_apis.get(self.current_backup, {}).get('algod') or 
                         self.tier2_apis.get(self.current_backup, {}).get('algod'),
                'indexer': self.tier1_apis.get(self.current_backup, {}).get('indexer') or 
                           self.tier2_apis.get(self.current_backup, {}).get('indexer'),
                'status': self.tier1_apis.get(self.current_backup, {}).get('status') or 
                          self.tier2_apis.get(self.current_backup, {}).get('status'),
                'score': self.tier1_apis.get(self.current_backup, {}).get('score') or 
                         self.tier2_apis.get(self.current_backup, {}).get('score')
            },
            'tier1_apis': self.tier1_apis,
            'tier2_apis': self.tier2_apis,
            'defi_apis': self.defi_apis
        }
    
    def get_best_defi_protocol(self) -> str:
        """Get the best performing DeFi protocol"""
        healthy_protocols = [(name, data) for name, data in self.defi_apis.items() if data['status'] == 'healthy']
        
        if not healthy_protocols:
            return None
        
        # Sort by score and priority
        healthy_protocols.sort(key=lambda x: (-x[1]['score'], x[1]['priority']))
        return healthy_protocols[0][0]
    
    def test_connection(self) -> bool:
        """Test current connection with detailed feedback"""
        try:
            algod_url, indexer_url = self.get_current_endpoints()
            
            if not algod_url:
                print("❌ No valid endpoints available")
                return False
            
            print(f"🔗 Testing connection to: {algod_url}")
            
            response = requests.get(f"{algod_url}/v2/status", timeout=10)
            if response.status_code == 200:
                network_info = response.json()
                print(f"✅ Connected! Last Round: {network_info.get('last-round', 'N/A')}")
                
                # Show current ranking
                status = self.get_endpoint_status()
                print(f"\n📊 Current API Ranking:")
                print(f"   🥇 Primary: {status['primary']['name']} (Score: {status['primary']['score']:.1f})")
                print(f"   🥈 Backup: {status['backup']['name']} (Score: {status['backup']['score']:.1f})")
                
                return True
            else:
                print(f"❌ Connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

def main():
    """Test the enhanced dynamic API system"""
    api = EnhancedDynamicAPISystem()
    
    print("\n🧪 Testing Enhanced Dynamic API System...")
    print("=" * 60)
    
    # Test connection
    if api.test_connection():
        print("✅ Enhanced API system working!")
        
        # Show comprehensive status
        status = api.get_endpoint_status()
        print(f"\n📊 Comprehensive Status:")
        print(f"   Primary: {status['primary']['name']} ({status['primary']['status']})")
        print(f"   Backup: {status['backup']['name']} ({status['backup']['status']})")
        
        # Show DeFi protocol status
        best_protocol = api.get_best_defi_protocol()
        if best_protocol:
            print(f"   🏆 Best DeFi Protocol: {best_protocol}")
        
        # Show all endpoints with scores
        print(f"\n🌐 All Endpoints (Ranked by Score):")
        all_apis = {**status['tier1_apis'], **status['tier2_apis']}
        sorted_apis = sorted(all_apis.items(), key=lambda x: -x[1]['score'])
        
        for name, data in sorted_apis:
            tier = "🥇" if data in status['tier1_apis'].values() else "🥈"
            status_emoji = "✅" if data['status'] == 'healthy' else "⚠️" if data['status'] == 'degraded' else "❌"
            print(f"   {tier} {name}: {data['status']} | Score: {data['score']:.1f}")
    else:
        print("❌ Enhanced API system failed!")

if __name__ == "__main__":
    main()



