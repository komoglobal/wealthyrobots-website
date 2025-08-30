#!/usr/bin/env python3
"""
Test script for updated profit tracking system
"""

import sys
import os
sys.path.append('.')

def test_profit_tracking():
    print("🧪 Testing Updated Profit Tracking System")
    print("=" * 50)
    
    try:
        from algofund.profit import ProfitTracker
        
        # Create profit tracker
        tracker = ProfitTracker()
        print("✅ ProfitTracker created successfully")
        
        # Check current state
        print(f"\n📊 Current State:")
        print(f"nav_start_usd: {tracker.state.get('nav_start_usd', 'N/A')}")
        print(f"last_nav_usd: {tracker.state.get('last_nav_usd', 'N/A')}")
        print(f"treasury_funding_usd: {tracker.state.get('treasury_funding_usd', 'N/A')}")
        print(f"real_trading_profit_usd: {tracker.state.get('real_trading_profit_usd', 'N/A')}")
        print(f"proper_tracking_initialized: {tracker.state.get('proper_tracking_initialized', 'N/A')}")
        
        # Test update with current NAV
        current_nav = 1053.86
        print(f"\n🔄 Testing update with NAV: ${current_nav}")
        
        snapshot = tracker.update(current_nav)
        print(f"✅ Update successful")
        print(f"Real Trading Profit: ${snapshot.real_trading_profit_usd:+,.2f}")
        print(f"Treasury Funding: ${snapshot.treasury_funding_usd:,.2f}")
        
        # Check updated state
        print(f"\n📊 Updated State:")
        print(f"treasury_funding_usd: {tracker.state.get('treasury_funding_usd', 'N/A')}")
        print(f"real_trading_profit_usd: {tracker.state.get('real_trading_profit_usd', 'N/A')}")
        print(f"daily_real_change: {tracker.state.get('daily_real_change', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_profit_tracking()
