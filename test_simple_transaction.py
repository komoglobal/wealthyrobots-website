#!/usr/bin/env python3
"""
Test Simple Transaction
"""

import os

def test_simple_transaction():
    """Test simple transaction creation and signing"""
    
    print("🧪 TESTING SIMPLE TRANSACTION")
    print("=" * 50)
    
    try:
        # Load mnemonic from .env
        mnemonic_phrase = None
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('ALGORAND_WALLET_MNEMONIC='):
                        mnemonic_phrase = line.split('=')[1].strip()
                        break
        
        if not mnemonic_phrase:
            print("❌ No mnemonic found in .env")
            return False
        
        print(f"📝 Mnemonic loaded: {mnemonic_phrase[:20]}...")
        
        # Test conversion
        from algosdk import mnemonic, account, transaction, v2client
        
        # Convert mnemonic to private key
        private_key_bytes = mnemonic.to_private_key(mnemonic_phrase)
        print(f"✅ Private key generated: {len(private_key_bytes)} bytes")
        
        # Convert private key to address
        address = account.address_from_private_key(private_key_bytes)
        print(f"📍 Address generated: {address}")
        
        # Test transaction creation
        print("\n🔧 Testing transaction creation...")
        
        # Create a simple test transaction
        test_receiver = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ"
        
        # Get suggested parameters (this might fail if no connection)
        try:
            algod_client = v2client.algod.AlgodClient(
                algod_token="",
                algod_address="https://mainnet-api.algonode.cloud"
            )
            
            params = algod_client.suggested_params()
            print("✅ Got suggested parameters")
            
            # Create transaction
            txn = transaction.PaymentTxn(
                sender=address,
                sp=params,
                receiver=test_receiver,
                amt=1000  # 0.001 ALGO
            )
            print("✅ Transaction created successfully")
            
            # Sign transaction
            print("🔐 Signing transaction...")
            signed_txn = txn.sign(private_key_bytes)
            print("✅ Transaction signed successfully")
            
            return True
            
        except Exception as e:
            print(f"❌ Transaction test failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_transaction()
    if success:
        print("\n🎉 Simple transaction test passed!")
    else:
        print("\n❌ Simple transaction test failed!")





