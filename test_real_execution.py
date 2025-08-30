#!/usr/bin/env python3
"""
Test script to verify real Pact DEX execution
"""

import asyncio
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_pact_integration():
    """Test the real Pact DEX integration"""
    try:
        print("🧪 Testing real Pact DEX integration...")
        
        # Import the trading agent
        from algorand_defi_trading_agent import AlgorandDeFiTradingAgent
        
        # Create agent instance
        agent = AlgorandDeFiTradingAgent()
        
        print("📊 Testing Pact pool data retrieval...")
        
        # Test getting pool data
        pool_data = await agent._get_pact_pool_data("ALGO", "USDC")
        if pool_data:
            print(f"✅ Pool data retrieved: {pool_data.get('asset_a_symbol', 'N/A')}/{pool_data.get('asset_b_symbol', 'N/A')}")
            print(f"   Reserves: {pool_data.get('asset_a_reserves', 'N/A')} / {pool_data.get('asset_b_reserves', 'N/A')}")
        else:
            print("❌ Failed to get pool data")
            return False
        
        print("🧮 Testing output calculation...")
        
        # Test output calculation
        amount_in = 10.0  # 10 ALGO
        expected_output = await agent._calculate_pact_output("ALGO", "USDC", amount_in, pool_data)
        if expected_output:
            print(f"✅ Output calculated: {amount_in} ALGO → {expected_output:.4f} USDC")
        else:
            print("❌ Failed to calculate output")
            return False
        
        print("🚀 Testing real trade execution...")
        
        # Test real trade execution (small amount for safety)
        test_amount = 1.0  # 1 ALGO for testing
        result = await agent.execute_pact_trade(
            action='swap',
            asset_in='ALGO',
            asset_out='USDC',
            amount=test_amount,
            min_received=test_amount * 0.95  # 5% slippage tolerance
        )
        
        if result and result.get('success'):
            print(f"✅ Real trade executed successfully!")
            print(f"   Transaction: {result.get('tx_hash', 'N/A')}")
            print(f"   Received: {result.get('received_amount', 'N/A')} USDC")
            print(f"   Fee: {result.get('fee', 'N/A')} ALGO")
            print(f"   Slippage: {result.get('slippage', 'N/A'):.2%}")
            return True
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'No result'
            print(f"❌ Trade execution failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_market_making_execution():
    """Test the market making agent with real execution"""
    try:
        print("\n🧪 Testing market making agent with real execution...")
        
        # Import the market making agent
        from algofund.agents.market_making import EnhancedMarketMakingAgent
        
        # Create agent instance
        agent = EnhancedMarketMakingAgent()
        
        print("📊 Testing real order placement...")
        
        # Test placing a real order
        success = await agent._place_order(
            position=None,
            order_type='buy',
            price=0.0,  # Market order
            amount=1.0   # 1 ALGO
        )
        
        if success:
            print("✅ Real order placed successfully!")
            return True
        else:
            print("❌ Real order placement failed")
            return False
            
    except Exception as e:
        print(f"❌ Market making test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting real execution tests...\n")
    
    # Test 1: Pact integration
    pact_success = await test_pact_integration()
    
    # Test 2: Market making execution
    mm_success = await test_market_making_execution()
    
    print("\n" + "="*50)
    print("📋 TEST RESULTS SUMMARY")
    print("="*50)
    print(f"Pact Integration: {'✅ PASSED' if pact_success else '❌ FAILED'}")
    print(f"Market Making:   {'✅ PASSED' if mm_success else '❌ FAILED'}")
    
    if pact_success and mm_success:
        print("\n🎉 All tests passed! Real execution is working.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
