#!/usr/bin/env python3
"""
🚀 COMPREHENSIVE EMPIRE DEPLOYMENT & TESTING SCRIPT
Hybrid Algorand Trading Empire - Full System Test

This script:
1. Deploys the trading empire in production mode
2. Runs comprehensive testing to ensure flawless operation
3. Monitors performance and provides real-time status
4. Handles any issues automatically with recovery systems
"""

import time
import sys
import os
import threading

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class EmpireDeploymentManager:
    """Manages the deployment and testing of the trading empire"""
    
    def __init__(self):
        self.empire = None
        self.deployment_active = False
        self.test_results = {}
        self.monitoring_active = False
        
    def initialize_empire(self):
        """Initialize the trading empire"""
        try:
            print("🔧 Initializing Hybrid Algorand Trading Empire...")
            from hybrid_algorand_trading_empire import HybridAlgorandTradingEmpire
            
            self.empire = HybridAlgorandTradingEmpire()
            print("✅ Trading Empire initialized successfully!")
            
            # Check system status
            print("\n📊 System Status Check:")
            print(f"✅ System: {self.empire.name} v{self.empire.version}")
            print(f"✅ Hybrid Mode: {'ENABLED' if self.empire.hybrid_mode else 'DISABLED'}")
            print(f"✅ Blockchain: {'CONNECTED' if self.empire.blockchain_connected else 'DISCONNECTED'}")
            print(f"✅ Real Trading: {'ENABLED' if self.empire.real_trading_enabled else 'DISABLED'}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing empire: {e}")
            return False
    
    def run_comprehensive_testing(self):
        """Run comprehensive testing to ensure flawless operation"""
        try:
            print("\n🧪 RUNNING COMPREHENSIVE SYSTEM TESTING")
            print("=" * 60)
            
            # Test 1: DeFi Protocol Testing
            print("\n🎯 Test 1: DeFi Protocol Testing")
            print("-" * 40)
            success_count, total_operations = self.empire.execute_comprehensive_trading_operation()
            self.test_results['defi_protocols'] = {
                'success_count': success_count,
                'total_operations': total_operations,
                'success_rate': success_count / total_operations if total_operations > 0 else 0
            }
            print(f"✅ DeFi Protocol Test: {success_count}/{total_operations} ({self.test_results['defi_protocols']['success_rate']*100:.1f}%)")
            
            # Test 2: Real Profitable Trading
            print("\n🎯 Test 2: Real Profitable Trading")
            print("-" * 40)
            success_count, total_strategies = self.empire.execute_real_profitable_trading()
            self.test_results['profitable_trading'] = {
                'success_count': success_count,
                'total_strategies': total_strategies,
                'success_rate': success_count / total_strategies if total_strategies > 0 else 0
            }
            print(f"✅ Profitable Trading Test: {success_count}/{total_strategies} ({self.test_results['profitable_trading']['success_rate']*100:.1f}%)")
            
            # Test 3: Bot Deployment
            print("\n🎯 Test 3: Trading Bot Deployment")
            print("-" * 40)
            bot_success, bot_total = self.empire.launch_autonomous_trading_bots()
            self.test_results['trading_bots'] = {
                'success_count': bot_success,
                'total_bots': bot_total,
                'success_rate': bot_success / bot_total if bot_total > 0 else 0
            }
            print(f"✅ Trading Bot Test: {bot_success}/{bot_total} ({self.test_results['trading_bots']['success_rate']*100:.1f}%)")
            
            # Test 4: Monitoring Systems
            print("\n🎯 Test 4: Monitoring Systems")
            print("-" * 40)
            monitoring_success = self.empire.start_real_time_monitoring()
            self.test_results['monitoring_systems'] = {
                'success': monitoring_success,
                'status': 'ACTIVE' if monitoring_success else 'FAILED'
            }
            print(f"✅ Monitoring Systems: {'ACTIVE' if monitoring_success else 'FAILED'}")
            
            # Calculate overall success rate
            total_tests = len(self.test_results)
            successful_tests = sum(1 for test in self.test_results.values() 
                                if 'success_rate' in test and test['success_rate'] >= 0.8 
                                or 'success' in test and test['success'])
            
            self.test_results['overall'] = {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'overall_success_rate': successful_tests / total_tests if total_tests > 0 else 0
            }
            
            print(f"\n🎉 COMPREHENSIVE TESTING COMPLETED!")
            print(f"📊 Overall Success Rate: {self.test_results['overall']['overall_success_rate']*100:.1f}%")
            print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
            
            return self.test_results['overall']['overall_success_rate'] >= 0.8
            
        except Exception as e:
            print(f"❌ Error in comprehensive testing: {e}")
            return False
    
    def deploy_production_empire(self):
        """Deploy the trading empire in production mode"""
        try:
            if not self.empire:
                print("❌ Empire not initialized. Please run initialize_empire() first.")
                return False
            
            print("\n🚀 DEPLOYING PRODUCTION TRADING EMPIRE")
            print("=" * 60)
            print("🎯 Deploying for flawless 24/7 operation...")
            print("🤖 All bots will run continuously with enhanced monitoring")
            print("📊 Real-time performance tracking and error recovery")
            print("🛡️ Advanced risk management and portfolio protection")
            
            deploy_success = self.empire.deploy_production_trading_empire()
            
            if deploy_success:
                print("\n🎉 PRODUCTION DEPLOYMENT SUCCESSFULLY!")
                print("🚀 Your empire is now running in production mode!")
                self.deployment_active = True
                return True
            else:
                print("\n❌ Production deployment failed!")
                return False
                
        except Exception as e:
            print(f"❌ Error deploying production empire: {e}")
            return False
    
    def start_monitoring(self):
        """Start continuous monitoring of the deployed empire"""
        try:
            print("\n📊 Starting Continuous Monitoring...")
            self.monitoring_active = True
            
            # Start monitoring in background thread
            self.monitoring_thread = threading.Thread(target=self._monitoring_worker, daemon=True)
            self.monitoring_thread.start()
            
            print("✅ Continuous monitoring started!")
            return True
            
        except Exception as e:
            print(f"❌ Error starting monitoring: {e}")
            return False
    
    def _monitoring_worker(self):
        """Background monitoring worker"""
        try:
            while self.monitoring_active and self.deployment_active:
                try:
                    time.sleep(60)  # Check every minute
                    
                    if not self.empire or not self.deployment_active:
                        break
                    
                    # Get production status
                    status = self.empire.get_production_status()
                    if status != 'RUNNING':
                        print(f"⚠️ Production mode stopped unexpectedly: {status}")
                        break
                    
                    # Get performance metrics
                    performance = self.empire.get_production_performance()
                    if 'error' not in performance:
                        runtime_hours = performance.get('runtime_hours', 0)
                        total_trades = performance.get('total_trades', 0)
                        trades_per_hour = performance.get('trades_per_hour', 0)
                        error_count = performance.get('error_count', 0)
                        recovery_count = performance.get('recovery_count', 0)
                        
                        # Print status every 5 minutes
                        if int(time.time()) % 300 < 60:  # Every 5 minutes
                            print(f"\n📊 Production Status Update:")
                            print(f"   Runtime: {runtime_hours:.2f} hours")
                            print(f"   Total Trades: {total_trades}")
                            print(f"   Trades/Hour: {trades_per_hour:.2f}")
                            print(f"   Errors: {error_count}")
                            print(f"   Recoveries: {recovery_count}")
                            
                except Exception as e:
                    print(f"❌ Error in monitoring: {e}")
                    time.sleep(60)  # Wait before retrying
                    
        except Exception as e:
            print(f"❌ Fatal error in monitoring: {e}")
    
    def stop_deployment(self):
        """Stop the production deployment"""
        try:
            print("\n🛑 Stopping Production Deployment...")
            
            self.monitoring_active = False
            self.deployment_active = False
            
            if self.empire and hasattr(self.empire, 'stop_production_mode'):
                self.empire.stop_production_mode()
            
            print("✅ Production deployment stopped safely")
            return True
            
        except Exception as e:
            print(f"❌ Error stopping deployment: {e}")
            return False
    
    def get_deployment_status(self):
        """Get current deployment status"""
        return {
            'empire_initialized': self.empire is not None,
            'deployment_active': self.deployment_active,
            'monitoring_active': self.monitoring_active,
            'test_results': self.test_results
        }

