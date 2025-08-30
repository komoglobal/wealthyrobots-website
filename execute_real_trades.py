#!/usr/bin/env python3
"""
Execute Real DeFi Trades
Bypasses all simulation code and executes real DeFi transactions
"""

import os
import json
from datetime import datetime

def execute_real_defi_trades():
    """Execute REAL DeFi trades - no simulations, no wallet-to-wallet"""
    
    print("🚀 EXECUTING REAL DEFI TRADES")
    print("=" * 50)
    print("🎯 This will execute REAL trades (not wallet-to-wallet)!")
    
    try:
        # Import the multi-protocol trading system
        from multi_protocol_trading_system import MultiProtocolTradingSystem
        
        print("✅ Multi-protocol system imported successfully")
        
        # Initialize blockchain connection
        from algosdk.v2client import algod
        from algosdk.v2client import indexer
        
        print("🔗 Connecting to Algorand mainnet...")
        algod_client = algod.AlgodClient(
            algod_token="",
            algod_address="https://mainnet-api.algonode.cloud"
        )
        
        # Test connection
        status = algod_client.status()
        print(f"✅ Connected to mainnet: Block {status['last-round']}")
        
        # Load wallet credentials
        wallet_address = None
        private_key = None
        
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('ALGORAND_WALLET_ADDRESS='):
                        wallet_address = line.split('=')[1].strip()
                    elif line.startswith('ALGORAND_WALLET_MNEMONIC='):
                        mnemonic_phrase = line.split('=')[1].strip()
                        try:
                            from algosdk import mnemonic
                            private_key = mnemonic.to_private_key(mnemonic_phrase)
                        except ImportError:
                            print("❌ algosdk not available")
                            return False
        
        if not wallet_address or not private_key:
            print("❌ Wallet credentials not found")
            return False
        
        print(f"✅ Wallet loaded: {wallet_address[:10]}...{wallet_address[-10:]}")
        
        # Check balances
        account_info = algod_client.account_info(wallet_address)
        algo_balance = account_info['amount'] / 1000000
        
        usdc_balance = 0
        for asset in account_info.get('assets', []):
            if asset['asset-id'] == 31566704:  # USDC
                usdc_balance = asset['amount'] / 1000000
                break
        
        print(f"\n💰 Current Balances:")
        print(f"   ALGO: {algo_balance:.6f} ALGO")
        print(f"   USDC: {usdc_balance:.6f} USDC")
        
        # Initialize multi-protocol trading system
        print("\n🔧 Initializing Multi-Protocol Trading System...")
        multi_protocol = MultiProtocolTradingSystem()
        
        # Set the blockchain client manually
        multi_protocol.algod_client = algod_client
        # The mnemonic is already loaded from .env in the __init__ method
        
        # Scan for opportunities
        print("\n🔍 Scanning for real DeFi opportunities...")
        all_opportunities = multi_protocol.scan_all_opportunities()
        
        # Flatten opportunities from all protocols
        flat_opportunities = []
        for protocol, opps in all_opportunities.items():
            for opp in opps:
                opp['protocol'] = protocol  # Add protocol name to each opportunity
                flat_opportunities.append(opp)
        
        if not flat_opportunities:
            print("⚠️ No trading opportunities found")
            return False
        
        print(f"🎯 Found {len(flat_opportunities)} opportunities:")
        for opp in flat_opportunities:
            print(f"   • {opp['protocol'].upper()}: {opp.get('type', 'Unknown')} - APY: {opp.get('estimated_apy', 0)}%")
        
        # Execute the best opportunity
        best_opportunity = max(flat_opportunities, key=lambda x: x.get('estimated_apy', 0))
        print(f"\n🚀 Executing best opportunity: {best_opportunity['protocol'].upper()}")
        
        # Calculate trade amount (use 2% of available ALGO)
        trade_amount = min(algo_balance * 0.02, 0.5)  # 2% or max 0.5 ALGO
        print(f"💰 Trade amount: {trade_amount:.6f} ALGO")
        
        # Execute the trade
        print("\n🔄 Executing real DeFi trade...")
        success = multi_protocol.execute_real_trade(best_opportunity, trade_amount)
        
        if success:
            print("\n🎉 REAL DEFI TRADE EXECUTED SUCCESSFULLY!")
            print("💰 This should appear in your wallet as a REAL DeFi transaction")
            print("🔍 It should NOT be wallet-to-wallet!")
            print("📊 Check your wallet now for the new transaction")
            return True
        else:
            print("\n❌ Trade execution failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure multi_protocol_trading_system.py exists")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = execute_real_defi_trades()
    if success:
        print("\n🎯 SUCCESS: Real DeFi trade executed!")
        print("🔍 Check your wallet - it should show a real transaction!")
    else:
        print("\n❌ FAILED: Could not execute real DeFi trade")
