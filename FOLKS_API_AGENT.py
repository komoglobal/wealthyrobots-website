#!/usr/bin/env python3
"""
FOLKS API AGENT
API-based agent that interacts with Folks Finance through their API endpoints
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCallTxn

class FolksAPIAgent:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance API endpoints
        self.base_url = "https://api.folks.finance"
        self.lending_url = "https://lending.folks.finance"
        
        # API headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        print("🔌 FOLKS API AGENT")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{wallet_address[-10:]}")
        print(f"🎯 API-based interaction with Folks Finance")
    
    def get_protocol_info(self) -> Dict:
        """Get protocol information from API"""
        print("📊 Getting protocol information...")
        
        try:
            # Try to get protocol stats
            response = requests.get(f"{self.base_url}/stats", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print("   ✅ Protocol info retrieved successfully")
                return {
                    'success': True,
                    'data': data,
                    'note': 'Protocol information retrieved'
                }
            else:
                print(f"   ⚠️ API returned status {response.status_code}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'note': 'API request failed'
                }
                
        except Exception as e:
            print(f"   ❌ Error getting protocol info: {e}")
            return {'error': str(e)}
    
    def get_markets_info(self) -> Dict:
        """Get markets information"""
        print("🏪 Getting markets information...")
        
        try:
            # Try to get markets data
            response = requests.get(f"{self.base_url}/markets", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Markets info retrieved: {len(data) if isinstance(data, list) else 'data'} markets")
                return {
                    'success': True,
                    'data': data,
                    'note': 'Markets information retrieved'
                }
            else:
                print(f"   ⚠️ Markets API returned status {response.status_code}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'note': 'Markets API request failed'
                }
                
        except Exception as e:
            print(f"   ❌ Error getting markets info: {e}")
            return {'error': str(e)}
    
    def get_user_portfolio(self) -> Dict:
        """Get user portfolio information"""
        print("👤 Getting user portfolio...")
        
        try:
            # Try to get user-specific data
            response = requests.get(f"{self.base_url}/user/{self.wallet_address}", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print("   ✅ User portfolio retrieved successfully")
                return {
                    'success': True,
                    'data': data,
                    'note': 'User portfolio retrieved'
                }
            else:
                print(f"   ⚠️ User API returned status {response.status_code}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'note': 'User API request failed'
                }
                
        except Exception as e:
            print(f"   ❌ Error getting user portfolio: {e}")
            return {'error': str(e)}
    
    def execute_supply_through_api(self, asset_id: int, amount: int) -> Dict:
        """Execute supply operation through API"""
        print(f"💰 Executing supply operation: {amount} of asset {asset_id}")
        
        try:
            # Create the supply transaction
            params = self.algod_client.suggested_params()
            
            # Folks Finance supply operation
            supply_txn = ApplicationCallTxn(
                sender=self.wallet_address,
                sp=params,
                index=465814065,  # Folks Finance App ID
                on_complete=0,  # NoOp
                app_args=[b'supply'],
                accounts=[self.wallet_address],
                foreign_assets=[asset_id],
                foreign_apps=[]
            )
            
            # Sign and submit
            signed_txn = supply_txn.sign(self.private_key)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            print(f"   📡 Supply transaction submitted: {tx_id}")
            
            # Wait for confirmation
            time.sleep(3)
            
            try:
                confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                
                if confirmed_txn.get('confirmed-round'):
                    return {
                        'success': True,
                        'transaction_id': tx_id,
                        'confirmed_round': confirmed_txn.get('confirmed-round'),
                        'note': 'Supply operation successful!'
                    }
                    
                elif confirmed_txn.get('pool-error'):
                    error_msg = confirmed_txn.get('pool-error')
                    return {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': error_msg,
                        'note': 'Supply operation failed'
                    }
                else:
                    return {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': 'Transaction pending',
                        'note': 'Supply operation pending'
                    }
                    
            except Exception as e:
                return {
                    'success': False,
                    'transaction_id': tx_id,
                    'error': str(e),
                    'note': 'Error checking supply transaction'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'note': 'Supply operation creation failed'
            }
    
    def execute_borrow_through_api(self, asset_id: int, amount: int) -> Dict:
        """Execute borrow operation through API"""
        print(f"💳 Executing borrow operation: {amount} of asset {asset_id}")
        
        try:
            # Create the borrow transaction
            params = self.algod_client.suggested_params()
            
            # Folks Finance borrow operation
            borrow_txn = ApplicationCallTxn(
                sender=self.wallet_address,
                sp=params,
                index=465814065,  # Folks Finance App ID
                on_complete=0,  # NoOp
                app_args=[b'borrow'],
                accounts=[self.wallet_address],
                foreign_assets=[asset_id],
                foreign_apps=[]
            )
            
            # Sign and submit
            signed_txn = borrow_txn.sign(self.private_key)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            print(f"   📡 Borrow transaction submitted: {tx_id}")
            
            # Wait for confirmation
            time.sleep(3)
            
            try:
                confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                
                if confirmed_txn.get('confirmed-round'):
                    return {
                        'success': True,
                        'transaction_id': tx_id,
                        'confirmed_round': confirmed_txn.get('confirmed-round'),
                        'note': 'Borrow operation successful!'
                    }
                    
                elif confirmed_txn.get('pool-error'):
                    error_msg = confirmed_txn.get('pool-error')
                    return {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': error_msg,
                        'note': 'Borrow operation failed'
                    }
                else:
                    return {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': 'Transaction pending',
                        'note': 'Borrow operation pending'
                    }
                    
            except Exception as e:
                return {
                    'success': False,
                    'transaction_id': tx_id,
                    'error': str(e),
                    'note': 'Error checking borrow transaction'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'note': 'Borrow operation creation failed'
            }
    
    def test_different_approaches(self) -> Dict:
        """Test different approaches to bypass PC 297"""
        print("🧪 Testing different approaches...")
        
        test_results = {}
        
        # Approach 1: Try with different app_args
        print("   🔍 Approach 1: Different app_args...")
        different_args = [
            b'init_user',
            b'create_account',
            b'setup_user',
            b'register',
            b'activate'
        ]
        
        for arg in different_args:
            print(f"      Testing: {arg}")
            try:
                params = self.algod_client.suggested_params()
                
                test_txn = ApplicationCallTxn(
                    sender=self.wallet_address,
                    sp=params,
                    index=465814065,
                    on_complete=0,
                    app_args=[arg],
                    accounts=[self.wallet_address],
                    foreign_assets=[],
                    foreign_apps=[]
                )
                
                signed_txn = test_txn.sign(self.private_key)
                tx_id = self.algod_client.send_transaction(signed_txn)
                
                time.sleep(3)
                
                try:
                    confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                    
                    if confirmed_txn.get('confirmed-round'):
                        print(f"         ✅ SUCCESS with {arg}!")
                        return {
                            'success': True,
                            'working_arg': arg.decode(),
                            'transaction_id': tx_id,
                            'note': f'Operation successful with {arg}'
                        }
                    elif confirmed_txn.get('pool-error'):
                        error_msg = confirmed_txn.get('pool-error')
                        if 'pc=297' in error_msg:
                            print(f"         ❌ Still PC 297 with {arg}")
                        else:
                            print(f"         🎯 Different error with {arg}: {error_msg[:50]}...")
                    else:
                        print(f"         ⏳ Pending with {arg}")
                        
                except Exception as e:
                    print(f"         ⚠️ Error checking {arg}: {e}")
                
            except Exception as e:
                print(f"         ❌ Error with {arg}: {e}")
            
            time.sleep(1)
        
        # Approach 2: Try with different on_complete values
        print("   🔍 Approach 2: Different on_complete values...")
        on_complete_values = [1, 2, 3, 4]  # Create, Update, Delete, OptIn
        
        for on_complete in on_complete_values:
            print(f"      Testing on_complete: {on_complete}")
            try:
                params = self.algod_client.suggested_params()
                
                test_txn = ApplicationCallTxn(
                    sender=self.wallet_address,
                    sp=params,
                    index=465814065,
                    on_complete=on_complete,
                    app_args=[b'init'],
                    accounts=[self.wallet_address],
                    foreign_assets=[],
                    foreign_apps=[]
                )
                
                signed_txn = test_txn.sign(self.private_key)
                tx_id = self.algod_client.send_transaction(signed_txn)
                
                time.sleep(3)
                
                try:
                    confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                    
                    if confirmed_txn.get('confirmed-round'):
                        print(f"         ✅ SUCCESS with on_complete {on_complete}!")
                        return {
                            'success': True,
                            'working_on_complete': on_complete,
                            'transaction_id': tx_id,
                            'note': f'Operation successful with on_complete {on_complete}'
                        }
                    elif confirmed_txn.get('pool-error'):
                        error_msg = confirmed_txn.get('pool-error')
                        if 'pc=297' in error_msg:
                            print(f"         ❌ Still PC 297 with on_complete {on_complete}")
                        else:
                            print(f"         🎯 Different error with on_complete {on_complete}: {error_msg[:50]}...")
                    else:
                        print(f"         ⏳ Pending with on_complete {on_complete}")
                        
                except Exception as e:
                    print(f"         ⚠️ Error checking on_complete {on_complete}: {e}")
                
            except Exception as e:
                print(f"         ❌ Error with on_complete {on_complete}: {e}")
            
            time.sleep(1)
        
        return {
            'success': False,
            'note': 'All approaches tested - still hitting PC 297'
        }
    
    def run_complete_api_automation(self) -> Dict:
        """Run complete API automation"""
        print("🚀 COMPLETE API AUTOMATION")
        print("=" * 60)
        
        automation_results = {}
        
        try:
            # Step 1: Get protocol info
            print("📊 STEP 1: Getting protocol info...")
            protocol_info = self.get_protocol_info()
            automation_results['protocol_info'] = protocol_info
            
            # Step 2: Get markets info
            print("🏪 STEP 2: Getting markets info...")
            markets_info = self.get_markets_info()
            automation_results['markets_info'] = markets_info
            
            # Step 3: Get user portfolio
            print("👤 STEP 3: Getting user portfolio...")
            user_portfolio = self.get_user_portfolio()
            automation_results['user_portfolio'] = user_portfolio
            
            # Step 4: Test different approaches
            print("🧪 STEP 4: Testing different approaches...")
            approach_tests = self.test_different_approaches()
            automation_results['approach_tests'] = approach_tests
            
            # Step 5: Test supply operation
            print("💰 STEP 5: Testing supply operation...")
            supply_test = self.execute_supply_through_api(0, 1000000)  # 1 ALGO
            automation_results['supply_test'] = supply_test
            
            # Step 6: Test borrow operation
            print("💳 STEP 6: Testing borrow operation...")
            borrow_test = self.execute_borrow_through_api(31566704, 1000000)  # 1 USDC
            automation_results['borrow_test'] = borrow_test
            
        except Exception as e:
            print(f"❌ Error in API automation: {e}")
            automation_results['error'] = str(e)
        
        return automation_results

def main():
    """Test the Folks API agent"""
    print("🧪 TESTING FOLKS API AGENT")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Folks API Agent ready!")
    print("🎯 This system tests different approaches to bypass PC 297!")
    print("🔌 Uses API endpoints and different transaction parameters!")
    print("🔗 Import this into your hybrid trading empire for API-based DeFi!")

if __name__ == "__main__":
    main()
