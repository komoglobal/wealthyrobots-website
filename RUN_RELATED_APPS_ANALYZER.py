#!/usr/bin/env python3
"""
RUN RELATED APPS ANALYZER
Actually runs the related apps analyzer to find required assets
"""

from RELATED_APPS_ANALYZER import RelatedAppsAnalyzer
from algosdk.v2client import algod
import os

def main():
    """Run the related apps analyzer"""
    print("🚀 RUNNING RELATED APPS ANALYZER")
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
        
        # Initialize related apps analyzer
        print("🔍 Initializing related apps analyzer...")
        related_apps_analyzer = RelatedAppsAnalyzer(algod_client, wallet_address, private_key)
        
        # Run analysis
        print("🚀 Starting related apps analysis...")
        analysis_results = related_apps_analyzer.run_complete_analysis()
        
        print("\n🎉 RELATED APPS ANALYSIS COMPLETE!")
        print("=" * 50)
        
        # Display key findings
        if 'all_discovered_assets' in analysis_results:
            all_assets = analysis_results['all_discovered_assets']
            if all_assets['unique_asset_ids']:
                print(f"🎯 KEY DISCOVERY: Found {len(all_assets['unique_asset_ids'])} required assets!")
                print("🔍 These are the exact assets Folks Finance expects:")
                for asset_id in all_assets['unique_asset_ids']:
                    print(f"   • Asset ID: {asset_id}")
                
                print(f"\n🚀 NEXT STEP: Opt into these specific assets!")
                print("💰 This should solve the PC 297 validation issue!")
            else:
                print("🔍 No specific asset IDs found in related apps")
                print("📊 Need to analyze other protocol aspects")
        
        print(f"\n📁 Related apps analysis saved to: related_apps_analysis.json")
        print("🔍 This analysis will reveal the exact protocol requirements!")
        
    except Exception as e:
        print(f"❌ Error running related apps analyzer: {e}")

if __name__ == "__main__":
    main()
