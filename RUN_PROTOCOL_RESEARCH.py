#!/usr/bin/env python3
"""
RUN PROTOCOL RESEARCH
Actually runs the DeFi protocol research to find required assets
"""

from DEFI_PROTOCOL_RESEARCH import DeFiProtocolResearch
from algosdk.v2client import algod
import os

def main():
    """Run the DeFi protocol research system"""
    print("🚀 RUNNING DEFI PROTOCOL RESEARCH")
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
        
        # Initialize protocol research
        print("🔍 Initializing DeFi protocol research...")
        protocol_research = DeFiProtocolResearch(algod_client, wallet_address, private_key)
        
        # Run research
        print("🚀 Starting DeFi protocol research...")
        research_results = protocol_research.run_complete_research()
        
        print("\n🎉 PROTOCOL RESEARCH COMPLETE!")
        print("=" * 50)
        
        # Display key findings
        if 'known_assets_analysis' in research_results:
            known_assets = research_results['known_assets_analysis']
            print(f"📊 ASSET ANALYSIS RESULTS:")
            print(f"   Total assets analyzed: {known_assets['total_assets']}")
            print(f"   Working combinations found: {len(known_assets['working_combinations'])}")
            
            if known_assets['working_combinations']:
                print(f"\n🎉 SUCCESS: Found working asset combinations!")
                for combo in known_assets['working_combinations']:
                    print(f"   Assets: {combo['assets']}")
                    print(f"   Result: {combo['result']['note']}")
        
        if 'asset_combination_tests' in research_results:
            combination_tests = research_results['asset_combination_tests']
            if isinstance(combination_tests, dict) and combination_tests.get('success'):
                print(f"\n🎉 SUCCESS: Asset combination test successful!")
                working_combo = combination_tests['working_combination']
                print(f"   Working combination: {working_combo['name']}")
                print(f"   Assets: {working_combo['assets']}")
                print(f"   Description: {working_combo['description']}")
                print(f"   Transaction: {combination_tests['result']['transaction_id']}")
                print(f"🚀 YOU NOW HAVE A WORKING FOLKS FINANCE SYSTEM!")
            else:
                print(f"\n🔍 ASSET COMBINATION TESTING:")
                print(f"   Note: {combination_tests.get('note', 'Unknown')}")
                print("📊 Testing completed - need to refine asset combinations")
        
        print(f"\n📁 Protocol research saved to: defi_protocol_research.json")
        print("🔍 This research reveals the exact protocol requirements!")
        
    except Exception as e:
        print(f"❌ Error running protocol research: {e}")

if __name__ == "__main__":
    main()
