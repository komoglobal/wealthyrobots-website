#!/usr/bin/env python3
"""
RUN STATE ANALYZER
Actually runs the Folks Finance state analysis
"""

from FOLKS_STATE_ANALYZER import FolksStateAnalyzer
from algosdk.v2client import algod
import os

def main():
    """Run the Folks Finance state analyzer"""
    print("🚀 RUNNING FOLKS STATE ANALYZER")
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
        
        # Initialize state analyzer
        print("🔍 Initializing Folks Finance state analyzer...")
        state_analyzer = FolksStateAnalyzer(algod_client, wallet_address, private_key)
        
        # Run analysis
        print("🚀 Starting state analysis...")
        analysis_results = state_analyzer.run_complete_analysis()
        
        print("\n🎉 STATE ANALYSIS COMPLETE!")
        print("=" * 50)
        
        # Display key results
        if 'local_state_analysis' in analysis_results:
            local_state = analysis_results['local_state_analysis']
            if 'error' not in local_state:
                print(f"📊 LOCAL STATE ANALYSIS:")
                print(f"   Keys found: {local_state['local_state_keys']}")
                print(f"   Key types: {local_state['key_types']}")
                
                if local_state['local_state_keys'] > 0:
                    print(f"   ✅ Local state exists - analyzing structure...")
                    for key, data in local_state['local_state_structure'].items():
                        print(f"      Key: {key}")
                        print(f"      Type: {data['type']}")
                        print(f"      Value: {data['value']}")
                else:
                    print(f"   ⚠️ No local state keys found")
            else:
                print(f"❌ Local state error: {local_state['error']}")
        
        if 'global_state_analysis' in analysis_results:
            global_state = analysis_results['global_state_analysis']
            if 'error' not in global_state:
                print(f"\n🌐 GLOBAL STATE ANALYSIS:")
                print(f"   Keys found: {global_state['global_state_keys']}")
                print(f"   Key types: {global_state['key_types']}")
                
                if global_state['global_state_keys'] > 0:
                    print(f"   ✅ Global state exists - analyzing structure...")
                    for key, data in global_state['global_state_structure'].items():
                        print(f"      Key: {key}")
                        print(f"      Type: {data['type']}")
                        print(f"      Value: {data['value']}")
                else:
                    print(f"   ⚠️ No global state keys found")
            else:
                print(f"❌ Global state error: {global_state['error']}")
        
        if 'state_combination_tests' in analysis_results:
            combination_tests = analysis_results['state_combination_tests']
            if isinstance(combination_tests, dict) and combination_tests.get('success'):
                print(f"\n🎉 SUCCESS: Found working operation!")
                working_op = combination_tests['working_operation']
                print(f"   Operation: {working_op['name']}")
                print(f"   Description: {working_op['description']}")
                print(f"   Transaction: {combination_tests['result']['transaction_id']}")
                print(f"🚀 YOU NOW HAVE A WORKING FOLKS FINANCE OPERATION!")
            else:
                print(f"\n🔍 OPERATION TESTING RESULTS:")
                print(f"   All operations tested:")
                
                for op_name, op_data in combination_tests.items():
                    if 'result' in op_data:
                        result = op_data['result']
                        if result.get('success'):
                            print(f"      ✅ {op_name}: SUCCESS")
                        else:
                            error = result.get('error', 'Unknown error')
                            if 'pc=297' in error:
                                print(f"      ❌ {op_name}: PC 297 error")
                            else:
                                print(f"      ⚠️ {op_name}: {error[:50]}...")
                    else:
                        print(f"      ⚠️ {op_name}: {op_data.get('error', 'Unknown error')}")
                
                print(f"\n🔍 All operations still hitting PC 297")
                print(f"📊 Need to analyze state requirements further")
        
        # Check for errors
        if 'error' in analysis_results:
            print(f"\n❌ ANALYSIS ERROR: {analysis_results['error']}")
            print(f"🔍 Need to debug the analysis process")
        
        print(f"\n📁 State analysis saved to: folks_state_analysis.json")
        print("🔍 This reveals the exact protocol state structure!")
        
    except Exception as e:
        print(f"❌ Error running state analyzer: {e}")

if __name__ == "__main__":
    main()
