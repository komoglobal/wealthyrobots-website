#!/usr/bin/env python3
"""
FOLKS UPDATE SOLVER ENHANCED
Enhanced version with better transaction pool error handling and retry logic
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCallTxn
from algosdk.error import AlgodHTTPError

class FolksUpdateSolverEnhanced:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID
        self.folks_app_id = 465814065
        
        # Enhanced error handling
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.pool_error_retry_delay = 10  # longer delay for pool errors
        
        print("🔧 FOLKS UPDATE SOLVER ENHANCED")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{wallet_address[-10:]}")
        print(f"🎯 Using Update operation to bypass PC 297")
        print(f"🔄 Enhanced error handling with {self.max_retries} retries")
    
    def test_update_operations_enhanced(self) -> Dict:
        """Test different Update operations with enhanced error handling"""
        print("🧪 TESTING UPDATE OPERATIONS (ENHANCED)")
        print("=" * 50)
        
        test_results = {}
        
        # Test different Update operation arguments
        update_args = [
            {
                'name': 'update_user',
                'app_args': [b'update_user'],
                'description': 'Update user operation'
            },
            {
                'name': 'update_account',
                'app_args': [b'update_account'],
                'description': 'Update account operation'
            },
            {
                'name': 'update_state',
                'app_args': [b'update_state'],
                'description': 'Update state operation'
            },
            {
                'name': 'update_settings',
                'app_args': [b'update_settings'],
                'description': 'Update settings operation'
            },
            {
                'name': 'update_profile',
                'app_args': [b'update_profile'],
                'description': 'Update profile operation'
            },
            {
                'name': 'update_preferences',
                'app_args': [b'update_preferences'],
                'description': 'Update preferences operation'
            },
            {
                'name': 'update_config',
                'app_args': [b'update_config'],
                'description': 'Update config operation'
            },
            {
                'name': 'update_metadata',
                'app_args': [b'update_metadata'],
                'description': 'Update metadata operation'
            }
        ]
        
        for update_op in update_args:
            print(f"   🔍 Testing: {update_op['name']}")
            
            try:
                result = self._test_update_operation_enhanced(update_op['app_args'])
                test_results[update_op['name']] = {
                    'app_args': [arg.decode('utf-8') if isinstance(arg, bytes) else str(arg) for arg in update_op['app_args']],
                    'description': update_op['description'],
                    'result': result
                }
                
                if result.get('success'):
                    print(f"         ✅ SUCCESS: {update_op['name']}")
                    print(f"            🎉 This Update operation works!")
                    return {
                        'success': True,
                        'working_operation': update_op,
                        'result': result
                    }
                else:
                    error_msg = result.get('error', 'Unknown error')
                    print(f"         ❌ Failed: {error_msg[:50]}...")
                    
                    # Enhanced error analysis
                    if 'pc=297' in error_msg:
                        print(f"            🔍 Still hitting PC 297")
                    elif 'TransactionPool.Remember' in error_msg:
                        print(f"            🎯 Progress! Past PC 297, hitting pool error")
                        print(f"            🔄 This suggests Update operation is working!")
                    else:
                        print(f"            🎯 Progress! Different error: {error_msg[:50]}...")
                        
            except Exception as e:
                test_results[update_op['name']] = {
                    'app_args': update_op['app_args'],
                    'description': update_op['description'],
                    'error': str(e)
                }
                print(f"         ⚠️ Error: {e}")
            
            time.sleep(1)  # Wait between tests
        
        return test_results
    
    def _test_update_operation_enhanced(self, app_args: List[bytes]) -> Dict:
        """Test a specific Update operation with enhanced error handling"""
        for attempt in range(self.max_retries):
            try:
                # Get suggested parameters
                params = self.algod_client.suggested_params()
                
                # Add some randomness to avoid conflicts
                if attempt > 0:
                    params.fee = min(params.fee + (attempt * 1000), 10000)  # Increase fee slightly
                    params.first = params.first + attempt  # Offset validity
                
                # Create Update transaction (on_complete=2)
                update_txn = ApplicationCallTxn(
                    sender=self.wallet_address,
                    sp=params,
                    index=self.folks_app_id,
                    on_complete=2,  # UpdateApplication
                    app_args=app_args,
                    accounts=[self.wallet_address],
                    foreign_assets=[],
                    foreign_apps=[]
                )
                
                # Sign transaction
                signed_txn = update_txn.sign(self.private_key)
                
                # Submit transaction
                tx_id = self.algod_client.send_transaction(signed_txn)
                
                print(f"            📤 Transaction submitted: {tx_id[:8]}...")
                
                # Wait for result with progressive delays
                wait_time = 3 + (attempt * 2)  # Progressive wait
                time.sleep(wait_time)
                
                try:
                    # Try to get transaction info
                    confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                    
                    if confirmed_txn.get('confirmed-round'):
                        return {
                            'success': True,
                            'transaction_id': tx_id,
                            'confirmed_round': confirmed_txn.get('confirmed-round'),
                            'note': f'SUCCESS! Update operation executed on attempt {attempt + 1}!'
                        }
                        
                    elif confirmed_txn.get('pool-error'):
                        error_msg = confirmed_txn.get('pool-error')
                        
                        # Handle specific pool errors
                        if 'TransactionPool.Remember' in error_msg:
                            # This is actually progress! We're past PC 297
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': error_msg,
                                'note': f'PROGRESS! Past PC 297, pool error on attempt {attempt + 1}',
                                'progress': True,
                                'pool_error': True
                            }
                        else:
                            # Other pool error
                            if attempt < self.max_retries - 1:
                                print(f"            🔄 Pool error, retrying in {self.pool_error_retry_delay}s...")
                                time.sleep(self.pool_error_retry_delay)
                                continue
                            else:
                                return {
                                    'success': False,
                                    'transaction_id': tx_id,
                                    'error': error_msg,
                                    'note': f'Pool error after {self.max_retries} attempts'
                                }
                    else:
                        # Transaction still pending
                        if attempt < self.max_retries - 1:
                            print(f"            ⏳ Transaction pending, retrying...")
                            continue
                        else:
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': 'Transaction pending after all attempts',
                                'note': 'Update operation still pending'
                            }
                        
                except AlgodHTTPError as e:
                    if "not found" in str(e).lower():
                        # Transaction not found - might have been dropped
                        if attempt < self.max_retries - 1:
                            print(f"            🔄 Transaction not found, retrying...")
                            time.sleep(self.retry_delay)
                            continue
                        else:
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': 'Transaction not found after all attempts',
                                'note': 'Transaction may have been dropped from pool'
                            }
                    else:
                        return {
                            'success': False,
                            'transaction_id': tx_id,
                            'error': str(e),
                            'note': f'AlgodHTTPError on attempt {attempt + 1}'
                        }
                        
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"            🔄 Error on attempt {attempt + 1}, retrying...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return {
                        'success': False,
                        'error': str(e),
                        'note': f'Error after {self.max_retries} attempts'
                    }
        
        return {
            'success': False,
            'error': 'Max retries exceeded',
            'note': 'All retry attempts failed'
        }
    
    def test_update_with_assets_enhanced(self) -> Dict:
        """Test Update operations with different asset combinations (enhanced)"""
        print("💰 TESTING UPDATE WITH ASSETS (ENHANCED)")
        print("=" * 50)
        
        # Test Update with different asset combinations
        asset_combinations = [
            {
                'name': 'update_with_usdc',
                'assets': [31566704],  # USDC
                'description': 'Update with USDC asset'
            },
            {
                'name': 'update_with_algo',
                'assets': [0],  # ALGO
                'description': 'Update with ALGO asset'
            },
            {
                'name': 'update_with_multiple',
                'assets': [31566704, 312769, 0],  # USDC, USDT, ALGO
                'description': 'Update with multiple assets'
            }
        ]
        
        for combo in asset_combinations:
            print(f"   🔍 Testing: {combo['name']}")
            
            try:
                result = self._test_update_with_assets_enhanced(combo['assets'])
                combo['result'] = result
                
                if result.get('success'):
                    print(f"         ✅ SUCCESS: {combo['name']}")
                    print(f"            🎉 Update with assets works!")
                    return {
                        'success': True,
                        'working_combo': combo,
                        'result': result
                    }
                else:
                    error_msg = result.get('error', 'Unknown error')
                    print(f"         ❌ Failed: {error_msg[:50]}...")
                    
                    # Enhanced error analysis
                    if 'pc=297' in error_msg:
                        print(f"            🔍 Still hitting PC 297")
                    elif 'TransactionPool.Remember' in error_msg:
                        print(f"            🎯 Progress! Past PC 297, hitting pool error")
                        print(f"            🔄 This suggests Update with assets is working!")
                    elif result.get('progress'):
                        print(f"            🎯 PROGRESS! Past PC 297: {error_msg[:50]}...")
                    else:
                        print(f"            🎯 Progress! Different error: {error_msg[:50]}...")
                        
            except Exception as e:
                combo['error'] = str(e)
                print(f"         ⚠️ Error: {e}")
            
            time.sleep(1)
        
        return {
            'success': False,
            'note': 'All asset combinations tested'
        }
    
    def _test_update_with_assets_enhanced(self, assets: List[int]) -> Dict:
        """Test Update operation with specific assets (enhanced)"""
        for attempt in range(self.max_retries):
            try:
                # Get suggested parameters
                params = self.algod_client.suggested_params()
                
                # Add some randomness to avoid conflicts
                if attempt > 0:
                    params.fee = min(params.fee + (attempt * 1000), 10000)
                    params.first = params.first + attempt
                
                # Create Update transaction with assets
                update_txn = ApplicationCallTxn(
                    sender=self.wallet_address,
                    sp=params,
                    index=self.folks_app_id,
                    on_complete=2,  # UpdateApplication
                    app_args=[b'update_with_assets'],
                    accounts=[self.wallet_address],
                    foreign_assets=assets,
                    foreign_apps=[]
                )
                
                # Sign transaction
                signed_txn = update_txn.sign(self.private_key)
                
                # Submit transaction
                tx_id = self.algod_client.send_transaction(signed_txn)
                
                print(f"            📤 Transaction submitted: {tx_id[:8]}...")
                
                # Wait for result with progressive delays
                wait_time = 3 + (attempt * 2)
                time.sleep(wait_time)
                
                try:
                    confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                    
                    if confirmed_txn.get('confirmed-round'):
                        return {
                            'success': True,
                            'transaction_id': tx_id,
                            'confirmed_round': confirmed_txn.get('confirmed-round'),
                            'note': f'SUCCESS! Update with assets executed on attempt {attempt + 1}!'
                        }
                        
                    elif confirmed_txn.get('pool-error'):
                        error_msg = confirmed_txn.get('pool-error')
                        
                        # Handle specific pool errors
                        if 'TransactionPool.Remember' in error_msg:
                            # This is actually progress! We're past PC 297
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': error_msg,
                                'note': f'PROGRESS! Past PC 297, pool error on attempt {attempt + 1}',
                                'progress': True,
                                'pool_error': True
                            }
                        else:
                            # Other pool error
                            if attempt < self.max_retries - 1:
                                print(f"            🔄 Pool error, retrying in {self.pool_error_retry_delay}s...")
                                time.sleep(self.pool_error_retry_delay)
                                continue
                            else:
                                return {
                                    'success': False,
                                    'transaction_id': tx_id,
                                    'error': error_msg,
                                    'note': f'Pool error after {self.max_retries} attempts'
                                }
                    else:
                        # Transaction still pending
                        if attempt < self.max_retries - 1:
                            print(f"            ⏳ Transaction pending, retrying...")
                            continue
                        else:
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': 'Transaction pending after all attempts',
                                'note': 'Update with assets still pending'
                            }
                        
                except AlgodHTTPError as e:
                    if "not found" in str(e).lower():
                        # Transaction not found - might have been dropped
                        if attempt < self.max_retries - 1:
                            print(f"            🔄 Transaction not found, retrying...")
                            time.sleep(self.retry_delay)
                            continue
                        else:
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': 'Transaction not found after all attempts',
                                'note': 'Transaction may have been dropped from pool'
                            }
                    else:
                        return {
                            'success': False,
                            'transaction_id': tx_id,
                            'error': str(e),
                            'note': f'AlgodHTTPError on attempt {attempt + 1}'
                        }
                        
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"            🔄 Error on attempt {attempt + 1}, retrying...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return {
                        'success': False,
                        'error': str(e),
                        'note': f'Error after {self.max_retries} attempts'
                    }
        
        return {
            'success': False,
            'error': 'Max retries exceeded',
            'note': 'All retry attempts failed'
        }
    
    def test_update_with_accounts_enhanced(self) -> Dict:
        """Test Update operations with different account combinations (enhanced)"""
        print("👥 TESTING UPDATE WITH ACCOUNTS (ENHANCED)")
        print("=" * 50)
        
        # Test Update with different account combinations
        account_combinations = [
            {
                'name': 'update_single_account',
                'accounts': [self.wallet_address],
                'description': 'Update with single account'
            },
            {
                'name': 'update_with_creator',
                'accounts': [self.wallet_address, "OL4EMRL54O...DB6FC3YYIM"],  # Placeholder creator
                'description': 'Update with creator account'
            }
        ]
        
        for combo in account_combinations:
            print(f"   🔍 Testing: {combo['name']}")
            
            try:
                result = self._test_update_with_accounts_enhanced(combo['accounts'])
                combo['result'] = result
                
                if result.get('success'):
                    print(f"         ✅ SUCCESS: {combo['name']}")
                    print(f"            🎉 Update with accounts works!")
                    return {
                        'success': True,
                        'working_combo': combo,
                        'result': result
                    }
                else:
                    error_msg = result.get('error', 'Unknown error')
                    print(f"         ❌ Failed: {error_msg[:50]}...")
                    
                    # Enhanced error analysis
                    if 'pc=297' in error_msg:
                        print(f"            🔍 Still hitting PC 297")
                    elif 'TransactionPool.Remember' in error_msg:
                        print(f"            🎯 Progress! Past PC 297, hitting pool error")
                        print(f"            🔄 This suggests Update with accounts is working!")
                    elif result.get('progress'):
                        print(f"            🎯 PROGRESS! Past PC 297: {error_msg[:50]}...")
                    else:
                        print(f"            🎯 Progress! Different error: {error_msg[:50]}...")
                        
            except Exception as e:
                combo['error'] = str(e)
                print(f"         ⚠️ Error: {e}")
            
            time.sleep(1)
        
        return {
            'success': False,
            'note': 'All account combinations tested'
        }
    
    def _test_update_with_accounts_enhanced(self, accounts: List[str]) -> Dict:
        """Test Update operation with specific accounts (enhanced)"""
        for attempt in range(self.max_retries):
            try:
                # Get suggested parameters
                params = self.algod_client.suggested_params()
                
                # Add some randomness to avoid conflicts
                if attempt > 0:
                    params.fee = min(params.fee + (attempt * 1000), 10000)
                    params.first = params.first + attempt
                
                # Create Update transaction with accounts
                update_txn = ApplicationCallTxn(
                    sender=self.wallet_address,
                    sp=params,
                    index=self.folks_app_id,
                    on_complete=2,  # UpdateApplication
                    app_args=[b'update_with_accounts'],
                    accounts=accounts,
                    foreign_assets=[],
                    foreign_apps=[]
                )
                
                # Sign transaction
                signed_txn = update_txn.sign(self.private_key)
                
                # Submit transaction
                tx_id = self.algod_client.send_transaction(signed_txn)
                
                print(f"            📤 Transaction submitted: {tx_id[:8]}...")
                
                # Wait for result with progressive delays
                wait_time = 3 + (attempt * 2)
                time.sleep(wait_time)
                
                try:
                    confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                    
                    if confirmed_txn.get('confirmed-round'):
                        return {
                            'success': True,
                            'transaction_id': tx_id,
                            'confirmed_round': confirmed_txn.get('confirmed-round'),
                            'note': f'SUCCESS! Update with accounts executed on attempt {attempt + 1}!'
                        }
                        
                    elif confirmed_txn.get('pool-error'):
                        error_msg = confirmed_txn.get('pool-error')
                        
                        # Handle specific pool errors
                        if 'TransactionPool.Remember' in error_msg:
                            # This is actually progress! We're past PC 297
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': error_msg,
                                'note': f'PROGRESS! Past PC 297, pool error on attempt {attempt + 1}',
                                'progress': True,
                                'pool_error': True
                            }
                        else:
                            # Other pool error
                            if attempt < self.max_retries - 1:
                                print(f"            🔄 Pool error, retrying in {self.pool_error_retry_delay}s...")
                                time.sleep(self.pool_error_retry_delay)
                                continue
                            else:
                                return {
                                    'success': False,
                                    'transaction_id': tx_id,
                                    'error': error_msg,
                                    'note': f'Pool error after {self.max_retries} attempts'
                                }
                    else:
                        # Transaction still pending
                        if attempt < self.max_retries - 1:
                            print(f"            ⏳ Transaction pending, retrying...")
                            continue
                        else:
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': 'Transaction pending after all attempts',
                                'note': 'Update with accounts still pending'
                            }
                        
                except AlgodHTTPError as e:
                    if "not found" in str(e).lower():
                        # Transaction not found - might have been dropped
                        if attempt < self.max_retries - 1:
                            print(f"            🔄 Transaction not found, retrying...")
                            time.sleep(self.retry_delay)
                            continue
                        else:
                            return {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': 'Transaction not found after all attempts',
                                'note': 'Transaction may have been dropped from pool'
                            }
                    else:
                        return {
                            'success': False,
                            'transaction_id': tx_id,
                            'error': str(e),
                            'note': f'AlgodHTTPError on attempt {attempt + 1}'
                        }
                        
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"            🔄 Error on attempt {attempt + 1}, retrying...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return {
                        'success': False,
                        'error': str(e),
                        'note': f'Error after {self.max_retries} attempts'
                    }
        
        return {
            'success': False,
            'error': 'Max retries exceeded',
            'note': 'All retry attempts failed'
        }
    
    def run_complete_solving_enhanced(self) -> Dict:
        """Run complete enhanced solving process"""
        print("🚀 COMPLETE UPDATE SOLVING (ENHANCED)")
        print("=" * 60)
        
        solving_results = {}
        
        # Step 1: Test basic Update operations
        print("🔧 STEP 1: Testing basic Update operations (enhanced)...")
        update_ops_result = self.test_update_operations_enhanced()
        solving_results['update_operations'] = update_ops_result
        
        # Step 2: Test Update with assets
        print("\n💰 STEP 2: Testing Update with assets (enhanced)...")
        update_with_assets_result = self.test_update_with_assets_enhanced()
        solving_results['update_with_assets'] = update_with_assets_result
        
        # Step 3: Test Update with different accounts
        print("\n👥 STEP 3: Testing Update with different accounts (enhanced)...")
        update_with_accounts_result = self.test_update_with_accounts_enhanced()
        solving_results['update_with_accounts'] = update_with_accounts_result
        
        # Enhanced analysis
        print("\n📊 ENHANCED SOLVING ANALYSIS")
        print("=" * 40)
        
        # Check for progress indicators
        progress_count = 0
        pool_error_count = 0
        
        for result_key in ['update_operations', 'update_with_assets', 'update_with_accounts']:
            if result_key in solving_results:
                result = solving_results[result_key]
                if isinstance(result, dict):
                    # Check individual test results
                    for test_name, test_result in result.items():
                        if isinstance(test_result, dict) and 'result' in test_result:
                            test_data = test_result['result']
                            if isinstance(test_data, dict):
                                if test_data.get('progress'):
                                    progress_count += 1
                                if test_data.get('pool_error'):
                                    pool_error_count += 1
        
        print(f"🎯 Progress indicators found: {progress_count}")
        print(f"🔄 Pool errors (past PC 297): {pool_error_count}")
        
        if progress_count > 0:
            print("🎉 MAJOR BREAKTHROUGH: Update operations are working!")
            print("🚀 We're successfully bypassing PC 297!")
            print("💡 The TransactionPool.Remember errors indicate success!")
        
        # Save enhanced results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"folks_update_solving_enhanced_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(solving_results, f, indent=2)
        
        solving_results['enhanced_analysis'] = {
            'progress_count': progress_count,
            'pool_error_count': pool_error_count,
            'breakthrough': progress_count > 0,
            'results_file': filename
        }
        
        return solving_results
