#!/usr/bin/env python3
"""
RUN OPTIN SOLVER
Runs the Folks Finance opt-in solver to enable Update operations
"""

from FOLKS_OPTIN_SOLVER import FolksOptInSolver
from algosdk.v2client import algod
import os

def main():
    """Run the Folks Finance opt-in solver"""
    print("🚀 RUNNING FOLKS FINANCE OPTIN SOLVER")
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
        
        # Initialize opt-in solver
        print("🔍 Initializing Folks Finance opt-in solver...")
        optin_solver = FolksOptInSolver(algod_client, wallet_address, private_key)
        
        # Run opt-in solving
        print("🚀 Starting opt-in solving...")
        solving_results = optin_solver.run_optin_solving()
        
        print("\n🎉 OPTIN SOLVING COMPLETE!")
        print("=" * 50)
        
        # Display results
        if 'current_status' in solving_results:
            current_status = solving_results['current_status']
            if current_status.get('opted_in'):
                print(f"✅ Account is opted into Folks Finance!")
                print(f"   App ID: {current_status.get('app_id')}")
                print(f"   Local State: {len(current_status.get('local_state', []))} keys")
            else:
                print(f"❌ Account is NOT opted into Folks Finance")
                print(f"   App ID: {current_status.get('app_id')}")
                if 'error' in current_status:
                    print(f"   Error: {current_status['error']}")
        
        if 'optin_result' in solving_results:
            optin_result = solving_results['optin_result']
            if optin_result.get('success'):
                print(f"\n🎉 OPTIN SUCCESSFUL!")
                print(f"   Transaction ID: {optin_result.get('transaction_id')}")
                print(f"   Confirmed Round: {optin_result.get('confirmed_round')}")
                print(f"   Note: {optin_result.get('note')}")
            else:
                print(f"\n❌ OPTIN FAILED")
                print(f"   Error: {optin_result.get('error', 'Unknown error')}")
                print(f"   Note: {optin_result.get('note')}")
        
        # Summary
        print(f"\n📊 OPTIN SOLVING SUMMARY:")
        print("=" * 30)
        
        ready_for_update = solving_results.get('ready_for_update', False)
        action_needed = solving_results.get('action_needed', 'unknown')
        
        if ready_for_update:
            print(f"   ✅ Account ready for Folks Finance operations!")
            print(f"   🚀 Can now use Update operations successfully!")
            print(f"   💡 The PC 297 error should be resolved!")
        else:
            print(f"   ❌ Account not ready for Folks Finance operations")
            print(f"   🔄 Action needed: {action_needed}")
            print(f"   💡 Need to complete opt-in first")
        
        # Next steps
        if ready_for_update:
            print(f"\n🚀 NEXT STEPS:")
            print(f"   1. ✅ Opt-in completed successfully")
            print(f"   2. 🎯 PC 297 error bypassed")
            print(f"   3. 🔄 Update operations should now work")
            print(f"   4. 💰 Ready to implement DeFi operations!")
        else:
            print(f"\n🔧 NEXT STEPS:")
            print(f"   1. ❌ Complete opt-in process")
            print(f"   2. 🔍 Investigate opt-in failures")
            print(f"   3. 🔄 Retry opt-in if needed")
            print(f"   4. 🎯 Then proceed with Update operations")
        
        # Save results
        if 'results_file' in solving_results:
            print(f"\n📁 Results saved to: {solving_results['results_file']}")
        
    except Exception as e:
        print(f"❌ Error running opt-in solver: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()