def main():
    """Main deployment and testing process"""
    try:
        print("🚀 HYBRID ALGORAND TRADING EMPIRE")
        print("🎯 COMPREHENSIVE DEPLOYMENT & TESTING")
        print("=" * 60)
        
        # Initialize deployment manager
        manager = EmpireDeploymentManager()
        
        # Step 1: Initialize Empire
        print("\n🎯 Step 1: Initializing Trading Empire")
        if not manager.initialize_empire():
            print("❌ Empire initialization failed. Exiting.")
            return
        
        # Step 2: Run Comprehensive Testing
        print("\n🎯 Step 2: Running Comprehensive Testing")
        testing_success = manager.run_comprehensive_testing()
        
        if not testing_success:
            print("❌ Comprehensive testing failed. Please fix issues before deployment.")
            return
        
        # Step 3: Deploy Production Empire
        print("\n🎯 Step 3: Deploying Production Empire")
        deploy_success = manager.deploy_production_empire()
        
        if not deploy_success:
            print("❌ Production deployment failed. Please check configuration.")
            return
        
        # Step 4: Start Continuous Monitoring
        print("\n🎯 Step 4: Starting Continuous Monitoring")
        manager.start_monitoring()
        
        # Keep the deployment running
        print("\n⏳ Production deployment is running... Press Ctrl+C to stop")
        print("📊 Performance reports will be generated every hour")
        print("🔄 Trading cycles execute every 3 minutes")
        print("🛡️ Error recovery and monitoring systems are active")
        
        try:
            while True:
                time.sleep(60)  # Check every minute
                
                if not manager.deployment_active:
                    print("⚠️ Deployment stopped unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping deployment...")
            manager.stop_deployment()
            print("✅ Deployment stopped safely")
            
            # Print final test results
            print("\n📊 FINAL TEST RESULTS:")
            for test_name, results in manager.test_results.items():
                if test_name != 'overall':
                    if 'success_rate' in results:
                        print(f"   {test_name}: {results['success_rate']*100:.1f}%")
                    elif 'success' in results:
                        print(f"   {test_name}: {'PASS' if results['success'] else 'FAIL'}")
            
            overall = manager.test_results.get('overall', {})
            print(f"\n🏆 Overall Success Rate: {overall.get('overall_success_rate', 0)*100:.1f}%")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Deployment interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()






