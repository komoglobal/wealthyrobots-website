#!/usr/bin/env python3
"""
FIXED ALGO TRANSFER - Proper receiver address handling
"""

import os
import json
from datetime import datetime
from algosdk import mnemonic, account, transaction, v2client, encoding
import time

def load_wallet_credentials():
    """Load real wallet credentials from .env file"""
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
        raise ValueError("❌ Wallet credentials not found in .env file")
    
    return wallet_address, mnemonic_phrase

def verify_wallet(wallet_address, mnemonic_phrase):
    """Verify wallet credentials are valid"""
    try:
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        generated_address = account.address_from_private_key(private_key)
        
        if generated_address != wallet_address:
            raise ValueError(f"❌ Address mismatch: {generated_address} vs {wallet_address}")
        
        print(f"✅ Wallet verified: {wallet_address[:10]}...{wallet_address[-10:]}")
        return private_key
    except Exception as e:
        raise ValueError(f"❌ Invalid wallet credentials: {e}")

def connect_to_algorand():
    """Connect to Algorand mainnet"""
    try:
        algod_client = v2client.algod.AlgodClient(
            algod_token="",
            algod_address="https://mainnet-api.algonode.cloud"
        )
        
        # Test connection
        status = algod_client.status()
        print(f"✅ Connected to Algorand mainnet: Block {status['last-round']}")
        return algod_client
    except Exception as e:
        raise ConnectionError(f"❌ Failed to connect to Algorand: {e}")

def check_balance(algod_client, wallet_address):
    """Check current ALGO balance"""
    try:
        account_info = algod_client.account_info(wallet_address)
        algo_balance = account_info['amount'] / 1000000  # Convert microalgos to ALGO
        print(f"💰 Current balance: {algo_balance:.6f} ALGO")
        return algo_balance
    except Exception as e:
        raise RuntimeError(f"❌ Failed to get balance: {e}")

def get_valid_receiver_address(sender_address):
    """Get a valid, different Algorand address to send to"""
    
    # Use the real treasury wallet address provided by the user
    # This is a real, valid Algorand mainnet address that can receive transactions
    receiver_address = "5LEDUTOGIWSMD2MZW4FIYJ2W3KZU262H2K3F7R2BBQNMHUYNDFHEA77UJQ"
    
    print(f"🎯 Using treasury wallet address: {receiver_address}")
    print(f"📏 Address length: {len(receiver_address)} characters")
    
    # Verify the address is valid and different
    if len(receiver_address) != 58:
        raise ValueError(f"❌ Address wrong length: {len(receiver_address)}")
    
    if receiver_address == sender_address:
        raise ValueError("❌ Receiver address cannot be the same as sender")
    
    try:
        # Validate the address format
        encoding.decode_address(receiver_address)
        print(f"✅ Address validation passed")
    except Exception as e:
        raise ValueError(f"❌ Invalid address format: {e}")
    
    print(f"⚠️  Note: This is a real treasury wallet - ALGO sent here will be received")
    print(f"📝 Receiver address: {receiver_address}")
    
    return receiver_address

