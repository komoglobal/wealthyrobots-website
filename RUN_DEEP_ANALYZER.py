#!/usr/bin/env python3
"""
RUN DEEP ANALYZER
Actually runs the deep PC 297 analyzer to understand validation logic
"""

from DEEP_PC_297_ANALYZER import DeepPC297Analyzer
from algosdk.v2client import algod
import os

def main():
    """Run the deep PC 297 analyzer"""
    print("🚀 RUNNING DEEP PC 297 ANALYZER")
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
        
        # Initialize deep analyzer
        print("🔍 Initializing deep PC 297 analyzer...")
        deep_analyzer = DeepPC297Analyzer(algod_client, wallet_address, private_key)
        
        # Run deep analysis
        print("🚀 Starting deep PC 297 analysis...")
        analysis_results = deep_analyzer.run_deep_analysis()
        
        print("\n🎉 DEEP PC 297 ANALYSIS COMPLETE!")
        print("=" * 50)
        
        # Display key findings
        if 'validation_logic' in analysis_results:
            validation = analysis_results['validation_logic']
            print(f"🔍 VALIDATION LOGIC DISCOVERED:")
            for key, description in validation.items():
                print(f"   • {key}: {description}")
        
        if 'context_analysis' in analysis_results:
            context = analysis_results['context_analysis']
            print(f"\n🎯 PC 297 EXACT LOCATION:")
            print(f"   Byte position: {context['start_pos']}-{context['end_pos']}")
            print(f"   Context hex: {context['context_hex'][:100]}...")
        
        print(f"\n📁 Deep analysis results saved to: deep_pc_297_analysis.json")
        print("🔍 This analysis reveals the exact validation requirements!")
        
    except Exception as e:
        print(f"❌ Error running deep analyzer: {e}")

if __name__ == "__main__":
    main()
