#!/usr/bin/env python3
"""
ALGORAND TRADING FIRM MONITORING SCRIPT
Quick status check and PnL monitoring
"""

import json
import subprocess
import os
from datetime import datetime

def check_quick_status():
    """Quick status check of Algorand trading firm"""
    print("🔍 ALGORAND TRADING FIRM - QUICK STATUS CHECK")
    print("=" * 60)
    
    # Check if performance report exists
    if os.path.exists('algorand_performance_report.json'):
        try:
            with open('algorand_performance_report.json', 'r') as f:
                data = json.load(f)
            
            print(f"📊 Portfolio Status:")
            print(f"   Live NAV: ${data['portfolio_summary']['current_nav']:.2f}")
            print(f"   Paper NAV: ${data['portfolio_summary']['paper_nav']:.2f}")
            print(f"   Hot Wallet: {data['portfolio_summary']['hot_wallet_algo']:.6f} ALGO")
            print(f"   Active Trades: {data['portfolio_summary']['active_trades']}")
            
            print(f"\n💰 PnL Metrics:")
            print(f"   Daily PnL: ${data['pnl_metrics']['daily_pnl']:.2f}")
            print(f"   Total PnL: ${data['pnl_metrics']['total_pnl']:.2f}")
            
            print(f"\n🔄 Trading Activity:")
            print(f"   Total Transactions: {data['trading_activity']['total_transactions']}")
            print(f"   Volume: {data['trading_activity']['total_volume_microalgo']:,} microALGO")
            
            # Check data verification
            if data['verification_status']['real_data_verified']:
                print(f"\n✅ Real Data: VERIFIED")
            else:
                print(f"\n⚠️  Real Data: PENDING VERIFICATION")
                
        except Exception as e:
            print(f"❌ Error reading performance report: {e}")
    else:
        print("❌ No performance report found")
    
    # Check critical services
    print(f"\n🔧 Critical Services:")
    critical_services = ['algofund-paper', 'algofund-live', 'fund-manager']
    
    for service in critical_services:
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', f'{service}.service'],
                capture_output=True,
                text=True,
                timeout=5
            )
            status = result.stdout.strip()
            icon = "✅" if status == "active" else "❌"
            print(f"   {icon} {service}: {status}")
        except Exception as e:
            print(f"   ❌ {service}: error checking")
    
    print(f"\n⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    check_quick_status()
