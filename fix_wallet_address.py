#!/usr/bin/env python3
"""
Fix Wallet Address Script
Corrects the malformed wallet address in .env file
"""

import os

def fix_wallet_address():
    """Fix the wallet address in .env file"""
    
    # Read current .env file
    env_path = '.env'
    if not os.path.exists(env_path):
        print("❌ .env file not found")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Fix the wallet address (add missing "O")
    old_address = "OL4EMRL54OZFBMHGNJZIV5RLJ703VTIEWPQDMIIU26JLXZ3DDB6FC3YYIM"
    new_address = "OL4EMRL54OZFBMHGNJZIV5RLJ7O3VTIEWPQDMIIU26JLXZ3DDB6FC3YYIM"
    
    if old_address in content:
        content = content.replace(old_address, new_address)
        
        # Write back to .env
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("✅ Wallet address fixed!")
        print(f"   Old: {old_address}")
        print(f"   New: {new_address}")
        return True
    else:
        print("⚠️ Wallet address not found or already correct")
        return False

if __name__ == "__main__":
    fix_wallet_address()
