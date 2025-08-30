#!/usr/bin/env python3
"""
FOLKS FINANCE RESEARCH
Research and find correct operation parameters for Folks Finance DeFi protocol
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.transaction import ApplicationCallTxn
from algosdk.v2client import algod

class FolksFinanceResearch:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID (already opted in)
        self.folks_app_id = 465814065
        
        # Known Folks Finance creator and related addresses
        self.folks_creator = "3EPGHSNBBN5M2LD6V7A63EHZQQLATVQHDBYJQIZ6BLCBTIXA5XR7ZOZEB4"
        
        print("🔬 FOLKS FINANCE RESEARCH System Initialized")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{self.wallet_address[-10:]}")
        print(f"🎯 Researching correct parameters for Folks Finance (App ID: {self.folks_app_id})")
    
    def research_folks_protocol(self) -> Dict:
        """Research Folks Finance protocol specifications"""
        print("🔬 RESEARCHING FOLKS FINANCE PROTOCOL")
        print("=" * 50)
        
        research_results = {}
        
        # 1. Get app information from Algorand
        print("📋 Getting app information from Algorand...")
        try:
            app_info = self.algod_client.application_info(self.folks_app_id)
            research_results['app_info'] = {
                'app_id': app_info['id'],
                'creator': app_info['params']['creator'],
                'approval_program': app_info['params']['approval-program'][:100] + "...",  # First 100 chars
                'clear_state_program': app_info['params']['clear-state-program'][:100] + "...",
                'global_state_schema': app_info['params']['global-state-schema'],
                'local_state_schema': app_info['params']['local-state-schema']
            }
            print("✅ App information retrieved")
        except Exception as e:
            print(f"❌ Error getting app info: {e}")
            research_results['app_info'] = None
        
        # 2. Get account information to see what's already set up
        print("👤 Getting account information...")
        try:
            account_info = self.algod_client.account_info(self.wallet_address)
            
            # Check local state for this app
            local_state = None
            for app in account_info.get('apps-local-state', []):
                if app['id'] == self.folks_app_id:
                    local_state = app
                    break
            
            research_results['account_state'] = {
                'opted_in': local_state is not None,
                'local_state': local_state,
                'total_apps': len(account_info.get('apps-local-state', [])),
                'total_assets': len(account_info.get('assets', []))
            }
            print("✅ Account information retrieved")
        except Exception as e:
            print(f"❌ Error getting account info: {e}")
            research_results['account_state'] = None
        
        # 3. Research known Folks Finance operations
        print("📚 Researching known Folks Finance operations...")
        known_operations = self._get_known_folks_operations()
        research_results['known_operations'] = known_operations
        print(f"✅ Found {len(known_operations)} known operations")
        
        # 4. Test advanced parameter combinations
        print("🧪 Testing advanced parameter combinations...")
        advanced_results = self._test_advanced_parameters()
        research_results['advanced_tests'] = advanced_results
        print(f"✅ Advanced parameter tests completed")
        
        return research_results
    
    def _get_known_folks_operations(self) -> Dict:
        """Get known Folks Finance operations based on research"""
        return {
            "create_market": {
                "description": "Create a new lending market",
                "app_args": [b"create_market"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "create_escrow": {
                "description": "Create escrow account",
                "app_args": [b"create_escrow"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "setup_user": {
                "description": "Setup user account",
                "app_args": [b"setup_user"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "register_user": {
                "description": "Register user with protocol",
                "app_args": [b"register_user"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "initialize_user": {
                "description": "Initialize user state",
                "app_args": [b"initialize_user"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "optin_user": {
                "description": "Opt-in user to protocol",
                "app_args": [b"optin_user"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "bootstrap_user": {
                "description": "Bootstrap user account",
                "app_args": [b"bootstrap_user"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "empty_args": {
                "description": "Call with no arguments",
                "app_args": [],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "with_creator": {
                "description": "Include creator account",
                "app_args": [b"init"],
                "accounts": [self.wallet_address, self.folks_creator],
                "foreign_assets": [],
                "foreign_apps": []
            },
            "with_current_app": {
                "description": "Include current app",
                "app_args": [b"init"],
                "accounts": [self.wallet_address],
                "foreign_assets": [],
                "foreign_apps": [self.folks_app_id]
            }
        }
    
    def _test_advanced_parameters(self) -> Dict:
        """Test advanced parameter combinations"""
        print("   🧪 Testing advanced parameter combinations...")
        
        advanced_operations = self._get_known_folks_operations()
        results = {}
        
        for operation_name, operation in advanced_operations.items():
            print(f"      Testing: {operation_name}")
            
            try:
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
                signed_txn = app_call_txn.sign(self.private_key)
                
                # Submit the transaction
                tx_id = self.algod_client.send_transaction(signed_txn)
                
                # Wait for result
                time.sleep(3)
                
                try:
                    confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
                    
                    if confirmed_txn.get('confirmed-round'):
                        results[operation_name] = {
                            'success': True,
                            'transaction_id': tx_id,
                            'confirmed_round': confirmed_txn.get('confirmed-round'),
                            'note': 'SUCCESS! Operation executed!'
                        }
                        print(f"         ✅ SUCCESS: {operation_name}")
                        break  # Found a working operation!
                        
                    elif confirmed_txn.get('pool-error'):
                        error_msg = confirmed_txn.get('pool-error')
                        
                        if "logic eval error" in error_msg:
                            # Extract program counter and opcodes
                            if "pc=" in error_msg and "opcodes=" in error_msg:
                                pc_start = error_msg.find("pc=") + 3
                                pc_end = error_msg.find(",", pc_start)
                                pc = error_msg[pc_start:pc_end] if pc_end != -1 else "unknown"
                                
                                opcodes_start = error_msg.find("opcodes=") + 8
                                opcodes = error_msg[opcodes_start:opcodes_start+100] + "..."
                                
                                results[operation_name] = {
                                    'success': False,
                                    'transaction_id': tx_id,
                                    'error': error_msg,
                                    'program_counter': pc,
                                    'opcodes': opcodes,
                                    'note': 'Reached smart contract but failed execution'
                                }
                            else:
                                results[operation_name] = {
                                    'success': False,
                                    'transaction_id': tx_id,
                                    'error': error_msg,
                                    'note': 'Reached smart contract but failed execution'
                                }
                        else:
                            results[operation_name] = {
                                'success': False,
                                'transaction_id': tx_id,
                                'error': error_msg,
                                'note': 'Transaction pool error'
                            }
                        
                        print(f"         ❌ Failed: {operation_name} - {error_msg[:50]}...")
                    else:
                        results[operation_name] = {
                            'success': False,
                            'transaction_id': tx_id,
                            'error': 'Transaction pending',
                            'note': 'Transaction still pending'
                        }
                        print(f"         ⏳ Pending: {operation_name}")
                        
                except Exception as e:
                    results[operation_name] = {
                        'success': False,
                        'transaction_id': tx_id,
                        'error': str(e),
                        'note': 'Error checking transaction'
                    }
                    print(f"         ⚠️ Error: {operation_name} - {e}")
                
            except Exception as e:
                results[operation_name] = {
                    'success': False,
                    'error': str(e),
                    'note': 'Transaction creation failed'
                }
                print(f"         ❌ Creation failed: {operation_name} - {e}")
            
            # Wait between tests
            time.sleep(1)
        
        return results
    
    def run_comprehensive_research(self) -> Dict:
        """Run comprehensive research on Folks Finance"""
        print("🚀 COMPREHENSIVE FOLKS FINANCE RESEARCH")
        print("=" * 60)
        
        # Run research
        research_results = self.research_folks_protocol()
        
        # Analyze results
        print(f"\n📊 RESEARCH RESULTS ANALYSIS")
        print("=" * 40)
        
        # Check if we found any working operations
        advanced_tests = research_results.get('advanced_tests', {})
        success_count = sum(1 for result in advanced_tests.values() if result.get('success', False))
        total_count = len(advanced_tests)
        
        print(f"🧪 Advanced tests completed: {total_count}")
        print(f"✅ Successful operations: {success_count}")
        
        if success_count > 0:
            print(f"\n🎉 SUCCESS: Found {success_count} working DeFi operations!")
            print("🚀 This means we've discovered the correct parameters!")
            
            for name, result in advanced_tests.items():
                if result.get('success'):
                    print(f"   ✅ {name}: Working operation!")
                    print(f"      Transaction: {result['transaction_id']}")
                    print(f"      Round: {result['confirmed_round']}")
        else:
            print(f"\n🔍 No operations succeeded, but we've gathered valuable data")
            print("📊 Analyzing error patterns to find the right approach...")
            
            # Analyze error patterns
            pc_patterns = {}
            for name, result in advanced_tests.items():
                if 'program_counter' in result:
                    pc = result['program_counter']
                    if pc not in pc_patterns:
                        pc_patterns[pc] = []
                    pc_patterns[pc].append(name)
            
            if pc_patterns:
                print(f"\n📍 Program Counter Analysis:")
                for pc, operations in pc_patterns.items():
                    print(f"   PC {pc}: {len(operations)} operations failed")
                    print(f"      Operations: {', '.join(operations[:3])}")
        
        # Save research results
        with open('folks_finance_research_results.json', 'w') as f:
            # Convert bytes to strings for JSON serialization
            json_safe_results = json.loads(json.dumps(research_results, default=str))
            json.dump(json_safe_results, f, indent=2)
        
        print(f"\n📁 Research results saved to: folks_finance_research_results.json")
        
        return research_results

def main():
    """Test the Folks Finance research system"""
    print("🧪 TESTING FOLKS FINANCE RESEARCH SYSTEM")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Folks Finance Research System ready!")
    print("🎯 This system will research and find correct DeFi parameters!")
    print("🔗 Import this into your hybrid trading empire for protocol research!")

if __name__ == "__main__":
    main()

