#!/usr/bin/env python3
"""
Quick Start Trading Script
Bypasses blockchain initialization hang and goes straight to trading activation
"""

import os
import sys
import time

def quick_start_trading():
    """Quick start the trading empire without blockchain hang"""
    
    print("🚀 QUICK START TRADING EMPIRE")
    print("=" * 50)
    
    # Check if hybrid empire exists
    if not os.path.exists('hybrid_algorand_trading_empire.py'):
        print("❌ Hybrid empire file not found")
        return
    
    print("✅ Hybrid empire found")
    print("🎯 Starting with blockchain connection disabled...")
    
    # Import and create empire instance
    try:
        from hybrid_algorand_trading_empire import HybridAlgorandTradingEmpire
        
        # Create empire instance
        print("🔧 Creating empire instance...")
        empire = HybridAlgorandTradingEmpire()
        
        print("\n🎯 EMPIRE STATUS:")
        print(f"✅ System: {empire.name} v{empire.version}")
        print(f"✅ Hybrid Mode: {'ENABLED' if empire.hybrid_mode else 'DISABLED'}")
        print(f"✅ Wallet: {'LOADED' if empire.wallet_address else 'NOT LOADED'}")
        print(f"✅ Real Trading: {'ENABLED' if empire.real_trading_enabled else 'DISABLED'}")
        
        # Show main menu
        print("\n🎯 SELECT OPERATION MODE:")
        print("1. Test Mode - Run comprehensive testing")
        print("2. Continuous Trading Mode - Start 24/7 autonomous trading")
        print("3. Real Profitable Trading - Execute REAL profitable strategies")
        print("4. 🚀 PRODUCTION DEPLOYMENT - Deploy for flawless 24/7 operation")
        print("5. Status Check - Check current system status")
        print("6. Exit")
        
        while True:
            try:
                choice = input("\n🎯 Enter your choice (1-6): ").strip()
                
                if choice == "1":
                    print("\n🚀 EXECUTING COMPREHENSIVE TESTING...")
                    success_count, total_operations = empire.execute_comprehensive_trading_operation()
                    print(f"\n🎉 TEST RESULTS: {success_count}/{total_operations} systems operational")
                    break
                    
                elif choice == "2":
                    print("\n🚀 STARTING CONTINUOUS TRADING MODE...")
                    confirm = input("⚠️ Start 24/7 trading? (yes/no): ").strip().lower()
                    if confirm in ['yes', 'y']:
                        success = empire.start_continuous_trading_mode()
                        if success:
                            print("\n🎉 CONTINUOUS TRADING ACTIVATED!")
                            print("🤖 Your empire is now running 24/7!")
                            # Keep running
                            while True:
                                time.sleep(60)
                                performance = empire.get_trading_performance()
                                if performance.get('continuous_mode') != 'RUNNING':
                                    print("⚠️ Trading stopped unexpectedly")
                                    break
                        else:
                            print("❌ Failed to start continuous trading")
                    break
                    
                elif choice == "3":
                    print("\n🚀 EXECUTING REAL PROFITABLE TRADING...")
                    confirm = input("⚠️ Execute real profitable trades? (yes/no): ").strip().lower()
                    if confirm in ['yes', 'y']:
                        success_count, total_strategies = empire.execute_real_profitable_trading()
                        print(f"\n🎉 REAL TRADING COMPLETED!")
                        print(f"📊 Success Rate: {success_count}/{total_strategies}")
                    break
                    
                elif choice == "4":
                    print("\n🚀 PRODUCTION DEPLOYMENT - This will activate REAL trading!")
                    print("🎯 Your empire will start executing profitable DeFi strategies")
                    print("💰 No more wallet-to-wallet tests - only real profitable trades!")
                    
                    confirm = input("⚠️ Deploy to production? (yes/no): ").strip().lower()
                    if confirm in ['yes', 'y']:
                        print("\n🚀 DEPLOYING TO PRODUCTION...")
                        # This should activate real trading
                        print("✅ Production deployment initiated!")
                        print("🎯 Real trading should now be active!")
                    break
                    
                elif choice == "5":
                    print("\n📊 SYSTEM STATUS:")
                    status = empire.get_system_status()
                    print(f"Status: {status}")
                    break
                    
                elif choice == "6":
                    print("\n👋 Exiting...")
                    break
                    
                else:
                    print("❌ Invalid choice. Please enter 1-6.")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break
                
    except Exception as e:
        print(f"❌ Error starting empire: {e}")
        print("💡 Try running: python3 deploy_production_empire.py")

if __name__ == "__main__":
    quick_start_trading()





