#!/usr/bin/env python3
"""
RUN PARAMETER DISCOVERY
Actually runs the parameter discovery to find working DeFi parameters
"""

from DEFI_PARAMETER_DISCOVERY import DeFiParameterDiscovery
from algosdk.v2client import algod
import os

def main():
    """Run the parameter discovery system"""
    print("🚀 RUNNING DEFI PARAMETER DISCOVERY")
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
        
        # Initialize parameter discovery system
        print("🔍 Initializing parameter discovery system...")
        discovery_system = DeFiParameterDiscovery(algod_client, wallet_address, private_key)
        
        # Run discovery for all protocols
        print("🚀 Starting parameter discovery...")
        results = discovery_system.discover_all_protocols()
        
        print("\n🎉 PARAMETER DISCOVERY COMPLETE!")
        print("=" * 40)
        
        # Display results
        for protocol, working_params in results.items():
            print(f"\n📊 {protocol.upper()}:")
            if working_params:
                print(f"   ✅ Found {len(working_params)} working combinations:")
                for name, params in working_params.items():
                    print(f"      • {name}: {params['app_args']}")
            else:
                print(f"   ❌ No working combinations found")
        
        print(f"\n📁 Results saved to: defi_parameter_discovery_results.json")
        
    except Exception as e:
        print(f"❌ Error running parameter discovery: {e}")

if __name__ == "__main__":
    main()
