#!/usr/bin/env python3
"""
RUN FINAL SOLUTION
Actually runs the complete Folks Finance solution to solve PC 297 validation
"""

from FOLKS_FINANCE_FINAL_SOLUTION import FolksFinanceFinalSolution
from algosdk.v2client import algod
import os

def main():
    """Run the complete Folks Finance solution"""
    print("🚀 RUNNING COMPLETE FOLKS FINANCE SOLUTION")
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
        
        # Initialize the final solution
        print("🔧 Initializing Folks Finance final solution...")
        final_solution = FolksFinanceFinalSolution(algod_client, wallet_address, private_key)
        
        # Run the complete solution
        print("🚀 Starting complete Folks Finance solution...")
        solution_results = final_solution.run_complete_solution()
        
        print("\n🎉 COMPLETE SOLUTION EXECUTED!")
        print("=" * 50)
        
        # Display results
        if solution_results.get('step') == 'complete':
            print("🎉 SUCCESS: Local state initialization completed!")
            print("🚀 DeFi operations should now work!")
            
            if 'defi_results' in solution_results:
                defi_results = solution_results['defi_results']
                if defi_results.get('success'):
                    print(f"✅ DeFi operation successful: {defi_results['working_operation']}")
                    print(f"   Transaction: {defi_results['transaction_id']}")
                    print("🎉 YOU NOW HAVE A WORKING DEFI SYSTEM!")
                else:
                    print("⚠️ DeFi operations still need refinement")
                    
        elif solution_results.get('step') == 'deFi_testing':
            print("✅ Local state was already ready!")
            if 'defi_results' in solution_results:
                defi_results = solution_results['defi_results']
                if defi_results.get('success'):
                    print(f"🎉 DeFi operation working: {defi_results['working_operation']}")
                    print("🚀 Your DeFi system is ready!")
                else:
                    print("🔍 DeFi operations need parameter tuning")
                    
        else:
            print("🔍 Solution completed, checking final state...")
            if 'final_state' in solution_results:
                final_state = solution_results['final_state']
                print(f"   Final state status: {final_state.get('status')}")
                print(f"   Uint count: {final_state.get('uint_count', 0)}")
        
        print(f"\n📁 Complete solution results saved to: folks_finance_complete_solution.json")
        print("🔗 This solution can now be integrated into your hybrid trading empire!")
        
    except Exception as e:
        print(f"❌ Error running final solution: {e}")

if __name__ == "__main__":
    main()
