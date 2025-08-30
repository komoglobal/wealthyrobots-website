#!/usr/bin/env python3
"""
Test Address Generation
"""

from algosdk import account, encoding

def test_address_generation():
    """Test that we can generate valid Algorand addresses"""
    
    print("🧪 TESTING ADDRESS GENERATION")
    print("=" * 40)
    
    # Generate a fresh address
    _, test_address = account.generate_account()
    
    print(f"Generated address: {test_address}")
    print(f"Length: {len(test_address)}")
    print(f"Valid length: {len(test_address) == 58}")
    
    # Test encoding validation
    try:
        encoding.decode_address(test_address)
        print("✅ Address validation passed")
    except Exception as e:
        print(f"❌ Address validation failed: {e}")
    
    return test_address

if __name__ == "__main__":
    test_address_generation()
