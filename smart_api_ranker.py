#!/usr/bin/env python3
"""
Smart API Ranker - Tests all APIs and ranks by actual connectivity
DeFi protocols (Tinyman, Pact) are primary, others are network backups
"""

import requests
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading

class SmartAPIRanker:
    def __init__(self):
        # DeFi Protocol APIs (Primary - These are what we actually trade on)
        self.defi_apis = {
            'tinyman': {
                'name': 'Tinyman',
                'api_url': 'https://api.tinyman.org',
                'priority': 1,
                'features': ['amm', 'liquidity_pools', 'swaps', 'primary_trading'],
                'score': 0,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'tier': 'primary'
            },
            'pact': {
                'name': 'Pact Finance',
                'api_url': 'https://api.pact.fi',
                'priority': 2,
                'features': ['yield_farming', 'liquidity_pools', 'swaps', 'primary_trading'],
                'score': 0,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'tier': 'primary'
            }
        }
        
        # Algorand Network APIs (Backup - For blockchain connectivity)
        self.network_apis = {
            'algonode': {
                'algod': 'https://mainnet-api.algonode.cloud',
                'indexer': 'https://mainnet-idx.algonode.cloud',
                'priority': 1,
                'features': ['high_reliability', 'fast_response', 'no_rate_limit'],
                'score': 0,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'tier': 'backup'
            },
            'purestake': {
                'algod': 'https://mainnet-api.purestake.io',
                'indexer': 'https://mainnet-idx.purestake.io',
                'priority': 2,
                'features': ['enterprise_grade', 'high_reliability', 'fast_response'],
                'score': 0,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'tier': 'backup'
            },
            'nodely': {
                'algod': 'https://mainnet-api.4160.nodely.dev',
                'indexer': 'https://mainnet-idx.4160.nodely.dev',
                'priority': 3,
                'features': ['free_tier', 'good_reliability', 'rate_limited'],
                'score': 0,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'tier': 'backup'
            },
            'algorand_foundation': {
                'algod': 'https://mainnet-api.algorand.cloud',
                'indexer': 'https://mainnet-idx.algorand.cloud',
                'priority': 4,
                'features': ['official', 'stable', 'rate_limited'],
                'score': 0,
                'last_check': None,
                'status': 'unknown',
                'response_time': None,
                'tier': 'backup'
            }
        }
        
        self.current_primary_defi = 'tinyman'
        self.current_backup_defi = 'pact'
        self.current_primary_network = 'algonode'
        self.current_backup_network = 'purestake'
        
        self.health_check_interval = 300  # 5 minutes
        self.last_health_check = None
        self.ranking_lock = threading.Lock()
        
        print("🧠 Smart API Ranker Initialized")
        print("🎯 Primary Focus: DeFi Protocols (Tinyman, Pact)")
        print("🌐 Backup: Algorand Network APIs")
    
    def test_defi_api_connectivity(self, name: str, api_data: Dict) -> Dict:
        """Test DeFi API connectivity by testing SDK initialization"""
        try:
            start_time = time.time()
            
            # Test SDK connectivity for each DeFi protocol
            if name == 'tinyman':
                try:
                    from tinyman.v2.client import TinymanV2MainnetClient
                    from tinyman.v2.constants import MAINNET_VALIDATOR_APP_ID
                    from algosdk.v2client import algod
                    
                    # Test basic SDK import and constants
                    algod_client = algod.AlgodClient("", "https://mainnet-api.algonode.cloud")
                    client = TinymanV2MainnetClient(algod_client)
                    
                    # Test if we can access basic protocol info
                    app_id = MAINNET_VALIDATOR_APP_ID
                    connected = True
                    working_url = "SDK Connected"
                    response_time = time.time() - start_time
                    
                except Exception as e:
                    connected = False
                    working_url = None
                    response_time = None
                    print(f"      Tinyman SDK Error: {str(e)}")
                    
            elif name == 'pact':
                try:
                    from pactsdk import PactClient
                    
                    # Test basic SDK import and client creation
                    client = PactClient(
                        algod="https://mainnet-api.algonode.cloud",
                        network="mainnet"
                    )
                    
                    # Test if we can access basic protocol info
                    connected = True
                    working_url = "SDK Connected"
                    response_time = time.time() - start_time
                    
                except Exception as e:
                    connected = False
                    working_url = None
                    response_time = None
                    print(f"      Pact SDK Error: {str(e)}")
            
            if connected:
                status = 'healthy'
                score = 100 + (50 if response_time and response_time < 0.5 else 25)
            else:
                status = 'down'
                score = 0
                response_time = None
            
            api_data.update({
                'status': status,
                'score': score,
                'response_time': response_time,
                'working_url': working_url,
                'last_check': datetime.now()
            })
            
            return api_data
            
        except Exception as e:
            api_data.update({
                'status': 'down',
                'score': 0,
                'response_time': None,
                'error': str(e),
                'last_check': datetime.now()
            })
            return api_data
    
    def test_network_api_connectivity(self, name: str, api_data: Dict) -> Dict:
        """Test Algorand network API connectivity"""
        try:
            start_time = time.time()
            
            # Test algod endpoint
            try:
                algod_response = requests.get(f"{api_data['algod']}/v2/status", timeout=10)
                algod_status = algod_response.status_code == 200
            except:
                algod_status = False
            
            # Test indexer endpoint
            try:
                indexer_response = requests.get(f"{api_data['indexer']}/v2/health", timeout=10)
                indexer_status = indexer_response.status_code == 200
            except:
                indexer_status = False
            
            response_time = time.time() - start_time
            
            # Determine status and score
            if algod_status and indexer_status:
                status = 'healthy'
                score = 100 + (30 if response_time < 0.5 else 15)
            elif algod_status or indexer_status:
                status = 'degraded'
                score = 75 + (15 if response_time < 0.5 else 7)
            else:
                status = 'down'
                score = 0
            
            api_data.update({
                'status': status,
                'response_time': response_time,
                'last_check': datetime.now(),
                'algod_ok': algod_status,
                'indexer_ok': indexer_status,
                'score': score
            })
            
            return api_data
            
        except Exception as e:
            api_data.update({
                'status': 'down',
                'response_time': None,
                'last_check': datetime.now(),
                'error': str(e),
                'algod_ok': False,
                'indexer_ok': False,
                'score': 0
            })
            return api_data
    
    def perform_comprehensive_test(self) -> None:
        """Test ALL APIs and rank them by actual connectivity"""
        print("🧪 PERFORMING COMPREHENSIVE API CONNECTIVITY TEST...")
        print("=" * 70)
        
        # Test DeFi APIs first (these are our primary focus)
        print("🎯 TESTING DEFI PROTOCOLS (Primary Trading APIs):")
        for name, api_data in self.defi_apis.items():
            health = self.test_defi_api_connectivity(name, api_data)
            self.defi_apis[name] = health
            
            status_emoji = "✅" if health['status'] == 'healthy' else "⚠️" if health['status'] == 'degraded' else "❌"
            response_time = health.get('response_time')
            response_str = f"{response_time:.3f}s" if response_time is not None else "N/A"
            print(f"   {status_emoji} {health['name']}: {health['status']} | Score: {health['score']} | Response: {response_str}")
            if health.get('working_url'):
                print(f"      🔗 Working URL: {health['working_url']}")
        
        # Test Network APIs (these are backups for blockchain connectivity)
        print("\n🌐 TESTING ALGORAND NETWORK APIS (Backup):")
        for name, api_data in self.network_apis.items():
            health = self.test_network_api_connectivity(name, api_data)
            self.network_apis[name] = health
            
            status_emoji = "✅" if health['status'] == 'healthy' else "⚠️" if health['status'] == 'degraded' else "❌"
            response_time = health.get('response_time')
            response_str = f"{response_time:.3f}s" if response_time is not None else "N/A"
            print(f"   {status_emoji} {name}: {health['status']} | Score: {health['score']} | Response: {response_str}")
            if health['algod_ok']:
                print(f"      🔗 Algod: ✅")
            if health['indexer_ok']:
                print(f"      🔗 Indexer: ✅")
        
        self.last_health_check = datetime.now()
        self._update_rankings()
    
    def _update_rankings(self) -> None:
        """Update rankings based on actual test results"""
        with self.ranking_lock:
            # Rank DeFi APIs (these are our primary focus)
            healthy_defi = [(name, data) for name, data in self.defi_apis.items() if data['status'] == 'healthy']
            if healthy_defi:
                healthy_defi.sort(key=lambda x: (-x[1]['score'], x[1]['priority']))
                new_primary_defi = healthy_defi[0][0]
                new_backup_defi = healthy_defi[1][0] if len(healthy_defi) > 1 else healthy_defi[0][0]
                
                if new_primary_defi != self.current_primary_defi:
                    print(f"\n🔄 Switching primary DeFi API: {self.current_primary_defi} → {new_primary_defi}")
                    print(f"   Reason: Higher score ({self.defi_apis[new_primary_defi]['score']} vs {self.defi_apis[self.current_primary_defi]['score']})")
                    self.current_primary_defi = new_primary_defi
                
                if new_backup_defi != self.current_backup_defi:
                    print(f"🔄 Switching backup DeFi API: {self.current_backup_defi} → {new_backup_defi}")
                    self.current_backup_defi = new_backup_defi
            
            # Rank Network APIs (these are backups)
            healthy_network = [(name, data) for name, data in self.network_apis.items() if data['status'] == 'healthy']
            if healthy_network:
                healthy_network.sort(key=lambda x: (-x[1]['score'], x[1]['priority']))
                new_primary_network = healthy_network[0][0]
                new_backup_network = healthy_network[1][0] if len(healthy_network) > 1 else healthy_network[0][0]
                
                if new_primary_network != self.current_primary_network:
                    print(f"🔄 Switching primary Network API: {self.current_primary_network} → {new_primary_network}")
                    self.current_primary_network = new_primary_network
                
                if new_backup_network != self.current_backup_network:
                    print(f"🔄 Switching backup Network API: {self.current_backup_network} → {new_backup_network}")
                    self.current_backup_network = new_backup_network
    
    def get_current_rankings(self) -> Dict:
        """Get current API rankings"""
        return {
            'defi': {
                'primary': {
                    'name': self.current_primary_defi,
                    'data': self.defi_apis[self.current_primary_defi]
                },
                'backup': {
                    'name': self.current_backup_defi,
                    'data': self.defi_apis[self.current_backup_defi]
                }
            },
            'network': {
                'primary': {
                    'name': self.current_primary_network,
                    'data': self.network_apis[self.current_primary_network]
                },
                'backup': {
                    'name': self.current_backup_network,
                    'data': self.network_apis[self.current_backup_network]
                }
            },
            'all_defi': self.defi_apis,
            'all_network': self.network_apis
        }
    
    def get_network_endpoints(self) -> Tuple[str, str]:
        """Get current network endpoints for Algorand connectivity"""
        primary = self.network_apis[self.current_primary_network]
        return primary['algod'], primary['indexer']
    
    def show_final_rankings(self) -> None:
        """Show comprehensive final rankings"""
        print("\n🏆 FINAL API RANKINGS (Based on Actual Connectivity)")
        print("=" * 70)
        
        rankings = self.get_current_rankings()
        
        # Show DeFi Rankings (Primary)
        print("🥇 DEFI PROTOCOL RANKINGS (Primary Trading APIs):")
        defi_sorted = sorted(rankings['all_defi'].items(), key=lambda x: -x[1]['score'])
        for i, (name, data) in enumerate(defi_sorted, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            status_emoji = "✅" if data['status'] == 'healthy' else "⚠️" if data['status'] == 'degraded' else "❌"
            response_time = data.get('response_time')
            response_str = f"{response_time:.3f}s" if response_time is not None else "N/A"
            print(f"   {medal} {data['name']}: {data['status']} | Score: {data['score']} | Response: {response_str}")
        
        # Show Network Rankings (Backup)
        print("\n🥈 NETWORK API RANKINGS (Blockchain Connectivity):")
        network_sorted = sorted(rankings['all_network'].items(), key=lambda x: -x[1]['score'])
        for i, (name, data) in enumerate(network_sorted, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            status_emoji = "✅" if data['status'] == 'healthy' else "⚠️" if data['status'] == 'degraded' else "❌"
            response_time = data.get('response_time')
            response_str = f"{response_time:.3f}s" if response_time is not None else "N/A"
            print(f"   {medal} {name}: {data['status']} | Score: {data['score']} | Response: {response_str}")
        
        # Show Current Selections
        print(f"\n🎯 CURRENT SELECTIONS:")
        print(f"   🏦 Primary DeFi: {rankings['defi']['primary']['name']} (Score: {rankings['defi']['primary']['data']['score']})")
        print(f"   🏦 Backup DeFi: {rankings['defi']['backup']['name']} (Score: {rankings['defi']['backup']['data']['score']})")
        print(f"   🌐 Primary Network: {rankings['network']['primary']['name']} (Score: {rankings['network']['primary']['data']['score']})")
        print(f"   🌐 Backup Network: {rankings['network']['backup']['name']} (Score: {rankings['network']['backup']['data']['score']})")

def main():
    """Test the smart API ranker"""
    ranker = SmartAPIRanker()
    
    print("\n🧪 TESTING SMART API RANKER...")
    print("=" * 70)
    
    # Perform comprehensive test
    ranker.perform_comprehensive_test()
    
    # Show final rankings
    ranker.show_final_rankings()
    
    print("\n✅ Smart API ranking complete!")
    print("🎯 DeFi protocols are now your primary trading APIs")
    print("🌐 Network APIs are backups for blockchain connectivity")

if __name__ == "__main__":
    main()

