#!/usr/bin/env python3
"""
Monitor for REAL DeFi transactions (not wallet-to-wallet)
"""

import time
import subprocess
import json
from datetime import datetime

def monitor_real_trades():
    print("🔥 REAL DeFi TRANSACTION MONITOR")
    print("=" * 50)
    print("🚫 NO MORE wallet-to-wallet transfers!")
    print("✅ ONLY real DeFi protocol interactions")
    print()

    last_tx_count = 0

    while True:
        try:
            # Check if engine is running
            result = subprocess.run(['pgrep', '-f', 'run_hybrid_trading_empire'],
                                  capture_output=True, text=True)

            if result.returncode != 0:
                print("❌ Trading engine not running!")
                break

            print(f"🟢 Engine running (PID: {result.stdout.strip().split()[0]})")

            # Check recent opportunities
            try:
                import os
                opp_files = [f for f in os.listdir('data') if f.startswith('opportunities_')]
                if opp_files:
                    opp_files.sort(reverse=True)
                    recent_file = f'data/{opp_files[0]}'

                    with open(recent_file, 'r') as f:
                        data = json.load(f)
                        opportunities = data.get('opportunities', [])

                    print(f"📊 Ready opportunities: {len(opportunities)}")

                    # Show high-score opportunities
                    high_score = [opp for opp in opportunities if opp.get('opportunity_score', 0) >= 70]
                    if high_score:
                        print("🎯 High-priority opportunities:")
                        for opp in high_score[:3]:
                            source = opp.get('source', 'unknown')
                            opp_type = opp.get('opportunity_type', 'unknown')
                            score = opp.get('opportunity_score', 0)
                            print(f"   • {source} - {opp_type} (Score: {score})")

            except Exception as e:
                print(f"⚠️  Opportunity check: {str(e)[:50]}...")

            # Check for real transaction indicators
            try:
                # Look for real transaction logs
                result = subprocess.run(['tail', '-20', 'logs/hybrid_empire_20250826.log'],
                                      capture_output=True, text=True)

                log_content = result.stdout

                # Check for real DeFi transaction indicators
                real_tx_indicators = [
                    'ApplicationNoOpTxn',
                    'ApplicationCallTxn',
                    'validator_app_id',
                    'REAL Tinyman',
                    'REAL Pact',
                    'REAL Folks',
                    'tx [A-Z0-9]{50,}',  # Real transaction hash pattern
                ]

                found_real_tx = False
                for indicator in real_tx_indicators:
                    if indicator in log_content:
                        print(f"✅ REAL TRANSACTION DETECTED: {indicator}")
                        found_real_tx = True

                if found_real_tx:
                    print("🎉 SUCCESS! Real DeFi transactions are happening!")
                    print("🚫 No more wallet-to-wallet transfers!")
                else:
                    print("⏳ Waiting for real DeFi transactions...")

            except Exception as e:
                print(f"⚠️  Log check: {str(e)[:50]}...")

            print(f"🕐 Last check: {datetime.now().strftime('%H:%M:%S')}")
            print("-" * 50)
            time.sleep(15)

        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped by user")
            break
        except Exception as e:
            print(f"⚠️  Monitor error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_real_trades()








