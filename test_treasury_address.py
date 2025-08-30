#!/usr/bin/env python3
"""
Test Treasury Wallet Address
"""

from algosdk import encoding

def test_treasury_address():
    """Test if the treasury wallet address is valid"""
    
    addr = "5LEDUTOGIWSMD2MZW4FIYJ2W3KZU262H2K3F7R2BBQNMHUYNDFHEA77UJQ"
    
    print(f"Testing treasury wallet address: {addr}")
    print(f"Length: {len(addr)}")
    print(f"Valid length: {len(addr) == 58}")
    
    try:
        encoding.decode_address(addr)
        print("✅ Valid address - ready to receive transactions!")
        return True
    except Exception as e:
        print(f"❌ Invalid: {e}")
        return False

if __name__ == "__main__":
    test_treasury_address()


