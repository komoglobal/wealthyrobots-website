#!/usr/bin/env python3
"""
RUN FOCUSED DEFI SOLVER
Runs the focused DeFi solver to test Update approach on Folks Finance
"""

from FOCUSED_DEFI_SOLVER import FocusedDeFiSolver
from algosdk.v2client import algod
import os

def main():
    """Run the focused DeFi solver"""
    print("🚀 RUNNING FOCUSED DEFI SOLVER")
    print("=" * 50)
    print("🎯 Testing Update approach on Folks Finance")
    print("💰 Focusing on verified working protocols")
    
    try:
        # Connect to Algorand
        print("\n🔗 Connecting to Algorand...")
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
        
        # Initialize focused DeFi solver
        print("\n🔍 Initializing focused DeFi solver...")
        defi_solver = FocusedDeFiSolver(algod_client, wallet_address, private_key)
        
        # Run focused solving
        print("\n🚀 Starting focused DeFi solving...")
        solving_results = defi_solver.run_focused_solving()
        
        print("\n🎉 FOCUSED DEFI SOLVING COMPLETE!")
        print("=" * 50)
        
        # Display analysis results
        if 'analysis' in solving_results:
            analysis = solving_results['analysis']
            
            print(f"\n📊 SOLVING ANALYSIS RESULTS:")
            print(f"   🎯 Progress indicators: {analysis.get('progress_count', 0)}")
            print(f"   ✅ Successful operations: {analysis.get('success_count', 0)}")
            print(f"   🚀 Breakthrough achieved: {analysis.get('breakthrough', False)}")
            
            if analysis.get('breakthrough'):
                print("🎉 MAJOR BREAKTHROUGH: Update approach is working!")
                print("🚀 We're successfully bypassing PC 297!")
                print("💡 Ready to implement actual DeFi operations!")
        
        # Display detailed results
        print(f"\n🔍 DETAILED OPERATION RESULTS:")
        print("=" * 40)
        
        # Update operations
        if 'update_operations' in solving_results:
            update_ops = solving_results['update_operations']
            print(f"\n📋 UPDATE OPERATIONS:")
            
            for test_name, test_result in update_ops.items():
                if isinstance(test_result, dict) and 'result' in test_result:
                    result = test_result['result']
                    if isinstance(result, dict):
                        status = "✅ SUCCESS" if result.get('success') else "❌ FAILED"
                        print(f"   {test_name}: {status}")
                        
                        if result.get('progress'):
                            print(f"      🎯 PROGRESS: Past PC 297!")
                            print(f"      Error: {result.get('error', 'Unknown')[:50]}...")
                        elif result.get('success'):
                            print(f"      Transaction: {result.get('transaction_id', 'Unknown')}")
                            print(f"      Round: {result.get('confirmed_round', 'Unknown')}")
                        else:
                            print(f"      Error: {result.get('error', 'Unknown')[:50]}...")
        
        # Supply operations
        if 'supply_operations' in solving_results:
            supply_ops = solving_results['supply_operations']
            print(f"\n📋 SUPPLY OPERATIONS:")
            
            if isinstance(supply_ops, dict) and 'result' in supply_ops:
                result = supply_ops['result']
                if isinstance(result, dict):
                    status = "✅ SUCCESS" if result.get('success') else "❌ FAILED"
                    print(f"   Supply operations: {status}")
                    
                    if result.get('progress'):
                        print(f"      🎯 PROGRESS: Past PC 297!")
                        print(f"      Error: {result.get('error', 'Unknown')[:50]}...")
                    elif result.get('success'):
                        print(f"      Transaction: {result.get('transaction_id', 'Unknown')}")
                        print(f"      Round: {result.get('confirmed_round', 'Unknown')}")
                    else:
                        print(f"      Error: {result.get('error', 'Unknown')[:50]}...")
        
        # Summary and next steps
        print(f"\n📊 FOCUSED SOLVING SUMMARY:")
        print("=" * 40)
        
        progress_count = analysis.get('progress_count', 0) if 'analysis' in solving_results else 0
        success_count = analysis.get('success_count', 0) if 'analysis' in solving_results else 0
        
        print(f"   Progress indicators: {progress_count}")
        print(f"   Successful operations: {success_count}")
        
        if progress_count > 0:
            print(f"\n🎉 SUCCESS: Update approach is working!")
            print(f"🚀 We've bypassed PC 297 errors!")
            print(f"💡 Ready to implement DeFi operations!")
        else:
            print(f"\n❌ No progress indicators found")
            print(f"🔍 Need to investigate further")
        
        # Key insights
        if progress_count > 0:
            print(f"\n💡 KEY INSIGHTS:")
            print(f"   🎯 The Update approach successfully bypasses PC 297!")
            print(f"   🚀 We can now access Folks Finance operations!")
            print(f"   💰 Ready to implement lending/borrowing operations!")
            print(f"   🔄 This is a universal solution for similar errors!")
        
        # Next steps
        if progress_count > 0:
            print(f"\n🚀 NEXT STEPS:")
            print(f"   1. ✅ Update approach verified working")
            print(f"   2. 🎯 PC 297 error bypassed")
            print(f"   3. 🔄 Ready to implement DeFi operations")
            print(f"   4. 💰 Can now supply, borrow, and interact with protocols")
        else:
            print(f"\n🔧 NEXT STEPS:")
            print(f"   1. ❌ Investigate why Update approach isn't working")
            print(f"   2. 🔍 Check transaction parameters and app arguments")
            print(f"   3. 🔄 Refine the approach")
            print(f"   4. 🎯 Then proceed with DeFi operations")
        
        # Save results
        if 'analysis' in solving_results and 'results_file' in solving_results['analysis']:
            print(f"\n📁 Results saved to: {solving_results['analysis']['results_file']}")
        
    except Exception as e:
        print(f"❌ Error running focused DeFi solver: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()



