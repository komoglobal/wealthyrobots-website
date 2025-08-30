#!/usr/bin/env python3
"""
FOLKS OPTIN SOLVER
Opts the account into the Folks Finance app so Update operations can work
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod
from algosdk.transaction import ApplicationOptInTxn
from algosdk.error import AlgodHTTPError

class FolksOptInSolver:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID
        self.folks_app_id = 465814065
        
        print("🔧 FOLKS OPTIN SOLVER")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{wallet_address[-10:]}")
        print(f"🎯 Opting into Folks Finance App ID: {self.folks_app_id}")
    
    def check_optin_status(self) -> Dict:
        """Check if account is already opted into Folks Finance"""
        try:
            # Get account info
            account_info = self.algod_client.account_info(self.wallet_address)
            
            # Check if app is in local state
            if 'apps-local-state' in account_info:
                for app in account_info['apps-local-state']:
                    if app['id'] == self.folks_app_id:
                        return {
                            'opted_in': True,
                            'app_id': self.folks_app_id,
                            'local_state': app.get('key-value', []),
                            'note': 'Account already opted into Folks Finance'
                        }
            
            return {
                'opted_in': False,
                'app_id': self.folks_app_id,
                'note': 'Account not opted into Folks Finance'
            }
            
        except Exception as e:
            return {
                'opted_in': False,
                'app_id': self.folks_app_id,
                'error': str(e),
                'note': 'Error checking opt-in status'
            }
    
    def opt_into_folks(self) -> Dict:
        """Opt the account into the Folks Finance app"""
        try:
            print("🔗 Opting into Folks Finance app...")
            
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            
            # Create opt-in transaction
            optin_txn = ApplicationOptInTxn(
                sender=self.wallet_address,
                sp=params,
                index=self.folks_app_id
            )
            
            # Sign transaction
            signed_txn = optin_txn.sign(self.private_key)
            
            # Submit transaction
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            print(f"📤 Opt-in transaction submitted: {tx_id}")
            
            # Wait for confirmation
            print("⏳ Waiting for confirmation...")
            time.sleep(5)
            
            try:
                # Check transaction status
                confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                
                if confirmed_txn.get('confirmed-round'):
                    print(f"✅ Opt-in successful! Confirmed in round {confirmed_txn.get('confirmed-round')}")
                    
                    # Verify opt-in status
                    optin_status = self.check_optin_status()
                    
                    return {
                        'success': True,
                        'transaction_id': tx_id,
                        'confirmed_round': confirmed_txn.get('confirmed-round'),
                        'optin_status': optin_status,
                        'note': 'Successfully opted into Folks Finance'
                    }
                    
                elif confirmed_txn.get('pool-error'):
                    error_msg = confirmed_txn.get('pool-error')
                    return {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': error_msg,
                        'note': 'Opt-in failed with pool error'
                    }
                else:
                    return {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': 'Transaction pending',
                        'note': 'Opt-in transaction still pending'
                    }
                    
            except AlgodHTTPError as e:
                return {
                    'success': False,
                    'transaction_id': tx_id,
                    'error': str(e),
                    'note': 'Error checking opt-in transaction'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'note': 'Error creating opt-in transaction'
            }
    
    def run_optin_solving(self) -> Dict:
        """Run complete opt-in solving process"""
        print("🚀 FOLKS FINANCE OPTIN SOLVING")
        print("=" * 50)
        
        solving_results = {}
        
        # Step 1: Check current opt-in status
        print("🔍 STEP 1: Checking current opt-in status...")
        optin_status = self.check_optin_status()
        solving_results['current_status'] = optin_status
        
        if optin_status.get('opted_in'):
            print("✅ Account already opted into Folks Finance!")
            print("🚀 Ready to use Update operations!")
            solving_results['action_needed'] = 'none'
            solving_results['ready_for_update'] = True
            return solving_results
        
        # Step 2: Perform opt-in
        print("\n🔗 STEP 2: Performing opt-in...")
        optin_result = self.opt_into_folks()
        solving_results['optin_result'] = optin_result
        
        if optin_result.get('success'):
            print("🎉 Opt-in successful!")
            print("🚀 Account now ready for Folks Finance operations!")
            solving_results['action_needed'] = 'none'
            solving_results['ready_for_update'] = True
        else:
            print("❌ Opt-in failed")
            solving_results['action_needed'] = 'retry_optin'
            solving_results['ready_for_update'] = False
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"folks_optin_solving_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(solving_results, f, indent=2)
        
        solving_results['results_file'] = filename
        
        return solving_results



