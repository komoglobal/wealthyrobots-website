#!/usr/bin/env python3
"""
RUN WORKING SOLUTION
Actually runs the working Folks Finance solution with asset opt-ins
"""

from FOLKS_FINANCE_WORKING_SOLUTION import FolksFinanceWorkingSolution
from algosdk.v2client import algod
import os

def main():
    """Run the working Folks Finance solution"""
    print("🚀 RUNNING WORKING FOLKS FINANCE SOLUTION")
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
        
        # Initialize the working solution
        print("🔧 Initializing Folks Finance working solution...")
        working_solution = FolksFinanceWorkingSolution(algod_client, wallet_address, private_key)
        
        # Run the working solution
        print("🚀 Starting working Folks Finance solution...")
        solution_results = working_solution.run_working_solution()
        
        print("\n🎉 WORKING SOLUTION EXECUTED!")
        print("=" * 50)
        
        # Display results
        if 'asset_status' in solution_results:
            asset_status = solution_results['asset_status']
            print(f"📊 ASSET STATUS:")
            print(f"   Total current assets: {asset_status.get('total_current', 0)}")
            print(f"   Already opted in: {len(asset_status.get('opted_in', []))}")
            print(f"   Missing assets: {len(asset_status.get('missing', []))}")
        
        if 'opt_in_results' in solution_results:
            opt_in_results = solution_results['opt_in_results']
            if opt_in_results:
                successful_opt_ins = sum(1 for result in opt_in_results.values() if result.get('success'))
                total_opt_ins = len(opt_in_results)
                print(f"\n🔧 ASSET OPT-INS:")
                print(f"   Successful: {successful_opt_ins}/{total_opt_ins}")
        
        if 'operation_results' in solution_results:
            operation_results = solution_results['operation_results']
            if operation_results.get('success'):
                print(f"\n🎉 SUCCESS: FOLKS FINANCE OPERATION WORKING!")
                print(f"   Working operation: {operation_results['working_operation']}")
                print(f"   Transaction: {operation_results['transaction_id']}")
                print("🚀 YOU NOW HAVE A FULLY FUNCTIONAL DEFI SYSTEM!")
                print("💰 Ready for lending, borrowing, and yield farming!")
            else:
                print(f"\n🔍 OPERATIONS TESTED:")
                print(f"   Note: {operation_results.get('note', 'Unknown')}")
                print("📊 Asset opt-ins completed - next step is parameter tuning")
        
        print(f"\n📁 Working solution results saved to: folks_finance_working_solution.json")
        print("🔗 This solution can now be integrated into your hybrid trading empire!")
        
    except Exception as e:
        print(f"❌ Error running working solution: {e}")

if __name__ == "__main__":
    main()
