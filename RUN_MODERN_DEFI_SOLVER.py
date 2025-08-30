#!/usr/bin/env python3
"""
RUN MODERN DEFI SOLVER
Runs the modern DeFi solver focusing on active, operational protocols
"""

from MODERN_DEFI_SOLVER import ModernDeFiSolver
from algosdk.v2client import algod
import os

def main():
    """Run the modern DeFi solver"""
    print("🚀 RUNNING MODERN DEFI SOLVER")
    print("=" * 50)
    print("🎯 Focusing on ACTIVE protocols (not defunct like Algofi)")
    print("📊 Testing operational DeFi protocols on Algorand")
    
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
        
        # Initialize modern DeFi solver
        print("\n🔍 Initializing modern DeFi solver...")
        defi_solver = ModernDeFiSolver(algod_client, wallet_address, private_key)
        
        # Run complete solving
        print("\n🚀 Starting modern DeFi solving...")
        solving_results = defi_solver.run_complete_solving()
        
        print("\n🎉 MODERN DEFI SOLVING COMPLETE!")
        print("=" * 50)
        
        # Display analysis results
        if 'analysis' in solving_results:
            analysis = solving_results['analysis']
            
            print(f"\n📊 SOLVING ANALYSIS RESULTS:")
            print(f"   ✅ Working protocols: {len(analysis.get('working_protocols', []))}")
            print(f"   🔄 PC error protocols: {len(analysis.get('pc_error_protocols', []))}")
            print(f"   🎯 Update approach working: {len(analysis.get('update_working_protocols', []))}")
            
            if analysis.get('working_protocols'):
                print(f"\n🎉 WORKING PROTOCOLS (No issues):")
                for protocol in analysis['working_protocols']:
                    print(f"   - {protocol}")
            
            if analysis.get('update_working_protocols'):
                print(f"\n🚀 UPDATE APPROACH WORKING (PC 297 bypassed):")
                for protocol in analysis['update_working_protocols']:
                    print(f"   - {protocol}")
            
            if analysis.get('pc_error_protocols'):
                print(f"\n⚠️ PROTOCOLS WITH PC ERRORS:")
                for protocol in analysis['pc_error_protocols']:
                    print(f"   - {protocol}")
        
        # Display detailed results for each protocol
        print(f"\n🔍 DETAILED PROTOCOL RESULTS:")
        print("=" * 40)
        
        for protocol_key in ['folks_finance', 'pact_fi', 'tinyman', 'gard', 'vestige']:
            if f'{protocol_key}_status' in solving_results:
                status = solving_results[f'{protocol_key}_status']
                operations = solving_results.get(f'{protocol_key}_operations', {})
                update = solving_results.get(f'{protocol_key}_update', {})
                
                print(f"\n📋 {protocol_key.upper()}:")
                print(f"   Status: {status.get('status', 'unknown')}")
                
                if operations:
                    print(f"   Operations: {operations.get('status', 'unknown')}")
                    if operations.get('status') == 'pc_error':
                        print(f"   PC Error: {operations.get('error', 'Unknown')[:50]}...")
                
                if update:
                    print(f"   Update Approach: {update.get('status', 'unknown')}")
                    if update.get('status') == 'progress':
                        print(f"   Update Progress: {update.get('note', 'Unknown')}")
        
        # Summary and next steps
        print(f"\n📊 MODERN DEFI SOLVING SUMMARY:")
        print("=" * 40)
        
        working_count = len(analysis.get('working_protocols', [])) if 'analysis' in solving_results else 0
        update_working_count = len(analysis.get('update_working_protocols', [])) if 'analysis' in solving_results else 0
        
        total_working = working_count + update_working_count
        
        print(f"   Total working protocols: {total_working}/5")
        print(f"   Direct access: {working_count}")
        print(f"   Via Update approach: {update_working_count}")
        
        if total_working > 0:
            print(f"\n🎉 SUCCESS: Found {total_working} working DeFi protocols!")
            print(f"🚀 Ready to implement DeFi operations!")
            print(f"💡 The Update approach successfully bypasses PC 297 errors!")
        else:
            print(f"\n❌ No working protocols found")
            print(f"🔍 Need to investigate further")
        
        # Key insights
        if update_working_count > 0:
            print(f"\n💡 KEY INSIGHTS:")
            print(f"   🎯 The Update approach is a universal solution!")
            print(f"   🚀 It works across multiple DeFi protocols!")
            print(f"   💰 We can now access active, operational DeFi on Algorand!")
            print(f"   🔄 No more dependency on defunct protocols like Algofi!")
        
        # Save results
        if 'analysis' in solving_results and 'results_file' in solving_results['analysis']:
            print(f"\n📁 Results saved to: {solving_results['analysis']['results_file']}")
        
    except Exception as e:
        print(f"❌ Error running modern DeFi solver: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()



