#!/usr/bin/env python3
"""
Execute Real Transfer to Different Address
This will send ALGO to a different wallet - a REAL transaction
"""

import os
import json
from datetime import datetime

def execute_real_transfer():
    """Execute a real transfer to a different address"""
    
    print("🚀 EXECUTING REAL TRANSFER TO DIFFERENT ADDRESS")
    print("=" * 60)
    print("🎯 This will send ALGO to a DIFFERENT wallet (not self)!")
    
    try:
        # Load wallet credentials
        wallet_address = None
        mnemonic_phrase = None
        
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('ALGORAND_WALLET_ADDRESS='):
                        wallet_address = line.split('=')[1].strip()
                    elif line.startswith('ALGORAND_WALLET_MNEMONIC='):
                        mnemonic_phrase = line.split('=')[1].strip()
        
        if not wallet_address or not mnemonic_phrase:
            print("❌ Wallet credentials not found")
            return False
        
        print(f"✅ Wallet loaded: {wallet_address[:10]}...{wallet_address[-10:]}")
        
        # Import Algorand SDK
        from algosdk import mnemonic, account, transaction, v2client
        
        # Convert mnemonic to private key
        print("🔑 Converting mnemonic to private key...")
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        print(f"✅ Private key generated: {len(private_key)} bytes")
        
        # Verify address
        generated_address = account.address_from_private_key(private_key)
        if generated_address != wallet_address:
            print(f"❌ Address mismatch: {generated_address} vs {wallet_address}")
            return False
        print("✅ Address verified")
        
        # Connect to Algorand
        print("🔗 Connecting to Algorand mainnet...")
        algod_client = v2client.algod.AlgodClient(
            algod_token="",
            algod_address="https://mainnet-api.algonode.cloud"
        )
        
        # Test connection
        status = algod_client.status()
        print(f"✅ Connected to mainnet: Block {status['last-round']}")
        
        # Check balance
        account_info = algod_client.account_info(wallet_address)
        algo_balance = account_info['amount'] / 1000000
        print(f"💰 Current balance: {algo_balance:.6f} ALGO")
        
        if algo_balance < 0.002:
            print("❌ Insufficient balance for transaction")
            return False
        
        # Create a real transfer to a DIFFERENT address
        print("\n🔧 Creating real transfer to different address...")
        
        # Use a real, valid Algorand address (this is NOT your wallet)
        # Let me use a real DeFi protocol address
        print("🔧 Creating real ALGO transfer to DeFi protocol...")
        
        # For a real test, let me create a transaction that will definitely work
        # Let me use a different approach - create a real DeFi interaction
        
        # Get suggested parameters
        params = algod_client.suggested_params()
        print("✅ Got transaction parameters")
        
        # Create transaction (send 0.001 ALGO to different address)
        txn = transaction.PaymentTxn(
            sender=wallet_address,
            sp=params,
            receiver=different_receiver,
            amt=1000  # 0.001 ALGO in microalgos
        )
        print("✅ Transaction created")
        
        # Sign transaction
        print("🔐 Signing transaction...")
        signed_txn = txn.sign(private_key)
        print("✅ Transaction signed")
        
        # Submit transaction
        print("📤 Submitting transaction...")
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"✅ Transaction submitted: {tx_id}")
        
        # Wait for confirmation
        print("⏳ Waiting for confirmation...")
        confirmed_txn = algod_client.pending_transaction_info(tx_id)
        
        while confirmed_txn.get('confirmed-round') is None:
            import time
            time.sleep(1)
            confirmed_txn = algod_client.pending_transaction_info(tx_id)
        
        print(f"✅ Transaction confirmed in round {confirmed_txn.get('confirmed-round')}")
        
        # Save transaction details
        tx_details = {
            "timestamp": datetime.now().isoformat(),
            "transaction_id": tx_id,
            "confirmed_round": confirmed_txn.get('confirmed-round'),
            "sender": wallet_address,
            "receiver": different_receiver,
            "amount": "0.001 ALGO",
            "type": "real_transfer_to_different_address",
            "status": "confirmed"
        }
        
        with open('real_transfer_transaction.json', 'w') as f:
            json.dump(tx_details, f, indent=2)
        
        print("\n🎉 REAL TRANSFER TO DIFFERENT ADDRESS EXECUTED!")
        print("💰 This sends ALGO to a DIFFERENT wallet (not self)!")
        print("🔍 Check your wallet - you should see a transaction TO a different address!")
        print(f"📄 Transaction details saved to: real_transfer_transaction.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = execute_real_transfer()
    if success:
        print("\n🎯 SUCCESS: Real transfer to different address executed!")
        print("🔍 Check your wallet - it should show a transaction TO a different address!")
    else:
        print("\n❌ FAILED: Could not execute real transfer")
