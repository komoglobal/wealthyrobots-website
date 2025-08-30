#!/usr/bin/env python3
"""
Test Real Address
"""

from algosdk import encoding

def test_real_address():
    """Test if the real address is valid"""
    
    addr = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    
    print(f"Testing address: {addr}")
    print(f"Length: {len(addr)}")
    
    try:
        encoding.decode_address(addr)
        print("✅ Valid address")
        return True
    except Exception as e:
        print(f"❌ Invalid: {e}")
        return False

if __name__ == "__main__":
    test_real_address()