def execute_real_transfer(algod_client, wallet_address, private_key, receiver_address, amount_algo):
    """Execute REAL ALGO transfer to different address"""
    try:
        print(f"\n🚀 EXECUTING REAL TRANSFER")
        print(f"📤 From: {wallet_address[:10]}...{wallet_address[-10:]}")
        print(f"📥 To: {receiver_address[:10]}...{receiver_address[-10:]}")
        print(f"💰 Amount: {amount_algo} ALGO")
        print("=" * 60)
        
        # Validate receiver address one more time
        if len(receiver_address) != 58:
            raise ValueError(f"❌ Receiver address wrong length: {len(receiver_address)}")
        
        try:
            encoding.decode_address(receiver_address)
        except Exception as e:
            raise ValueError(f"❌ Invalid receiver address: {e}")
        
        # Get suggested parameters
        params = algod_client.suggested_params()
        print("✅ Got transaction parameters")
        
        # Convert ALGO to microalgos
        amount_microalgos = int(amount_algo * 1000000)
        
        # Create REAL transaction
        txn = transaction.PaymentTxn(
            sender=wallet_address,
            sp=params,
            receiver=receiver_address,
            amt=amount_microalgos
        )
        print("✅ Transaction created")
        
        # Sign transaction
        print("🔐 Signing transaction...")
        signed_txn = txn.sign(private_key)
        print("✅ Transaction signed")
        
        # Submit transaction
        print("📡 Submitting transaction to Algorand network...")
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"✅ Transaction submitted! TX ID: {tx_id}")
        
        # Wait for confirmation
        print("⏳ Waiting for transaction confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
        
        if confirmed_txn:
            print("🎉 TRANSACTION CONFIRMED ON BLOCKCHAIN!")
            print(f"📊 Block: {confirmed_txn['confirmed-round']}")
            
            # Handle fee calculation safely
            try:
                fee = confirmed_txn.get('fee', 0) / 1000000
                print(f"💰 Fee: {fee:.6f} ALGO")
            except (KeyError, TypeError):
                print("💰 Fee: Information not available")
            
            print(f"🔗 View on AlgoExplorer: https://algoexplorer.io/tx/{tx_id}")
            
            # Save transaction details
            tx_details = {
                'tx_id': tx_id,
                'timestamp': datetime.now().isoformat(),
                'sender': wallet_address,
                'receiver': receiver_address,
                'amount_algo': amount_algo,
                'amount_microalgos': amount_microalgos,
                'fee': confirmed_txn.get('fee', 0) / 1000000,
                'block': confirmed_txn['confirmed-round'],
                'status': 'confirmed'
            }
            
            with open('real_transaction_log.json', 'w') as f:
                json.dump(tx_details, f, indent=2)
            
            print("✅ Transaction details saved to real_transaction_log.json")
            return True
            
    except Exception as e:
        print(f"❌ Transfer failed: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main execution function"""
    print("🚀 FIXED ALGO TRANSFER SYSTEM")
    print("=" * 60)
    print("🎯 This will ACTUALLY send ALGO to a DIFFERENT address!")
    print("⚠️  This is NOT a simulation - REAL blockchain transaction")
    print("=" * 60)
    
    try:
        # Load wallet credentials
        print("🔑 Loading wallet credentials...")
        wallet_address, mnemonic_phrase = load_wallet_credentials()
        
        # Verify wallet
        print("✅ Verifying wallet...")
        private_key = verify_wallet(wallet_address, mnemonic_phrase)
        
        # Connect to Algorand
        print("🔗 Connecting to Algorand mainnet...")
        algod_client = connect_to_algorand()
        
        # Check balance
        print("💰 Checking balance...")
        balance = check_balance(algod_client, wallet_address)
        
        if balance < 0.002:
            print("❌ Insufficient balance for transaction (need at least 0.002 ALGO)")
            return False
        
        # Get receiver address (different from your wallet)
        print("🎯 Generating valid receiver address...")
        receiver_address = get_valid_receiver_address(wallet_address)
        
        # Calculate transfer amount (small amount for testing)
        transfer_amount = min(0.001, balance - 0.001)  # Send 0.001 ALGO, keep 0.001 for fees
        
        print(f"\n📋 TRANSACTION SUMMARY:")
        print(f"   From: {wallet_address}")
        print(f"   To: {receiver_address}")
        print(f"   Amount: {transfer_amount} ALGO")
        print(f"   Network: Algorand Mainnet")
        print(f"   Type: Real Payment Transaction")
        
        # Confirm execution
        print("\n⚠️  WARNING: This will execute a REAL transaction!")
        print("   The ALGO will be sent to the treasury wallet and CANNOT be recovered!")
        print("   This is for testing purposes only!")
        
        # For safety, require confirmation
        confirm = input("\n🔐 Type 'EXECUTE' to confirm real transaction: ")
        
        if confirm != 'EXECUTE':
            print("❌ Transaction cancelled by user")
            return False
        
        # Execute the REAL transfer
        success = execute_real_transfer(
            algod_client, 
            wallet_address, 
            private_key, 
            receiver_address, 
            transfer_amount
        )
        
        if success:
            print("\n🎉 SUCCESS: Real ALGO transfer completed!")
            print("✅ ALGO has been sent to a different address on the blockchain")
            print("🔗 Check the transaction on AlgoExplorer for verification")
        else:
            print("\n❌ FAILED: Transfer did not complete")
            
        return success
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return False

if __name__ == "__main__":
    main()
