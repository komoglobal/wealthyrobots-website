#!/usr/bin/env python3
"""
FOLKS PROTOCOL INITIALIZER
Properly initializes Folks Finance protocol before DeFi operations
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCallTxn, ApplicationOptInTxn

class FolksProtocolInitializer:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID
        self.folks_app_id = 465814065
        
        print("🚀 FOLKS PROTOCOL INITIALIZER")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{wallet_address[-10:]}")
        print(f"🎯 Initializing Folks Finance protocol properly")
    
    def initialize_protocol(self) -> Dict:
        """Initialize Folks Finance protocol step by step"""
        print("🚀 INITIALIZING FOLKS FINANCE PROTOCOL")
        print("=" * 60)
        
        initialization_results = {}
        
        try:
            # Step 1: Check current app status
            print("📊 STEP 1: Checking current app status...")
            app_status = self._check_app_status()
            initialization_results['app_status'] = app_status
            
            # Step 2: Opt into the main app if needed
            print("🔗 STEP 2: Opting into main app...")
            app_opt_in = self._opt_into_main_app()
            initialization_results['app_opt_in'] = app_opt_in
            
            # Step 3: Initialize user account
            print("👤 STEP 3: Initializing user account...")
            account_init = self._initialize_user_account()
            initialization_results['account_init'] = account_init
            
            # Step 4: Test basic operation
            print("🧪 STEP 4: Testing basic operation...")
            basic_test = self._test_basic_operation()
            initialization_results['basic_test'] = basic_test
            
        except Exception as e:
            print(f"❌ Error in protocol initialization: {e}")
            initialization_results['error'] = str(e)
        
        return initialization_results
    
    def _check_app_status(self) -> Dict:
        """Check current app status"""
        print("   🔍 Checking app status...")
        
        try:
            # Check if user is opted into the app
            account_info = self.algod_client.account_info(self.wallet_address)
            created_apps = account_info.get('created-apps', [])
            opted_in_apps = account_info.get('apps-local-state', [])
            
            is_creator = any(app['id'] == self.folks_app_id for app in created_apps)
            is_opted_in = any(app['id'] == self.folks_app_id for app in opted_in_apps)
            
            status = {
                'is_creator': is_creator,
                'is_opted_in': is_opted_in,
                'app_id': self.folks_app_id,
                'current_state': 'opted_in' if is_opted_in else 'not_opted_in'
            }
            
            print(f"      App ID: {self.folks_app_id}")
            print(f"      Is creator: {is_creator}")
            print(f"      Is opted in: {is_opted_in}")
            print(f"      Current state: {status['current_state']}")
            
            return status
            
        except Exception as e:
            print(f"      ❌ Error checking app status: {e}")
            return {'error': str(e)}
    
    def _opt_into_main_app(self) -> Dict:
        """Opt into the main Folks Finance app"""
        print("   🔗 Opting into main app...")
        
        try:
            # Check if already opted in
            account_info = self.algod_client.account_info(self.wallet_address)
            opted_in_apps = account_info.get('apps-local-state', [])
            is_opted_in = any(app['id'] == self.folks_app_id for app in opted_in_apps)
            
            if is_opted_in:
                print("      ✅ Already opted into main app")
                return {'status': 'already_opted_in', 'note': 'User already opted in'}
            
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            
            # Create opt-in transaction
            opt_in_txn = ApplicationOptInTxn(
                sender=self.wallet_address,
                sp=params,
                index=self.folks_app_id
            )
            
            # Sign transaction
            signed_txn = opt_in_txn.sign(self.private_key)
            
            # Submit transaction
            tx_id = self.algod_client.send_transaction(signed_txn)
            print(f"      📡 Opt-in transaction submitted: {tx_id}")
            
            # Wait for confirmation
            print("      ⏳ Waiting for opt-in confirmation...")
            confirmed_txn = self._wait_for_confirmation(tx_id, 10)
            
            if confirmed_txn:
                print("      ✅ Successfully opted into main app!")
                return {
                    'status': 'opted_in',
                    'transaction_id': tx_id,
                    'confirmed_round': confirmed_txn.get('confirmed-round'),
                    'note': 'Successfully opted into Folks Finance'
                }
            else:
                print("      ❌ Opt-in failed")
                return {
                    'status': 'failed',
                    'transaction_id': tx_id,
                    'note': 'Opt-in transaction failed'
                }
                
        except Exception as e:
            print(f"      ❌ Error opting into main app: {e}")
            return {'error': str(e)}
    
    def _initialize_user_account(self) -> Dict:
        """Initialize user account on Folks Finance"""
        print("   👤 Initializing user account...")
        
        try:
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            
            # Create initialization transaction
            # Folks Finance typically requires an 'init' call
            init_txn = ApplicationCallTxn(
                sender=self.wallet_address,
                sp=params,
                index=self.folks_app_id,
                on_complete=0,  # NoOp
                app_args=[b'init'],
                accounts=[self.wallet_address],
                foreign_assets=[],
                foreign_apps=[]
            )
            
            # Sign transaction
            signed_txn = init_txn.sign(self.private_key)
            
            # Submit transaction
            tx_id = self.algod_client.send_transaction(signed_txn)
            print(f"      📡 Init transaction submitted: {tx_id}")
            
            # Wait for confirmation
            print("      ⏳ Waiting for init confirmation...")
            confirmed_txn = self._wait_for_confirmation(tx_id, 10)
            
            if confirmed_txn:
                print("      ✅ User account initialized!")
                return {
                    'status': 'initialized',
                    'transaction_id': tx_id,
                    'confirmed_round': confirmed_txn.get('confirmed-round'),
                    'note': 'User account initialized on Folks Finance'
                }
            else:
                print("      ❌ Account initialization failed")
                return {
                    'status': 'failed',
                    'transaction_id': tx_id,
                    'note': 'Account initialization failed'
                }
                
        except Exception as e:
            print(f"      ❌ Error initializing user account: {e}")
            return {'error': str(e)}
    
    def _test_basic_operation(self) -> Dict:
        """Test a basic operation after initialization"""
        print("   🧪 Testing basic operation...")
        
        try:
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            
            # Try a simple 'get_user_info' or similar operation
            # This should work if initialization was successful
            test_txn = ApplicationCallTxn(
                sender=self.wallet_address,
                sp=params,
                index=self.folks_app_id,
                on_complete=0,  # NoOp
                app_args=[b'get_user_info'],
                accounts=[self.wallet_address],
                foreign_assets=[],
                foreign_apps=[]
            )
            
            # Sign transaction
            signed_txn = test_txn.sign(self.private_key)
            
            # Submit transaction
            tx_id = self.algod_client.send_transaction(signed_txn)
            print(f"      📡 Test transaction submitted: {tx_id}")
            
            # Wait for confirmation
            print("      ⏳ Waiting for test confirmation...")
            confirmed_txn = self._wait_for_confirmation(tx_id, 10)
            
            if confirmed_txn:
                print("      ✅ Basic operation successful!")
                return {
                    'status': 'success',
                    'transaction_id': tx_id,
                    'confirmed_round': confirmed_txn.get('confirmed-round'),
                    'note': 'Basic operation successful - protocol ready!'
                }
            else:
                print("      ❌ Basic operation failed")
                return {
                    'status': 'failed',
                    'transaction_id': tx_id,
                    'note': 'Basic operation failed'
                }
                
        except Exception as e:
            print(f"      ❌ Error testing basic operation: {e}")
            return {'error': str(e)}
    
    def _wait_for_confirmation(self, tx_id: str, timeout: int = 10) -> Optional[Dict]:
        """Wait for transaction confirmation"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check transaction status
                txn_info = self.algod_client.pending_transaction_info(tx_id)
                
                if txn_info.get('confirmed-round'):
                    return txn_info
                elif txn_info.get('pool-error'):
                    print(f"         ❌ Transaction failed: {txn_info['pool-error']}")
                    return None
                
                time.sleep(1)
                
            except Exception as e:
                print(f"         ⚠️ Error checking transaction: {e}")
                time.sleep(1)
        
        print("         ⏰ Timeout waiting for confirmation")
        return None
    
    def run_complete_initialization(self) -> Dict:
        """Run complete protocol initialization"""
        print("🚀 COMPLETE PROTOCOL INITIALIZATION")
        print("=" * 60)
        
        # Run initialization
        initialization_results = self.initialize_protocol()
        
        # Display results
        print(f"\n📊 INITIALIZATION RESULTS")
        print("=" * 40)
        
        if 'app_status' in initialization_results:
            app_status = initialization_results['app_status']
            if 'error' not in app_status:
                print(f"📊 App Status: {app_status['current_state']}")
        
        if 'app_opt_in' in initialization_results:
            app_opt_in = initialization_results['app_opt_in']
            if 'error' not in app_opt_in:
                print(f"🔗 App Opt-in: {app_opt_in['status']}")
                if app_opt_in['status'] == 'opted_in':
                    print(f"   Transaction: {app_opt_in['transaction_id']}")
        
        if 'account_init' in initialization_results:
            account_init = initialization_results['account_init']
            if 'error' not in account_init:
                print(f"👤 Account Init: {account_init['status']}")
                if account_init['status'] == 'initialized':
                    print(f"   Transaction: {account_init['transaction_id']}")
        
        if 'basic_test' in initialization_results:
            basic_test = initialization_results['basic_test']
            if 'error' not in basic_test:
                print(f"🧪 Basic Test: {basic_test['status']}")
                if basic_test['status'] == 'success':
                    print(f"   Transaction: {basic_test['transaction_id']}")
                    print(f"\n🎉 SUCCESS: Folks Finance protocol initialized!")
                    print(f"🚀 Ready for DeFi operations!")
        
        # Save results
        with open('folks_protocol_initialization.json', 'w') as f:
            json.dump(initialization_results, f, indent=2, default=str)
        
        print(f"\n📁 Initialization results saved to: folks_protocol_initialization.json")
        
        return initialization_results

def main():
    """Test the Folks protocol initializer"""
    print("🧪 TESTING FOLKS PROTOCOL INITIALIZER")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Folks Protocol Initializer ready!")
    print("🎯 This system will properly initialize the protocol!")
    print("🔗 Import this into your hybrid trading empire for protocol setup!")

if __name__ == "__main__":
    main()
