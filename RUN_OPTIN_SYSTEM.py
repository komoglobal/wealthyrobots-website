#!/usr/bin/env python3
"""
RUN OPTIN SYSTEM
Actually runs the opt-in process for DeFi protocols
"""

from DEFI_OPTIN_SYSTEM import DeFiOptInSystem
from algosdk.v2client import algod
import os

def main():
    """Run the opt-in system"""
    print("🚀 RUNNING DEFI OPT-IN SYSTEM")
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
        
        # Initialize opt-in system
        print("🔍 Initializing opt-in system...")
        optin_system = DeFiOptInSystem(algod_client, wallet_address, private_key)
        
        # Run opt-in for all protocols
        print("🚀 Starting opt-in process...")
        results = optin_system.optin_to_all_protocols()
        
        print("\n🎉 OPT-IN PROCESS COMPLETE!")
        print("=" * 40)
        
        # Display results
        for protocol, result in results.items():
            print(f"\n📊 {protocol.upper()}:")
            if result['opted_in']:
                print(f"   ✅ SUCCESS: Opted in to App ID {result['app_id']}")
            else:
                print(f"   ❌ FAILED: Could not opt in to App ID {result['app_id']}")
        
        print(f"\n📁 Results saved to: defi_optin_results.json")
        
        # Check if we can now execute DeFi trades
        print("\n🔍 Checking if we can now execute DeFi trades...")
        for protocol, result in results.items():
            if result['opted_in']:
                app_id = result['app_id']
                if optin_system.check_optin_status(app_id):
                    print(f"   ✅ {protocol.upper()}: Ready for DeFi trading!")
                else:
                    print(f"   ❌ {protocol.upper()}: Opt-in verification failed")
            else:
                print(f"   ❌ {protocol.upper()}: Cannot trade - not opted in")
        
    except Exception as e:
        print(f"❌ Error running opt-in system: {e}")

if __name__ == "__main__":
    main()

