#!/usr/bin/env python3
"""
RUN UPDATE SOLVER
Actually runs the Folks Finance Update solver
"""

from FOLKS_UPDATE_SOLVER import FolksUpdateSolver
from algosdk.v2client import algod
import os

def main():
    """Run the Folks Finance Update solver"""
    print("🚀 RUNNING FOLKS UPDATE SOLVER")
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
        
        # Initialize Update solver
        print("🔍 Initializing Folks Finance Update solver...")
        update_solver = FolksUpdateSolver(algod_client, wallet_address, private_key)
        
        # Run solving
        print("🚀 Starting Update solving...")
        solving_results = update_solver.run_complete_solving()
        
        print("\n🎉 UPDATE SOLVING COMPLETE!")
        print("=" * 50)
        
        # Display key results
        if 'update_operations' in solving_results:
            update_ops = solving_results['update_operations']
            if isinstance(update_ops, dict) and update_ops.get('success'):
                print(f"\n🎉 SUCCESS: Found working Update operation!")
                working_op = update_ops['working_operation']
                print(f"   Operation: {working_op['name']}")
                print(f"   Description: {working_op['description']}")
                print(f"   Transaction: {update_ops['result']['transaction_id']}")
                print(f"   Confirmed: Round {update_ops['result']['confirmed_round']}")
                print(f"\n🚀 YOU NOW HAVE A WORKING FOLKS FINANCE UPDATE OPERATION!")
                print(f"💡 This bypasses the PC 297 error completely!")
            else:
                print(f"\n🔍 UPDATE OPERATIONS TESTING:")
                print(f"   Note: {update_ops.get('note', 'Unknown')}")
                print(f"   All Update operations tested")
        
        if 'update_with_assets' in solving_results:
            update_with_assets = solving_results['update_with_assets']
            if isinstance(update_with_assets, dict) and update_with_assets.get('success'):
                print(f"\n🎉 SUCCESS: Found working Update with assets!")
                working_combo = update_with_assets['working_combo']
                print(f"   Combination: {working_combo['name']}")
                print(f"   Assets: {working_combo['assets']}")
                print(f"   Transaction: {update_with_assets['result']['transaction_id']}")
                print(f"   Confirmed: Round {update_with_assets['result']['confirmed_round']}")
            else:
                print(f"\n💰 UPDATE WITH ASSETS:")
                print(f"   Note: {update_with_assets.get('note', 'Unknown')}")
        
        if 'update_with_accounts' in solving_results:
            update_with_accounts = solving_results['update_with_accounts']
            if isinstance(update_with_accounts, dict) and update_with_accounts.get('success'):
                print(f"\n🎉 SUCCESS: Found working Update with accounts!")
                working_combo = update_with_accounts['working_combo']
                print(f"   Combination: {working_combo['name']}")
                print(f"   Accounts: {len(working_combo['accounts'])}")
                print(f"   Transaction: {update_with_accounts['result']['transaction_id']}")
                print(f"   Confirmed: Round {update_with_accounts['result']['confirmed_round']}")
            else:
                print(f"\n👥 UPDATE WITH ACCOUNTS:")
                print(f"   Note: {update_with_accounts.get('note', 'Unknown')}")
        
        # Check for errors
        if 'error' in solving_results:
            print(f"\n❌ SOLVING ERROR: {solving_results['error']}")
            print(f"🔍 Need to debug the solving process")
        
        print(f"\n📁 Update solving results saved to: folks_update_solving.json")
        print("🔍 This shows which Update operations work!")
        
        # Summary
        print(f"\n📊 SOLVING SUMMARY:")
        print("=" * 30)
        
        success_count = 0
        if 'update_operations' in solving_results and solving_results['update_operations'].get('success'):
            success_count += 1
        if 'update_with_assets' in solving_results and solving_results['update_with_assets'].get('success'):
            success_count += 1
        if 'update_with_accounts' in solving_results and solving_results['update_with_accounts'].get('success'):
            success_count += 1
        
        print(f"   Successful approaches: {success_count}/3")
        
        if success_count > 0:
            print(f"   🎉 Update approach is working!")
            print(f"   🚀 Ready to implement DeFi operations!")
        else:
            print(f"   ⚠️ Update approach needs refinement")
            print(f"   🔍 Need to investigate further")
        
    except Exception as e:
        print(f"❌ Error running Update solver: {e}")

if __name__ == "__main__":
    main()
