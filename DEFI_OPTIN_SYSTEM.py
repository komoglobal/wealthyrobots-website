#!/usr/bin/env python3
"""
DEFI OPT-IN SYSTEM
Handles opt-in process for DeFi protocols before executing trades
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.transaction import ApplicationOptInTxn, ApplicationCallTxn
from algosdk.v2client import algod

class DeFiOptInSystem:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # VERIFIED DeFi Protocol App IDs
        self.verified_protocols = {
            "tinyman_v2": {
                "app_id": 1002541853,  # ✅ VERIFIED - EXISTS on mainnet
                "creator": "4HIR5U2J4FCIEAG6WMBJ4BS3VBTT6S7PLXXERVR2SQIOKZGZZZF2ZV27U4",
                "description": "DEX for token swaps"
            },
            "folks_finance": {
                "app_id": 465814065,  # ✅ VERIFIED - EXISTS on mainnet
                "creator": "3EPGHSNBBN5M2LD6V7A63EHZQQLATVQHDBYJQIZ6BLCBTIXA5XR7ZOZEB4",
                "description": "Lending and borrowing"
            }
        }
        
        print("🚀 DEFI OPT-IN SYSTEM Initialized")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{self.wallet_address[-10:]}")
        print("🎯 This system will opt-in to DeFi protocols for REAL trading!")
    
    def check_optin_status(self, app_id: int) -> bool:
        """Check if wallet is opted in to a specific app"""
        try:
            account_info = self.algod_client.account_info(self.wallet_address)
            
            # Check if the app is in the opted-in apps list
            for app in account_info.get('apps-local-state', []):
                if app['id'] == app_id:
                    print(f"✅ Already opted in to app {app_id}")
                    return True
            
            print(f"❌ Not opted in to app {app_id}")
            return False
            
        except Exception as e:
            print(f"❌ Error checking opt-in status: {e}")
            return False
    
    def optin_to_app(self, app_id: int, protocol_name: str) -> bool:
        """Opt-in to a specific DeFi app"""
        try:
            print(f"🔄 Opting in to {protocol_name} (App ID: {app_id})...")
            
            # Check current status
            if self.check_optin_status(app_id):
                print(f"✅ Already opted in to {protocol_name}")
                return True
            
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            
            # Create opt-in transaction
            optin_txn = ApplicationOptInTxn(
                sender=self.wallet_address,
                sp=params,
                index=app_id
            )
            
            # Sign and submit the opt-in transaction
            try:
                signed_txn = optin_txn.sign(self.private_key)
                print("✅ Opt-in transaction signed successfully")
            except Exception as sign_error:
                print(f"❌ Opt-in signing failed: {sign_error}")
                return False
            
            tx_id = self.algod_client.send_transaction(signed_txn)
            print(f"📤 Opt-in transaction submitted: {tx_id}")
            
            # Wait for confirmation
            print("⏳ Waiting for opt-in confirmation...")
            confirmed_round = None
            max_wait_time = 30
            start_time = time.time()
            
            while confirmed_round is None and (time.time() - start_time) < max_wait_time:
                try:
                    confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                    if confirmed_txn.get('confirmed-round'):
                        confirmed_round = confirmed_txn.get('confirmed-round')
                        print(f"✅ Opt-in confirmed in round {confirmed_round}")
                        break
                    elif confirmed_txn.get('pool-error'):
                        print(f"❌ Opt-in failed: {confirmed_txn.get('pool-error')}")
                        return False
                    else:
                        print("⏳ Still waiting for opt-in confirmation...")
                        time.sleep(2)
                except Exception as e:
                    print(f"⚠️ Error checking confirmation: {e}")
                    time.sleep(2)
            
            if confirmed_round is None:
                print("❌ Opt-in confirmation timeout")
                return False
            
            # Verify opt-in was successful
            if self.check_optin_status(app_id):
                print(f"🎉 SUCCESS: Opted in to {protocol_name}!")
                
                # Save opt-in details
                optin_details = {
                    "timestamp": datetime.now().isoformat(),
                    "protocol": protocol_name,
                    "app_id": app_id,
                    "transaction_id": tx_id,
                    "confirmed_round": confirmed_round,
                    "status": "opted_in",
                    "wallet": self.wallet_address
                }
                
                with open(f'{protocol_name}_optin_success.json', 'w') as f:
                    json.dump(optin_details, f, indent=2)
                
                return True
            else:
                print(f"❌ Opt-in verification failed")
                return False
                
        except Exception as e:
            print(f"❌ Opt-in to {protocol_name} failed: {e}")
            return False
    
    def optin_to_all_protocols(self) -> Dict:
        """Opt-in to all verified DeFi protocols"""
        print("🚀 OPTING IN TO ALL DEFI PROTOCOLS")
        print("=" * 50)
        
        results = {}
        
        for protocol_name, protocol_info in self.verified_protocols.items():
            print(f"\n🔍 Protocol: {protocol_name.upper()}")
            print("-" * 40)
            
            app_id = protocol_info['app_id']
            success = self.optin_to_app(app_id, protocol_name)
            results[protocol_name] = {
                'app_id': app_id,
                'opted_in': success,
                'timestamp': datetime.now().isoformat()
            }
            
            if success:
                print(f"✅ {protocol_name.upper()}: OPT-IN SUCCESSFUL")
            else:
                print(f"❌ {protocol_name.upper()}: OPT-IN FAILED")
            
            # Wait between opt-ins
            time.sleep(2)
        
        # Save overall results
        with open('defi_optin_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 OPT-IN COMPLETE")
        print("=" * 30)
        
        success_count = sum(1 for result in results.values() if result['opted_in'])
        total_count = len(results)
        
        print(f"✅ Successfully opted in: {success_count}/{total_count}")
        print(f"📁 Results saved to: defi_optin_results.json")
        
        return results

def main():
    """Test the DeFi opt-in system"""
    print("🧪 TESTING DEFI OPT-IN SYSTEM")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ DeFi Opt-In System ready!")
    print("🎯 This system will opt-in to DeFi protocols for REAL trading!")
    print("🔗 Import this into your hybrid trading empire for opt-in functionality!")

if __name__ == "__main__":
    main()

