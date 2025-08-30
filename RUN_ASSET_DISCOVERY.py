#!/usr/bin/env python3
"""
RUN ASSET DISCOVERY
Actually runs the Folks asset discovery to find required assets
"""

from FOLKS_ASSET_DISCOVERY import FolksAssetDiscovery
from algosdk.v2client import algod
import os

def main():
    """Run the Folks asset discovery system"""
    print("🚀 RUNNING FOLKS ASSET DISCOVERY")
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
        
        # Initialize asset discovery
        print("🔍 Initializing Folks asset discovery...")
        asset_discovery = FolksAssetDiscovery(algod_client, wallet_address, private_key)
        
        # Run asset discovery
        print("🚀 Starting Folks asset discovery...")
        discovery_results = asset_discovery.run_complete_discovery()
        
        print("\n🎉 ASSET DISCOVERY COMPLETE!")
        print("=" * 50)
        
        # Display key findings
        if 'asset_references' in discovery_results:
            asset_refs = discovery_results['asset_references']
            if asset_refs['asset_ids']:
                print(f"🎯 KEY DISCOVERY: Found {len(asset_refs['asset_ids'])} required assets!")
                print("🔍 These are the exact assets Folks Finance expects:")
                for ref in asset_refs['asset_ids']:
                    print(f"   • Asset ID: {ref['asset_id']}")
                    print(f"     From key: '{ref['key']}'")
                
                print(f"\n🚀 NEXT STEP: Opt into these specific assets!")
                print("💰 This should solve the PC 297 validation issue!")
            else:
                print("🔍 No specific asset IDs found in global state")
                print("📊 Need to analyze other protocol aspects")
        
        print(f"\n📁 Asset discovery results saved to: folks_asset_discovery.json")
        print("🔍 This discovery will reveal the exact protocol requirements!")
        
    except Exception as e:
        print(f"❌ Error running asset discovery: {e}")

if __name__ == "__main__":
    main()
