#!/usr/bin/env python3
"""
Test private key format for Algorand SDK
"""

import os
import base64
from algosdk import mnemonic, account

def test_private_key_formats():
    """Test different private key formats"""
    print("🧪 TESTING PRIVATE KEY FORMATS")
    print("=" * 50)
    
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
        return
    
    print(f"💰 Wallet: {wallet_address[:10]}...{wallet_address[-10:]}")
    print(f"🔑 Mnemonic: {mnemonic_phrase[:20]}...{mnemonic_phrase[-20:]}")
    
    # Test 1: Convert mnemonic to private key
    print("\n🔍 Test 1: Mnemonic to Private Key")
    try:
        private_key_result = mnemonic.to_private_key(mnemonic_phrase)
        print(f"✅ Private key result: {type(private_key_result)} - {len(str(private_key_result))} characters")
        print(f"   Value: {str(private_key_result)[:20]}...{str(private_key_result)[-20:]}")
        
        # Check if it's bytes or string
        if isinstance(private_key_result, bytes):
            print(f"   Type: bytes - {len(private_key_result)} bytes")
            print(f"   First 8 bytes: {private_key_result[:8].hex()}")
            print(f"   Last 8 bytes: {private_key_result[-8:].hex()}")
        else:
            print(f"   Type: string - {len(str(private_key_result))} characters")
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        return
    
    # Test 2: Handle private key format
    print("\n🔍 Test 2: Private Key Format Analysis")
    try:
        if isinstance(private_key_result, bytes):
            # Convert bytes to base64 string
            base64_string = base64.b64encode(private_key_result).decode('utf-8')
            print(f"✅ Converted to base64: {len(base64_string)} characters")
            print(f"   Base64: {base64_string}")
        else:
            # It's already a string
            base64_string = str(private_key_result)
            print(f"✅ Using string as-is: {len(base64_string)} characters")
            print(f"   String: {base64_string}")
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        return
    
    # Test 3: Test transaction signing
    print("\n🔍 Test 3: Transaction Signing Test")
    try:
        from algosdk.transaction import PaymentTxn
        from algosdk.v2client import algod
        
        # Create algod client
        algod_client = algod.AlgodClient("", "https://mainnet-api.algonode.cloud")
        params = algod_client.suggested_params()
        
        # Create test transaction
        txn = PaymentTxn(
            sender=wallet_address,
            sp=params,
            receiver=wallet_address,  # Send to self for testing
            amt=1000,  # 0.001 ALGO
            note=b"Test transaction"
        )
        
        # Try signing with the private key
        print("   Testing with private key...")
        if isinstance(private_key_result, bytes):
            signed_txn = txn.sign(private_key_result)
            print("   ✅ Signing with bytes: SUCCESS")
        else:
            signed_txn = txn.sign(str(private_key_result))
            print("   ✅ Signing with string: SUCCESS")
        
        print("✅ All signing tests passed!")
        
    except Exception as e:
        print(f"❌ Signing test failed: {e}")
        return
    
    print("\n🎉 PRIVATE KEY FORMAT TEST COMPLETED SUCCESSFULLY!")
    print("✅ Your private key is working correctly!")
    print(f"✅ Use format: {type(private_key_result)} (string) - {len(str(private_key_result))} characters")

if __name__ == "__main__":
    test_private_key_formats()
