#!/usr/bin/env python3
"""
RUN PROTOCOL INITIALIZER
Actually runs the Folks Finance protocol initialization
"""

from FOLKS_PROTOCOL_INITIALIZER import FolksProtocolInitializer
from algosdk.v2client import algod
import os

def main():
    """Run the Folks Finance protocol initializer"""
    print("🚀 RUNNING FOLKS PROTOCOL INITIALIZER")
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
        
        # Initialize protocol initializer
        print("🔍 Initializing Folks Finance protocol initializer...")
        protocol_initializer = FolksProtocolInitializer(algod_client, wallet_address, private_key)
        
        # Run initialization
        print("🚀 Starting protocol initialization...")
        initialization_results = protocol_initializer.run_complete_initialization()
        
        print("\n🎉 PROTOCOL INITIALIZATION COMPLETE!")
        print("=" * 50)
        
        # Display key results
        if 'app_status' in initialization_results:
            app_status = initialization_results['app_status']
            if 'error' not in app_status:
                print(f"📊 APP STATUS: {app_status['current_state']}")
                print(f"   App ID: {app_status['app_id']}")
                print(f"   Is opted in: {app_status['is_opted_in']}")
        
        if 'app_opt_in' in initialization_results:
            app_opt_in = initialization_results['app_opt_in']
            if 'error' not in app_opt_in:
                print(f"🔗 APP OPT-IN: {app_opt_in['status']}")
                if app_opt_in['status'] == 'opted_in':
                    print(f"   Transaction: {app_opt_in['transaction_id']}")
                    print(f"   Confirmed: Round {app_opt_in['confirmed_round']}")
        
        if 'account_init' in initialization_results:
            account_init = initialization_results['account_init']
            if 'error' not in account_init:
                print(f"👤 ACCOUNT INIT: {account_init['status']}")
                if account_init['status'] == 'initialized':
                    print(f"   Transaction: {account_init['transaction_id']}")
                    print(f"   Confirmed: Round {account_init['confirmed_round']}")
        
        if 'basic_test' in initialization_results:
            basic_test = initialization_results['basic_test']
            if 'error' not in basic_test:
                print(f"🧪 BASIC TEST: {basic_test['status']}")
                if basic_test['status'] == 'success':
                    print(f"   Transaction: {basic_test['transaction_id']}")
                    print(f"   Confirmed: Round {basic_test['confirmed_round']}")
                    print(f"\n🎉 SUCCESS: Folks Finance protocol fully initialized!")
                    print(f"🚀 Ready for DeFi operations!")
                    print(f"💡 You can now execute supply, borrow, and other operations!")
                else:
                    print(f"   Note: {basic_test['note']}")
                    print(f"🔍 Need to investigate further")
        
        # Check for errors
        if 'error' in initialization_results:
            print(f"\n❌ INITIALIZATION ERROR: {initialization_results['error']}")
            print(f"🔍 Need to debug the initialization process")
        
        print(f"\n📁 Initialization results saved to: folks_protocol_initialization.json")
        print("🔍 This shows the exact protocol setup status!")
        
    except Exception as e:
        print(f"❌ Error running protocol initializer: {e}")

if __name__ == "__main__":
    main()
