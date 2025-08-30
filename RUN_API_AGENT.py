#!/usr/bin/env python3
"""
RUN API AGENT
Actually runs the Folks Finance API agent to test different approaches
"""

from FOLKS_API_AGENT import FolksAPIAgent
from algosdk.v2client import algod
import os

def main():
    """Run the Folks Finance API agent"""
    print("🚀 RUNNING FOLKS API AGENT")
    print("=" * 50)
    
    try:
        # Connect to Algorand
        print("🔗 Connecting to Algorand...")
        algod_client = algod.AlgodClient("", "https://mainnet-api.algonode.cloud")
        
        # Test connection
        status = algod_client.status()
        print(f"✅ Connected to Algorand mainnet: Block {status['last-round']}")
        
        # Load wallet credentials
        print("💰 Loading wallet credentials...")
        wallet_address = None
        private_key = None
        
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('ALGORAND_WALLET_ADDRESS='):
                        wallet_address = line.split('=')[1].strip()
                    elif line.startswith('ALGORAND_WALLET_MNEMONIC='):
                        from algosdk import mnemonic
                        mnemonic_phrase = line.split('=')[1].strip()
                        private_key = mnemonic.to_private_key(mnemonic_phrase)
        
        if not wallet_address or not private_key:
            print("❌ Wallet credentials not found in .env file")
            return
        
        print(f"✅ Wallet loaded: {wallet_address[:10]}...{wallet_address[-10:]}")
        
        # Initialize API agent
        print("🔍 Initializing Folks Finance API agent...")
        api_agent = FolksAPIAgent(algod_client, wallet_address, private_key)
        
        # Run automation
        print("🚀 Starting API automation...")
        automation_results = api_agent.run_complete_api_automation()
        
        print("\n🎉 API AUTOMATION COMPLETE!")
        print("=" * 50)
        
        # Display key results
        if 'protocol_info' in automation_results:
            protocol_info = automation_results['protocol_info']
            if 'error' not in protocol_info:
                print(f"📊 PROTOCOL INFO: {protocol_info['note']}")
            else:
                print(f"❌ Protocol info error: {protocol_info['error']}")
        
        if 'markets_info' in automation_results:
            markets_info = automation_results['markets_info']
            if 'error' not in markets_info:
                print(f"🏪 MARKETS INFO: {markets_info['note']}")
            else:
                print(f"❌ Markets info error: {markets_info['error']}")
        
        if 'user_portfolio' in automation_results:
            user_portfolio = automation_results['user_portfolio']
            if 'error' not in user_portfolio:
                print(f"👤 USER PORTFOLIO: {user_portfolio['note']}")
            else:
                print(f"❌ User portfolio error: {user_portfolio['error']}")
        
        if 'approach_tests' in automation_results:
            approach_tests = automation_results['approach_tests']
            if approach_tests.get('success'):
                print(f"\n🎉 SUCCESS: Found working approach!")
                if 'working_arg' in approach_tests:
                    print(f"   Working argument: {approach_tests['working_arg']}")
                if 'working_on_complete' in approach_tests:
                    print(f"   Working on_complete: {approach_tests['working_on_complete']}")
                print(f"   Transaction: {approach_tests['transaction_id']}")
                print(f"   Note: {approach_tests['note']}")
                print(f"\n🚀 YOU NOW HAVE A WORKING FOLKS FINANCE APPROACH!")
            else:
                print(f"\n🔍 APPROACH TESTING:")
                print(f"   Note: {approach_tests['note']}")
                print(f"   All approaches still hitting PC 297")
        
        if 'supply_test' in automation_results:
            supply_test = automation_results['supply_test']
            if 'error' not in supply_test:
                if supply_test.get('success'):
                    print(f"\n💰 SUPPLY TEST: SUCCESS!")
                    print(f"   Transaction: {supply_test['transaction_id']}")
                    print(f"   Confirmed: Round {supply_test['confirmed_round']}")
                else:
                    print(f"\n💰 SUPPLY TEST: {supply_test['note']}")
            else:
                print(f"\n❌ Supply test error: {supply_test['error']}")
        
        if 'borrow_test' in automation_results:
            borrow_test = automation_results['borrow_test']
            if 'error' not in borrow_test:
                if borrow_test.get('success'):
                    print(f"\n💳 BORROW TEST: SUCCESS!")
                    print(f"   Transaction: {borrow_test['transaction_id']}")
                    print(f"   Confirmed: Round {borrow_test['confirmed_round']}")
                else:
                    print(f"\n💳 BORROW TEST: {borrow_test['note']}")
            else:
                print(f"\n❌ Borrow test error: {borrow_test['error']}")
        
        # Check for errors
        if 'error' in automation_results:
            print(f"\n❌ AUTOMATION ERROR: {automation_results['error']}")
            print(f"🔍 Need to debug the automation process")
        
        print(f"\n📁 API automation results saved to: folks_api_automation.json")
        print("🔍 This shows which approaches work and which don't!")
        
    except Exception as e:
        print(f"❌ Error running API agent: {e}")

if __name__ == "__main__":
    main()
