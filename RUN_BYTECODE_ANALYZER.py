#!/usr/bin/env python3
"""
RUN BYTECODE ANALYZER
Actually runs the smart contract bytecode analyzer to understand validation logic
"""

from SMART_CONTRACT_BYTECODE_ANALYZER import SmartContractBytecodeAnalyzer
from algosdk.v2client import algod
import os

def main():
    """Run the smart contract bytecode analyzer"""
    print("🚀 RUNNING SMART CONTRACT BYTECODE ANALYZER")
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
        
        # Initialize bytecode analyzer
        print("🔍 Initializing smart contract bytecode analyzer...")
        bytecode_analyzer = SmartContractBytecodeAnalyzer(algod_client, wallet_address, private_key)
        
        # Run comprehensive analysis
        print("🚀 Starting comprehensive smart contract analysis...")
        analysis_results = bytecode_analyzer.run_comprehensive_analysis()
        
        print("\n🎉 SMART CONTRACT ANALYSIS COMPLETE!")
        print("=" * 50)
        
        # Display key findings
        if 'pc_297_analysis' in analysis_results:
            pc_analysis = analysis_results['pc_297_analysis']
            print(f"🎯 KEY FINDING: Program Counter 297 Analysis")
            print(f"   This is where ALL Folks Finance operations are failing!")
            
            if 'validation_patterns' in pc_analysis:
                patterns = pc_analysis['validation_patterns']
                for pattern, description in patterns.items():
                    print(f"   🔍 {pattern}: {description}")
            
            if 'context_bytes' in pc_analysis:
                context = pc_analysis['context_bytes']
                print(f"   📍 Byte context: {context['start_position']}-{context['end_position']}")
                print(f"   🔍 Context hex: {context['context_hex'][:100]}...")
        
        print(f"\n📁 Analysis results saved to: smart_contract_analysis_results.json")
        print("🔍 This analysis will help us understand the exact validation logic!")
        
    except Exception as e:
        print(f"❌ Error running bytecode analyzer: {e}")

if __name__ == "__main__":
    main()
