#!/usr/bin/env python3
"""
Algorand DeFi Trading Setup Script
Quick setup and configuration for real Algorand DeFi trading
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("🟢" + "="*60 + "🟢")
    print("🚀 ALGORAND DEFI TRADING SETUP")
    print("🎯 Real Trading with Real Money on Algorand")
    print("🟢" + "="*60 + "🟢")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing Algorand DeFi dependencies...")
    
    try:
        # Install core dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install from requirements file
        if Path("requirements_algorand_defi.txt").exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements_algorand_defi.txt"
            ], check=True)
            print("✅ Dependencies installed successfully")
        else:
            print("⚠️ requirements_algorand_defi.txt not found, installing core packages...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "py-algorand-sdk", "aiohttp", "python-dotenv"
            ], check=True)
            print("✅ Core dependencies installed")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    return True

def create_env_file():
    """Create .env file from template"""
    print("\n🔧 Setting up environment configuration...")
    
    if Path(".env").exists():
        print("⚠️ .env file already exists")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return True
    
    if Path(".env.template").exists():
        # Copy template to .env
        with open(".env.template", "r") as f:
            template = f.read()
        
        with open(".env", "w") as f:
            f.write(template)
        
        print("✅ Created .env file from template")
        print("📝 Edit .env file with your wallet details")
        return True
    else:
        print("❌ .env.template not found")
        return False

def setup_wallet():
    """Guide user through wallet setup"""
    print("\n💼 WALLET SETUP")
    print("=" * 40)
    print("To trade with real money, you need an Algorand wallet.")
    print()
    print("🔑 OPTIONS:")
    print("1. Use existing wallet (recommended)")
    print("2. Create new wallet")
    print("3. Use testnet for practice")
    print()
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        print("\n📝 EXISTING WALLET SETUP:")
        print("You'll need either:")
        print("   • 25-word mnemonic phrase, OR")
        print("   • Wallet address")
        print()
        print("⚠️  IMPORTANT: Never share your mnemonic phrase!")
        print()
        
        mnemonic = input("Enter mnemonic phrase (or press Enter to skip): ").strip()
        if mnemonic:
            # Update .env file
            update_env_file("ALGORAND_WALLET_MNEMONIC", mnemonic)
            print("✅ Mnemonic configured in .env file")
        else:
            address = input("Enter wallet address: ").strip()
            if address:
                update_env_file("ALGORAND_WALLET_ADDRESS", address)
                print("✅ Wallet address configured in .env file")
            else:
                print("❌ No wallet information provided")
                return False
                
    elif choice == "2":
        print("\n🆕 NEW WALLET SETUP:")
        print("1. Download Pera Algo Wallet (mobile)")
        print("2. Create new wallet")
        print("3. Write down your 25-word mnemonic phrase")
        print("4. Add some ALGO to your wallet")
        print("5. Come back and enter your mnemonic")
        print()
        input("Press Enter when ready...")
        
        mnemonic = input("Enter your 25-word mnemonic phrase: ").strip()
        if mnemonic and len(mnemonic.split()) == 25:
            update_env_file("ALGORAND_WALLET_MNEMONIC", mnemonic)
            print("✅ New wallet configured!")
        else:
            print("❌ Invalid mnemonic phrase")
            return False
            
    elif choice == "3":
        print("\n🧪 TESTNET SETUP:")
        print("Using testnet for practice (no real money)")
        update_env_file("ALGORAND_NETWORK", "testnet")
        update_env_file("ALGOD_ADDRESS", "https://testnet-api.algonode.cloud")
        print("✅ Testnet configured")
        return True
        
    else:
        print("❌ Invalid choice")
        return False
    
    return True

def update_env_file(key, value):
    """Update .env file with key-value pair"""
    if not Path(".env").exists():
        return
    
    # Read current .env file
    with open(".env", "r") as f:
        lines = f.readlines()
    
    # Update or add key-value pair
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break
    
    if not updated:
        lines.append(f"{key}={value}\n")
    
    # Write back to .env file
    with open(".env", "w") as f:
        f.writelines(lines)

def test_connection():
    """Test Algorand connection"""
    print("\n🔌 Testing Algorand connection...")
    
    try:
        # Import and test Algorand SDK
        from algorand_defi_trading_agent import AlgorandDeFiTradingAgent
        
        # Create agent instance
        agent = AlgorandDeFiTradingAgent()
        
        if agent.connected:
            print("✅ Algorand connection successful!")
            return True
        else:
            print("❌ Algorand connection failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection test error: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n📋 NEXT STEPS:")
    print("=" * 40)
    print("1. ✅ Dependencies installed")
    print("2. ✅ Environment configured")
    print("3. ✅ Wallet setup complete")
    print()
    print("🚀 START TRADING:")
    print("   python3 algorand_defi_trading_agent.py")
    print()
    print("📊 MONITOR PERFORMANCE:")
    print("   python3 algorand_defi_config.py")
    print()
    print("⚠️  IMPORTANT REMINDERS:")
    print("   • Never share your private keys or mnemonic")
    print("   • Start with small amounts")
    print("   • Monitor your positions regularly")
    print("   • Keep your .env file secure")
    print()
    print("🟢 Happy trading on Algorand DeFi!")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        print("❌ Setup failed at environment configuration")
        sys.exit(1)
    
    # Setup wallet
    if not setup_wallet():
        print("❌ Setup failed at wallet configuration")
        sys.exit(1)
    
    # Test connection
    print("\n⏳ Waiting 3 seconds before testing connection...")
    time.sleep(3)
    
    if not test_connection():
        print("⚠️  Connection test failed, but setup may still work")
        print("   Check your .env file and try again")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)

















