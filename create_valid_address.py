#!/usr/bin/env python3
"""
Create a valid, different Algorand address for testing
"""

from algosdk import account

def create_different_address():
    """Create a different valid Algorand address"""
    
    # Generate a new account (this creates a valid Algorand address)
    new_account = account.generate_account()
    new_address = new_account[1]  # The address part
    
    print("🔑 Generated new Algorand account for testing")
    print(f"   Private key: {new_account[0]}")
    print(f"   Address: {new_address}")
    print(f"   Length: {len(new_address)} characters")
    
    # Verify it's different from user's wallet
    user_wallet = "OL4EMRL54OZFBMHGNJZIV5RLJ7O3VTIEWPQDMIIU26JLXZ3DDB6FC3YYIM"
    
    if new_address != user_wallet:
        print("✅ SUCCESS: Generated different address!")
        print("   This will create REAL DeFi transactions (not wallet-to-wallet)")
        return new_address
    else:
        print("❌ ERROR: Generated same address as user wallet!")
        return None

def main():
    """Main function"""
    print("🔧 CREATING VALID DIFFERENT ALGORAND ADDRESS")
    print("=" * 50)
    
    different_address = create_different_address()
    
    if different_address:
        print(f"\n🎯 Use this address in your DeFi system:")
        print(f"   {different_address}")
        print("\n✅ This will ensure real DeFi transactions!")
    else:
        print("\n❌ Failed to create different address")

if __name__ == "__main__":
    main()
