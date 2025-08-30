#!/usr/bin/env python3
"""
RUN FOLKS RESEARCH
Actually runs the Folks Finance research to find correct operation parameters
"""

from FOLKS_FINANCE_RESEARCH import FolksFinanceResearch
from algosdk.v2client import algod
import os

def main():
    """Run the Folks Finance research system"""
    print("🚀 RUNNING FOLKS FINANCE RESEARCH")
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
        
        # Initialize Folks Finance research system
        print("🔍 Initializing Folks Finance research system...")
        folks_research = FolksFinanceResearch(algod_client, wallet_address, private_key)
        
        # Run comprehensive research
        print("🚀 Starting comprehensive Folks Finance research...")
        research_results = folks_research.run_comprehensive_research()
        
        print("\n🎉 FOLKS FINANCE RESEARCH COMPLETE!")
        print("=" * 50)
        
        # Display final results
        advanced_tests = research_results.get('advanced_tests', {})
        success_count = sum(1 for result in advanced_tests.values() if result.get('success', False))
        total_count = len(advanced_tests)
        
        if success_count > 0:
            print(f"🎉 SUCCESS: Found {success_count} working DeFi operations!")
            print("🚀 This means we've discovered the correct parameters!")
            print("💰 You can now execute actual DeFi trades!")
        else:
            print(f"🔍 No operations succeeded, but we've gathered valuable research data")
            print("📊 The research will help us understand the correct approach")
        
        print(f"\n📁 Research results saved to: folks_finance_research_results.json")
        
    except Exception as e:
        print(f"❌ Error running Folks Finance research: {e}")

if __name__ == "__main__":
    main()

