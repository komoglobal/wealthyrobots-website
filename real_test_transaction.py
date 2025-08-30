#!/usr/bin/env python3
"""
Real Test Transaction - WealthyRobot
Executes a real transaction on the Algorand blockchain to verify the system is working
"""

import os
import json
import time
from datetime import datetime
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn
from algosdk import encoding

def load_wallet_config():
    """Load wallet configuration from .env file"""
    wallet_address = None
    wallet_mnemonic = None
    
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('ALGORAND_WALLET_ADDRESS='):
                    wallet_address = line.split('=')[1].strip()
                elif line.startswith('ALGORAND_WALLET_MNEMONIC='):
                    wallet_mnemonic = line.split('=')[1].strip()
    
    return wallet_address, wallet_mnemonic

def create_algod_client():
    """Create Algorand client connection"""
    # Using AlgoExplorer testnet for safe testing
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = ""
    
    try:
        client = algod.AlgodClient(algod_token, algod_address)
        return client
    except Exception as e:
        print(f"❌ Error connecting to Algorand: {e}")
        return None

def get_account_info(client, address):
    """Get account information"""
    try:
        account_info = client.account_info(address)
        return account_info
    except Exception as e:
        print(f"❌ Error getting account info: {e}")
        return None

def create_test_transaction(client, sender_address, sender_private_key, amount=0.001):
    """Create a real test transaction (self-to-self for safety)"""
    try:
        # Get suggested parameters
        params = client.suggested_params()
        
        # Create a self-to-self transaction (safe for testing)
        txn = PaymentTxn(
            sender=sender_address,
            sp=params,
            receiver=sender_address,  # Self-to-self for safety
            amt=int(amount * 1000000)  # Convert to microAlgos
        )
        
        # Sign the transaction
        signed_txn = txn.sign(sender_private_key)
        
        return signed_txn
        
    except Exception as e:
        print(f"❌ Error creating transaction: {e}")
        return None

def submit_transaction(client, signed_txn):
    """Submit transaction to the network"""
    try:
        # Submit the transaction
        tx_id = client.send_transaction(signed_txn)
        print(f"✅ Transaction submitted successfully!")
        print(f"🔗 Transaction ID: {tx_id}")
        return tx_id
    except Exception as e:
        print(f"❌ Error submitting transaction: {e}")
        return None

def wait_for_confirmation(client, tx_id, timeout=30):
    """Wait for transaction confirmation"""
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Check transaction status
                tx_info = client.pending_transaction_info(tx_id)
                if tx_info.get('confirmed-round'):
                    print(f"✅ Transaction confirmed in round {tx_info['confirmed-round']}")
                    return True
                time.sleep(2)
            except Exception:
                time.sleep(2)
        
        print("⚠️ Transaction confirmation timeout")
        return False
        
    except Exception as e:
        print(f"❌ Error waiting for confirmation: {e}")
        return False

def execute_real_test_transaction():
    """Execute a real test transaction on Algorand"""
    print("🚀 WEALTHYROBOT REAL TEST TRANSACTION")
    print("=" * 60)
    print("This will execute a REAL transaction on the Algorand blockchain")
    print("Amount: 0.001 ALGO (self-to-self for safety)")
    print("Network: Algorand Testnet (safe for testing)")
    print()
    
    # Load wallet configuration
    wallet_address, wallet_mnemonic = load_wallet_config()
    
    if not wallet_address or not wallet_mnemonic:
        print("❌ Wallet configuration not found in .env file")
        print("Please ensure ALGORAND_WALLET_ADDRESS and ALGORAND_WALLET_MNEMONIC are set")
        return False
    
    print(f"💰 Wallet Address: {wallet_address}")
    print(f"🔑 Wallet Configured: ✅")
    print()
    
    # Create Algorand client
    print("🔗 Connecting to Algorand network...")
    client = create_algod_client()
    if not client:
        return False
    
    print("✅ Connected to Algorand testnet")
    print()
    
    # Get account info
    print("📊 Getting account information...")
    account_info = get_account_info(client, wallet_address)
    if not account_info:
        return False
    
    balance = account_info.get('amount', 0) / 1000000  # Convert from microAlgos
    print(f"💰 Current Balance: {balance:.6f} ALGO")
    print()
    
    # Check if we have enough balance for the test
    test_amount = 0.001
    if balance < test_amount + 0.001:  # Need extra for fees
        print(f"❌ Insufficient balance for test transaction")
        print(f"Required: {test_amount + 0.001:.6f} ALGO (including fees)")
        print(f"Available: {balance:.6f} ALGO")
        return False
    
    # Create private key from mnemonic
    try:
        private_key = mnemonic.to_private_key(wallet_mnemonic)
        print("🔑 Private key derived from mnemonic")
    except Exception as e:
        print(f"❌ Error deriving private key: {e}")
        return False
    
    # Create test transaction
    print("🔄 Creating test transaction...")
    signed_txn = create_test_transaction(client, wallet_address, private_key, test_amount)
    if not signed_txn:
        return False
    
    print("✅ Test transaction created")
    print()
    
    # Submit transaction
    print("📡 Submitting transaction to Algorand network...")
    tx_id = submit_transaction(client, signed_txn)
    if not tx_id:
        return False
    
    print()
    print("⏳ Waiting for transaction confirmation...")
    
    # Wait for confirmation
    if wait_for_confirmation(client, tx_id):
        print()
        print("🎯 REAL TEST TRANSACTION SUCCESSFUL!")
        print("=" * 50)
        print(f"Transaction ID: {tx_id}")
        print(f"Amount: {test_amount} ALGO")
        print(f"Type: Self-to-self payment")
        print(f"Network: Algorand Testnet")
        print(f"Status: Confirmed")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 50)
        
        # Save transaction details
        tx_details = {
            'tx_id': tx_id,
            'amount': test_amount,
            'type': 'self_to_self_payment',
            'network': 'algorand_testnet',
            'status': 'confirmed',
            'timestamp': datetime.now().isoformat(),
            'wallet_address': wallet_address,
            'description': 'Real test transaction on Algorand blockchain'
        }
        
        with open('real_transaction_executed.json', 'w') as f:
            json.dump(tx_details, f, indent=2)
        
        print("📁 Transaction details saved to: real_transaction_executed.json")
        print()
        print("🔍 You can verify this transaction on:")
        print(f"   https://testnet.algoexplorer.io/tx/{tx_id}")
        print()
        print("🏆 REAL BLOCKCHAIN TRANSACTION COMPLETED!")
        print("The WealthyRobot system is now verified to work with real Algorand transactions!")
        
        return True
    else:
        print("❌ Transaction confirmation failed")
        return False

if __name__ == "__main__":
    print("🧪 EXECUTING REAL BLOCKCHAIN TEST TRANSACTION")
    print("This will create a real transaction on the Algorand testnet")
    print("Amount: 0.001 ALGO (self-to-self for safety)")
    print()
    
    success = execute_real_test_transaction()
    
    if success:
        print("\n🎉 REAL TEST TRANSACTION SUCCESSFUL!")
        print("Your wallet will show this transaction!")
    else:
        print("\n❌ REAL TEST TRANSACTION FAILED")
        print("Please check the error messages above")
