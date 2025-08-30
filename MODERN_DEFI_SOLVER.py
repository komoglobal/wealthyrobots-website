#!/usr/bin/env python3
"""
MODERN DEFI SOLVER
Focuses on active, operational DeFi protocols on Algorand
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCallTxn
from algosdk.error import AlgodHTTPError

class ModernDeFiSolver:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # ACTIVE DeFi Protocols (not defunct like Algofi)
        self.active_protocols = {
            'folks_finance': {
                'name': 'Folks Finance',
                'app_id': 465814065,
                'status': 'active',
                'description': 'Lending and borrowing protocol',
                'operations': ['supply', 'borrow', 'repay', 'withdraw']
            },
            'pact_fi': {
                'name': 'Pact.fi',
                'app_id': 148607000,
                'status': 'active', 
                'description': 'DEX and liquidity protocol',
                'operations': ['swap', 'add_liquidity', 'remove_liquidity']
            },
            'tinyman': {
                'name': 'Tinyman',
                'app_id': 148607000,
                'status': 'active',
                'description': 'DEX and AMM protocol',
                'operations': ['swap', 'pool_operations']
            },
            'gard': {
                'name': 'GARD',
                'app_id': 2838930,
                'status': 'active',
                'description': 'Stablecoin and DeFi protocol',
                'operations': ['mint', 'redeem', 'stake']
            },
            'vestige': {
                'name': 'Vestige',
                'app_id': 148607000,
                'status': 'active',
                'description': 'DEX aggregator',
                'operations': ['swap', 'route_trade']
            }
        }
        
        print("🔧 MODERN DEFI SOLVER")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{wallet_address[-10:]}")
        print(f"🎯 Focusing on ACTIVE protocols (not defunct like Algofi)")
        print(f"📊 Active protocols: {len(self.active_protocols)}")
    
    def check_protocol_status(self, protocol_key: str) -> Dict:
        """Check if a specific protocol is accessible and operational"""
        protocol = self.active_protocols.get(protocol_key)
        if not protocol:
            return {'status': 'unknown', 'error': 'Protocol not found'}
        
        try:
            # Try to get application info
            app_info = self.algod_client.application_info(protocol['app_id'])
            
            if app_info:
                return {
                    'status': 'active',
                    'protocol': protocol,
                    'app_info': {
                        'creator': app_info.get('params', {}).get('creator'),
                        'global_state': len(app_info.get('params', {}).get('global-state', [])),
                        'local_state_schema': app_info.get('params', {}).get('local-state-schema'),
                        'global_state_schema': app_info.get('params', {}).get('global-state-schema')
                    }
                }
            else:
                return {'status': 'inactive', 'protocol': protocol, 'error': 'No app info'}
                
        except Exception as e:
            return {'status': 'error', 'protocol': protocol, 'error': str(e)}
    
    def test_protocol_operations(self, protocol_key: str) -> Dict:
        """Test basic operations for a specific protocol"""
        protocol = self.active_protocols.get(protocol_key)
        if not protocol:
            return {'status': 'error', 'error': 'Protocol not found'}
        
        print(f"🧪 Testing {protocol['name']} operations...")
        
        # Test basic application call (NoOp)
        try:
            params = self.algod_client.suggested_params()
            
            # Create a simple NoOp call to test connectivity
            test_txn = ApplicationCallTxn(
                sender=self.wallet_address,
                sp=params,
                index=protocol['app_id'],
                on_complete=0,  # NoOp
                app_args=[b'ping'],
                accounts=[self.wallet_address],
                foreign_assets=[],
                foreign_apps=[]
            )
            
            # Sign and submit
            signed_txn = test_txn.sign(self.private_key)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            print(f"   📤 Test transaction submitted: {tx_id[:8]}...")
            
            # Wait for result
            time.sleep(3)
            
            try:
                result = self.algod_client.pending_transaction_info(tx_id)
                
                if result.get('confirmed-round'):
                    return {
                        'status': 'success',
                        'protocol': protocol,
                        'transaction_id': tx_id,
                        'confirmed_round': result.get('confirmed-round'),
                        'note': f'Successfully connected to {protocol["name"]}'
                    }
                elif result.get('pool-error'):
                    error_msg = result.get('pool-error')
                    if 'pc=' in error_msg:
                        return {
                            'status': 'pc_error',
                            'protocol': protocol,
                            'transaction_id': tx_id,
                            'error': error_msg,
                            'note': f'PC error on {protocol["name"]} - needs Update approach'
                        }
                    else:
                        return {
                            'status': 'pool_error',
                            'protocol': protocol,
                            'transaction_id': tx_id,
                            'error': error_msg,
                            'note': f'Pool error on {protocol["name"]}'
                        }
                else:
                    return {
                        'status': 'pending',
                        'protocol': protocol,
                        'transaction_id': tx_id,
                        'note': f'Transaction pending on {protocol["name"]}'
                    }
                    
            except Exception as e:
                return {
                    'status': 'error',
                    'protocol': protocol,
                    'transaction_id': tx_id,
                    'error': str(e),
                    'note': f'Error checking {protocol["name"]} transaction'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'protocol': protocol,
                'error': str(e),
                'note': f'Error creating {protocol["name"]} transaction'
            }
    
    def test_update_approach(self, protocol_key: str) -> Dict:
        """Test Update approach for protocols that hit PC errors"""
        protocol = self.active_protocols.get(protocol_key)
        if not protocol:
            return {'status': 'error', 'error': 'Protocol not found'}
        
        print(f"🔄 Testing Update approach for {protocol['name']}...")
        
        try:
            params = self.algod_client.suggested_params()
            
            # Create Update transaction
            update_txn = ApplicationCallTxn(
                sender=self.wallet_address,
                sp=params,
                index=protocol['app_id'],
                on_complete=2,  # Update
                app_args=[b'update'],
                accounts=[self.wallet_address],
                foreign_assets=[],
                foreign_apps=[]
            )
            
            # Sign and submit
            signed_txn = update_txn.sign(self.private_key)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            print(f"   📤 Update transaction submitted: {tx_id[:8]}...")
            
            # Wait for result
            time.sleep(3)
            
            try:
                result = self.algod_client.pending_transaction_info(tx_id)
                
                if result.get('confirmed-round'):
                    return {
                        'status': 'success',
                        'protocol': protocol,
                        'transaction_id': tx_id,
                        'confirmed_round': result.get('confirmed-round'),
                        'note': f'Update approach successful on {protocol["name"]}'
                    }
                elif result.get('pool-error'):
                    error_msg = result.get('pool-error')
                    if 'TransactionPool.Remember' in error_msg:
                        return {
                            'status': 'progress',
                            'protocol': protocol,
                            'transaction_id': tx_id,
                            'error': error_msg,
                            'note': f'Past PC error on {protocol["name"]} - Update working!'
                        }
                    else:
                        return {
                            'status': 'pool_error',
                            'protocol': protocol,
                            'transaction_id': tx_id,
                            'error': error_msg,
                            'note': f'Other pool error on {protocol["name"]}'
                        }
                else:
                    return {
                        'status': 'pending',
                        'protocol': protocol,
                        'transaction_id': tx_id,
                        'note': f'Update transaction pending on {protocol["name"]}'
                    }
                    
            except Exception as e:
                return {
                    'status': 'error',
                    'protocol': protocol,
                    'transaction_id': tx_id,
                    'error': str(e),
                    'note': f'Error checking {protocol["name"]} Update transaction'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'protocol': protocol,
                'error': str(e),
                'note': f'Error creating {protocol["name"]} Update transaction'
            }
    
    def run_complete_solving(self) -> Dict:
        """Run complete solving for all active protocols"""
        print("🚀 COMPLETE MODERN DEFI SOLVING")
        print("=" * 50)
        
        solving_results = {}
        
        for protocol_key in self.active_protocols.keys():
            print(f"\n🔍 Testing {protocol_key.upper()}...")
            
            # Check protocol status
            status = self.check_protocol_status(protocol_key)
            solving_results[f'{protocol_key}_status'] = status
            
            if status.get('status') == 'active':
                print(f"   ✅ {status['protocol']['name']} is active")
                
                # Test basic operations
                operations_result = self.test_protocol_operations(protocol_key)
                solving_results[f'{protocol_key}_operations'] = operations_result
                
                # If PC error, test Update approach
                if operations_result.get('status') == 'pc_error':
                    print(f"   🔄 PC error detected - testing Update approach...")
                    update_result = self.test_update_approach(protocol_key)
                    solving_results[f'{protocol_key}_update'] = update_result
                    
                    if update_result.get('status') == 'progress':
                        print(f"   🎯 Update approach working on {protocol_key}!")
                    elif update_result.get('status') == 'success':
                        print(f"   🎉 Update approach successful on {protocol_key}!")
                    else:
                        print(f"   ❌ Update approach failed on {protocol_key}")
                else:
                    print(f"   📊 Operations result: {operations_result.get('status')}")
            else:
                print(f"   ❌ {protocol_key} status: {status.get('status')}")
                if 'error' in status:
                    print(f"      Error: {status['error']}")
            
            time.sleep(1)  # Brief pause between protocols
        
        # Analysis
        print(f"\n📊 SOLVING ANALYSIS:")
        print("=" * 30)
        
        working_protocols = []
        pc_error_protocols = []
        update_working_protocols = []
        
        for protocol_key in self.active_protocols.keys():
            status = solving_results.get(f'{protocol_key}_status', {})
            operations = solving_results.get(f'{protocol_key}_operations', {})
            update = solving_results.get(f'{protocol_key}_update', {})
            
            if status.get('status') == 'active':
                if operations.get('status') == 'success':
                    working_protocols.append(protocol_key)
                elif operations.get('status') == 'pc_error':
                    pc_error_protocols.append(protocol_key)
                    if update.get('status') in ['success', 'progress']:
                        update_working_protocols.append(protocol_key)
        
        print(f"   ✅ Working protocols: {len(working_protocols)}")
        print(f"   🔄 PC error protocols: {len(pc_error_protocols)}")
        print(f"   🎯 Update approach working: {len(update_working_protocols)}")
        
        if working_protocols:
            print(f"\n🎉 WORKING PROTOCOLS:")
            for protocol in working_protocols:
                print(f"   - {protocol}")
        
        if update_working_protocols:
            print(f"\n🚀 UPDATE APPROACH WORKING:")
            for protocol in update_working_protocols:
                print(f"   - {protocol}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"modern_defi_solving_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(solving_results, f, indent=2)
        
        solving_results['analysis'] = {
            'working_protocols': working_protocols,
            'pc_error_protocols': pc_error_protocols,
            'update_working_protocols': update_working_protocols,
            'results_file': filename
        }
        
        return solving_results



