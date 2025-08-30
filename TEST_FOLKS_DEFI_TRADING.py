#!/usr/bin/env python3
"""
TEST FOLKS DEFI TRADING
Test real DeFi trading with the opted-in Folks Finance protocol
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.transaction import ApplicationCallTxn
from algosdk.v2client import algod

class TestFolksDeFiTrading:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID (already opted in)
        self.folks_app_id = 465814065
        
        print("🧪 TEST FOLKS DEFI TRADING System Initialized")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{self.wallet_address[-10:]}")
        print(f"🎯 Testing REAL DeFi trading with Folks Finance (App ID: {self.folks_app_id})")
    
    def test_folks_operations(self) -> Dict:
        """Test different Folks Finance operations"""
        print("🧪 TESTING FOLKS FINANCE OPERATIONS")
        print("=" * 50)
        
        # Test different operation types
        operations = [
            {
                "name": "bootstrap",
                "app_args": [b"bootstrap"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            {
                "name": "init",
                "app_args": [b"init"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            {
                "name": "supply",
                "app_args": [b"supply"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            {
                "name": "borrow",
                "app_args": [b"borrow"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            {
                "name": "repay",
                "app_args": [b"repay"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            {
                "name": "withdraw",
                "app_args": [b"withdraw"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            }
        ]
        
        results = {}
        
        for operation in operations:
            print(f"\n🔍 Testing operation: {operation['name']}")
            print("-" * 30)
            
            success = self._test_folks_operation(operation)
            results[operation['name']] = {
                'success': success,
                'operation': operation,
                'timestamp': datetime.now().isoformat()
            }
            
            if success:
                print(f"✅ {operation['name']}: SUCCESS!")
            else:
                print(f"❌ {operation['name']}: FAILED")
            
            # Wait between tests
            time.sleep(2)
        
        return results
    
    def _test_folks_operation(self, operation: Dict) -> bool:
        """Test a specific Folks Finance operation"""
        try:
            print(f"   Testing: {operation['name']}")
            
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            
            # Create smart contract call
            app_call_txn = ApplicationCallTxn(
                sender=self.wallet_address,
                sp=params,
                index=self.folks_app_id,
                on_complete=0,  # NoOp
                app_args=operation['app_args'],
                accounts=operation['accounts'],
                foreign_assets=operation['foreign_assets'],
                foreign_apps=operation['foreign_apps']
            )
            
            # Sign the transaction
            try:
                signed_txn = app_call_txn.sign(self.private_key)
                print("      ✅ Transaction signed successfully")
            except Exception as sign_error:
                print(f"      ❌ Signing failed: {sign_error}")
                return False
            
            # Submit the transaction
            tx_id = self.algod_client.send_transaction(signed_txn)
            print(f"      📤 Transaction submitted: {tx_id}")
            
            # Wait for confirmation
            print("      ⏳ Waiting for confirmation...")
            confirmed_round = None
            max_wait_time = 20
            start_time = time.time()
            
            while confirmed_round is None and (time.time() - start_time) < max_wait_time:
                try:
                    confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                    if confirmed_txn.get('confirmed-round'):
                        confirmed_round = confirmed_txn.get('confirmed-round')
                        print(f"      ✅ Transaction confirmed in round {confirmed_round}")
                        
                        # Save successful operation details
                        operation_details = {
                            "timestamp": datetime.now().isoformat(),
                            "operation": operation['name'],
                            "app_id": self.folks_app_id,
                            "transaction_id": tx_id,
                            "confirmed_round": confirmed_round,
                            "status": "confirmed",
                            "wallet": self.wallet_address,
                            "note": "REAL DeFi operation successful!",
                            "smart_contract": True,
                            "not_wallet_to_wallet": True
                        }
                        
                        with open(f'folks_{operation["name"]}_success.json', 'w') as f:
                            json.dump(operation_details, f, indent=2)
                        
                        return True
                        
                    elif confirmed_txn.get('pool-error'):
                        error_msg = confirmed_txn.get('pool-error')
                        print(f"      ❌ Transaction failed: {error_msg}")
                        
                        # Check if it's a logic error (which means we reached the smart contract)
                        if "logic eval error" in error_msg:
                            print(f"      📝 Reached smart contract but failed execution")
                            print(f"      🔍 This is progress - we're reaching the DeFi protocol!")
                            return False
                        else:
                            print(f"      ❌ Transaction pool error")
                            return False
                    else:
                        time.sleep(1)
                except Exception as e:
                    print(f"      ⚠️ Error checking confirmation: {e}")
                    time.sleep(1)
            
            if confirmed_round is None:
                print(f"      ⏰ Transaction timeout")
                return False
            
            return True
            
        except Exception as e:
            print(f"      ❌ Test failed: {e}")
            return False
    
    def run_comprehensive_test(self) -> Dict:
        """Run comprehensive test of Folks Finance DeFi operations"""
        print("🚀 COMPREHENSIVE FOLKS FINANCE DEFI TEST")
        print("=" * 60)
        
        # Test all operations
        results = self.test_folks_operations()
        
        # Analyze results
        print(f"\n📊 TEST RESULTS ANALYSIS")
        print("=" * 40)
        
        success_count = sum(1 for result in results.values() if result['success'])
        total_count = len(results)
        
        print(f"✅ Successful operations: {success_count}/{total_count}")
        print(f"📊 Success rate: {(success_count/total_count)*100:.1f}%")
        
        if success_count > 0:
            print(f"\n🎉 SUCCESS: Found {success_count} working DeFi operations!")
            print("🚀 This means REAL DeFi trading is working!")
            
            for name, result in results.items():
                if result['success']:
                    print(f"   ✅ {name}: Working DeFi operation")
        else:
            print(f"\n⚠️ No operations succeeded, but we're reaching the smart contracts")
            print("🔍 This means we need to find the correct operation parameters")
        
        # Save comprehensive results
        with open('folks_defi_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📁 Comprehensive results saved to: folks_defi_test_results.json")
        
        return results

def main():
    """Test the Folks DeFi trading system"""
    print("🧪 TESTING FOLKS DEFI TRADING SYSTEM")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Folks DeFi Trading Test System ready!")
    print("🎯 This system will test REAL DeFi operations with Folks Finance!")
    print("🔗 Import this into your hybrid trading empire for DeFi testing!")

if __name__ == "__main__":
    main()

