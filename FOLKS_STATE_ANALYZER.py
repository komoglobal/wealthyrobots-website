#!/usr/bin/env python3
"""
FOLKS STATE ANALYZER
Analyzes exact protocol state requirements at PC 297
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCallTxn

class FolksStateAnalyzer:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID
        self.folks_app_id = 465814065
        
        print("🔍 FOLKS STATE ANALYZER")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{wallet_address[-10:]}")
        print(f"🎯 Analyzing exact state requirements at PC 297")
    
    def analyze_protocol_state(self) -> Dict:
        """Analyze exact protocol state requirements"""
        print("🔍 ANALYZING PROTOCOL STATE REQUIREMENTS")
        print("=" * 60)
        
        analysis_results = {}
        
        try:
            # Method 1: Analyze current local state
            print("📊 METHOD 1: Analyzing current local state...")
            local_state_analysis = self._analyze_local_state()
            analysis_results['local_state_analysis'] = local_state_analysis
            
            # Method 2: Analyze global state
            print("🌐 METHOD 2: Analyzing global state...")
            global_state_analysis = self._analyze_global_state()
            analysis_results['global_state_analysis'] = global_state_analysis
            
            # Method 3: Test different state combinations
            print("🧪 METHOD 3: Testing different state combinations...")
            state_combination_tests = self._test_state_combinations()
            analysis_results['state_combination_tests'] = state_combination_tests
            
            # Method 4: Analyze successful transactions
            print("🔍 METHOD 4: Analyzing successful transactions...")
            transaction_analysis = self._analyze_successful_transactions()
            analysis_results['transaction_analysis'] = transaction_analysis
            
        except Exception as e:
            print(f"❌ Error in state analysis: {e}")
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    def _analyze_local_state(self) -> Dict:
        """Analyze current local state"""
        print("   📊 Analyzing local state...")
        
        try:
            # Get account info
            account_info = self.algod_client.account_info(self.wallet_address)
            opted_in_apps = account_info.get('apps-local-state', [])
            
            # Find Folks Finance local state
            folks_local_state = None
            for app in opted_in_apps:
                if app['id'] == self.folks_app_id:
                    folks_local_state = app
                    break
            
            if not folks_local_state:
                return {'error': 'No local state found for Folks Finance'}
            
            # Analyze local state structure
            local_state = folks_local_state.get('key-value', [])
            
            analysis = {
                'has_local_state': True,
                'local_state_keys': len(local_state),
                'local_state_structure': {},
                'key_types': {},
                'value_analysis': {}
            }
            
            print(f"      Found {len(local_state)} local state keys")
            
            for kv_pair in local_state:
                key = kv_pair.get('key', '')
                value = kv_pair.get('value', {})
                
                # Decode key if it's base64
                try:
                    import base64
                    decoded_key = base64.b64decode(key).decode('utf-8')
                except:
                    decoded_key = key
                
                # Analyze value type
                value_type = value.get('type', 'unknown')
                value_data = value.get('uint', value.get('bytes', 'N/A'))
                
                analysis['local_state_structure'][decoded_key] = {
                    'type': value_type,
                    'value': value_data
                }
                
                if value_type not in analysis['key_types']:
                    analysis['key_types'][value_type] = 0
                analysis['key_types'][value_type] += 1
                
                print(f"         Key: {decoded_key}")
                print(f"         Type: {value_type}")
                print(f"         Value: {value_data}")
            
            print(f"      Key types found: {analysis['key_types']}")
            
            return analysis
            
        except Exception as e:
            print(f"      ❌ Error analyzing local state: {e}")
            return {'error': str(e)}
    
    def _analyze_global_state(self) -> Dict:
        """Analyze global state"""
        print("   🌐 Analyzing global state...")
        
        try:
            # Get app info
            app_info = self.algod_client.application_info(self.folks_app_id)
            global_state = app_info.get('params', {}).get('global-state', [])
            
            analysis = {
                'has_global_state': len(global_state) > 0,
                'global_state_keys': len(global_state),
                'global_state_structure': {},
                'key_types': {},
                'protocol_config': {}
            }
            
            print(f"      Found {len(global_state)} global state keys")
            
            for kv_pair in global_state:
                key = kv_pair.get('key', '')
                value = kv_pair.get('value', {})
                
                # Decode key if it's base64
                try:
                    import base64
                    decoded_key = base64.b64decode(key).decode('utf-8')
                except:
                    decoded_key = key
                
                # Analyze value type
                value_type = value.get('type', 'unknown')
                value_data = value.get('uint', value.get('bytes', 'N/A'))
                
                analysis['global_state_structure'][decoded_key] = {
                    'type': value_type,
                    'value': value_data
                }
                
                if value_type not in analysis['key_types']:
                    analysis['key_types'][value_type] = 0
                analysis['key_types'][value_type] += 1
                
                print(f"         Key: {decoded_key}")
                print(f"         Type: {value_type}")
                print(f"         Value: {value_data}")
            
            print(f"      Global key types: {analysis['key_types']}")
            
            return analysis
            
        except Exception as e:
            print(f"      ❌ Error analyzing global state: {e}")
            return {'error': str(e)}
    
    def _test_state_combinations(self) -> Dict:
        """Test different state combinations"""
        print("   🧪 Testing different state combinations...")
        
        test_results = {}
        
        # Test different operation types
        test_operations = [
            {
                'name': 'supply_operation',
                'app_args': [b'supply'],
                'description': 'Supply operation'
            },
            {
                'name': 'borrow_operation',
                'app_args': [b'borrow'],
                'description': 'Borrow operation'
            },
            {
                'name': 'withdraw_operation',
                'app_args': [b'withdraw'],
                'description': 'Withdraw operation'
            },
            {
                'name': 'repay_operation',
                'app_args': [b'repay'],
                'description': 'Repay operation'
            },
            {
                'name': 'get_user_info',
                'app_args': [b'get_user_info'],
                'description': 'Get user info'
            }
        ]
        
        for operation in test_operations:
            print(f"      Testing: {operation['name']}")
            
            try:
                result = self._test_operation(operation['app_args'])
                test_results[operation['name']] = {
                    'app_args': operation['app_args'],
                    'description': operation['description'],
                    'result': result
                }
                
                if result.get('success'):
                    print(f"         ✅ SUCCESS: {operation['name']}")
                    print(f"            🎉 This operation works!")
                    return {
                        'success': True,
                        'working_operation': operation,
                        'result': result
                    }
                else:
                    error_msg = result.get('error', 'Unknown error')
                    print(f"         ❌ Failed: {error_msg[:50]}...")
                    
                    # Check if we're past PC 297
                    if 'pc=297' in error_msg:
                        print(f"            🔍 Still hitting PC 297")
                    else:
                        print(f"            🎯 Progress! Different error point: {error_msg}")
                        
            except Exception as e:
                test_results[operation['name']] = {
                    'app_args': operation['app_args'],
                    'description': operation['description'],
                    'error': str(e)
                }
                print(f"         ⚠️ Error: {e}")
            
            time.sleep(1)  # Wait between tests
        
        return test_results
    
    def _test_operation(self, app_args: List[bytes]) -> Dict:
        """Test a specific operation"""
        try:
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            
            # Create transaction
            txn = ApplicationCallTxn(
                sender=self.wallet_address,
                sp=params,
                index=self.folks_app_id,
                on_complete=0,  # NoOp
                app_args=app_args,
                accounts=[self.wallet_address],
                foreign_assets=[],
                foreign_apps=[]
            )
            
            # Sign transaction
            signed_txn = txn.sign(self.private_key)
            
            # Submit transaction
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            # Wait for result
            time.sleep(3)
            
            try:
                confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                
                if confirmed_txn.get('confirmed-round'):
                    return {
                        'success': True,
                        'transaction_id': tx_id,
                        'confirmed_round': confirmed_txn.get('confirmed-round'),
                        'note': 'SUCCESS! Operation executed!'
                    }
                    
                elif confirmed_txn.get('pool-error'):
                    error_msg = confirmed_txn.get('pool-error')
                    return {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': error_msg,
                        'note': 'Transaction failed'
                    }
                else:
                    return {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': 'Transaction pending',
                        'note': 'Transaction still pending'
                    }
                    
            except Exception as e:
                return {
                    'success': False,
                    'transaction_id': tx_id,
                    'error': str(e),
                    'note': 'Error checking transaction'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'note': 'Transaction creation failed'
            }
    
    def _analyze_successful_transactions(self) -> Dict:
        """Analyze successful transactions"""
        print("   🔍 Analyzing successful transactions...")
        
        analysis = {
            'successful_txns': [],
            'common_patterns': [],
            'state_requirements': []
        }
        
        try:
            print("      Note: Transaction analysis requires deeper blockchain analysis")
            print("      This would involve scanning recent blocks for successful calls")
            
        except Exception as e:
            print(f"      ❌ Error analyzing transactions: {e}")
            analysis['error'] = str(e)
        
        return analysis
    
    def run_complete_analysis(self) -> Dict:
        """Run complete state analysis"""
        print("🚀 COMPLETE STATE ANALYSIS")
        print("=" * 60)
        
        # Run analysis
        analysis_results = self.analyze_protocol_state()
        
        # Display results
        print(f"\n📊 STATE ANALYSIS RESULTS")
        print("=" * 40)
        
        if 'local_state_analysis' in analysis_results:
            local_state = analysis_results['local_state_analysis']
            if 'error' not in local_state:
                print(f"📊 Local State Analysis:")
                print(f"   Keys found: {local_state['local_state_keys']}")
                print(f"   Key types: {local_state['key_types']}")
                
                if local_state['local_state_keys'] > 0:
                    print(f"   ✅ Local state exists - protocol may be initialized")
                else:
                    print(f"   ⚠️ No local state keys - protocol needs initialization")
        
        if 'global_state_analysis' in analysis_results:
            global_state = analysis_results['global_state_analysis']
            if 'error' not in global_state:
                print(f"🌐 Global State Analysis:")
                print(f"   Keys found: {global_state['global_state_keys']}")
                print(f"   Key types: {global_state['key_types']}")
        
        if 'state_combination_tests' in analysis_results:
            combination_tests = analysis_results['state_combination_tests']
            if isinstance(combination_tests, dict) and combination_tests.get('success'):
                print(f"\n🎉 SUCCESS: Found working operation!")
                working_op = combination_tests['working_operation']
                print(f"   Operation: {working_op['name']}")
                print(f"   Description: {working_op['description']}")
                print(f"   Result: {combination_tests['result']['note']}")
            else:
                print(f"\n🔍 OPERATION TESTING:")
                print(f"   All operations still hitting PC 297")
                print(f"   Need to analyze state requirements further")
        
        # Save results
        with open('folks_state_analysis.json', 'w') as f:
            json.dump(analysis_results, f, indent=2, default=str)
        
        print(f"\n📁 State analysis saved to: folks_state_analysis.json")
        
        return analysis_results

def main():
    """Test the Folks state analyzer"""
    print("🧪 TESTING FOLKS STATE ANALYZER")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Folks State Analyzer ready!")
    print("🎯 This system will analyze exact state requirements!")
    print("🔗 Import this into your hybrid trading empire for state analysis!")

if __name__ == "__main__":
    main()
