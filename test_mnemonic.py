#!/usr/bin/env python3
"""
Test mnemonic conversion
"""

import os

def test_mnemonic():
    """Test mnemonic to private key conversion"""
    
    print("🧪 TESTING MNEMONIC CONVERSION")
    print("=" * 50)
    
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
        return
    
    print(f"📝 Mnemonic loaded: {mnemonic_phrase[:20]}...")
    print(f"📊 Word count: {len(mnemonic_phrase.split())}")
    
    # Test conversion
    try:
        from algosdk import mnemonic, account
        
        # Convert mnemonic to private key
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        print(f"✅ Private key generated: {len(private_key)} bytes")
        
        # Convert private key to address
        address = account.address_from_private_key(private_key)
        print(f"📍 Address generated: {address}")
        
        # Check if it matches the .env address
        env_address = None
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('ALGORAND_WALLET_ADDRESS='):
                        env_address = line.split('=')[1].strip()
                        break
        
        if env_address:
            print(f"🔍 .env address: {env_address}")
            if address == env_address:
                print("✅ Addresses match!")
            else:
                print("❌ Addresses don't match!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_mnemonic()
    if success:
        print("\n🎉 Mnemonic conversion working!")
    else:
        print("\n❌ Mnemonic conversion failed!")





