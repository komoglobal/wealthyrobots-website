#!/usr/bin/env python3
"""
Fund and Test Wallet - WealthyRobot
Funds the wallet with test ALGO and executes a real transaction
"""

import os
import json
import time
from datetime import datetime
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn
import requests

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

def fund_wallet_with_testnet_algo(wallet_address):
    """Fund wallet using Algorand testnet faucet"""
    print("💰 Funding wallet with testnet ALGO...")
    
    # Algorand testnet faucet URL
    faucet_url = "https://bank.testnet.algorand.network/v1/faucet"
    
    try:
        # Request funding from faucet
        response = requests.post(faucet_url, json={"address": wallet_address})
        
        if response.status_code == 200:
            print("✅ Faucet funding request successful!")
            print("⏳ Waiting for funds to arrive...")
            
            # Wait a bit for the transaction to be processed
            time.sleep(10)
            return True
        else:
            print(f"❌ Faucet funding failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error funding wallet: {e}")
        return False

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

def wait_for_confirmation(client, tx_id, timeout=60):
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
                time.sleep(3)
            except Exception:
                time.sleep(3)
        
        print("⚠️ Transaction confirmation timeout")
        return False
        
    except Exception as e:
        print(f"❌ Error waiting for confirmation: {e}")
        return False

def execute_fund_and_test():
    """Fund wallet and execute real test transaction"""
    print("🚀 WEALTHYROBOT FUND AND TEST WALLET")
    print("=" * 60)
    print("This will:")
    print("1. Fund your wallet with testnet ALGO")
    print("2. Execute a REAL transaction on Algorand")
    print("3. Show the transaction in your wallet")
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
    print("🔗 Connecting to Algorand testnet...")
    client = create_algod_client()
    if not client:
        return False
    
    print("✅ Connected to Algorand testnet")
    print()
    
    # Check initial balance
    print("📊 Checking initial balance...")
    account_info = get_account_info(client, wallet_address)
    if not account_info:
        return False
    
    initial_balance = account_info.get('amount', 0) / 1000000
    print(f"💰 Initial Balance: {initial_balance:.6f} ALGO")
    
    if initial_balance < 0.002:  # Need at least 0.002 ALGO for test + fees
        print("💸 Insufficient balance, funding wallet...")
        
        # Fund the wallet
        if not fund_wallet_with_testnet_algo(wallet_address):
            print("❌ Failed to fund wallet")
            return False
        
        # Wait and check new balance
        print("⏳ Waiting for funding to arrive...")
        time.sleep(15)
        
        # Check new balance
        account_info = get_account_info(client, wallet_address)
        if not account_info:
            return False
        
        new_balance = account_info.get('amount', 0) / 1000000
        print(f"💰 New Balance: {new_balance:.6f} ALGO")
        
        if new_balance < 0.002:
            print("❌ Still insufficient balance after funding")
            return False
    else:
        print("✅ Sufficient balance for test transaction")
    
    print()
    
    # Create private key from mnemonic
    try:
        private_key = mnemonic.to_private_key(wallet_mnemonic)
        print("🔑 Private key derived from mnemonic")
    except Exception as e:
        print(f"❌ Error deriving private key: {e}")
        return False
    
    # Create test transaction
    test_amount = 0.001
    print(f"🔄 Creating test transaction for {test_amount} ALGO...")
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
        print("Your wallet will now show this transaction!")
        print("The WealthyRobot system is verified to work with real Algorand transactions!")
        
        return True
    else:
        print("❌ Transaction confirmation failed")
        return False

if __name__ == "__main__":
    print("🧪 FUNDING WALLET AND EXECUTING REAL TEST TRANSACTION")
    print("This will create a real transaction on the Algorand testnet")
    print("Amount: 0.001 ALGO (self-to-self for safety)")
    print()
    
    success = execute_fund_and_test()
    
    if success:
        print("\n🎉 REAL TEST TRANSACTION SUCCESSFUL!")
        print("Check your wallet - you should see the transaction!")
    else:
        print("\n❌ REAL TEST TRANSACTION FAILED")
        print("Please check the error messages above")
