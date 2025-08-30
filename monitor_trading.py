#!/usr/bin/env python3
"""
Real-time Trading Engine Monitor
Shows live trading activity and transaction status
"""

import time
import os
import json
from datetime import datetime

def monitor_trading():
    print("🔥 WEALTHY ROBOT TRADING MONITOR")
    print("=" * 50)
    print()

    while True:
        try:
            # Check engine status
            import subprocess
            result = subprocess.run(['pgrep', '-f', 'run_hybrid_trading_empire'],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                pid = result.stdout.strip().split('\n')[0]
                print(f"✅ Engine RUNNING (PID: {pid})")
            else:
                print("❌ Engine NOT RUNNING")
                break

            # Check recent opportunities
            try:
                opp_files = [f for f in os.listdir('data') if f.startswith('opportunities_')]
                if opp_files:
                    opp_files.sort(reverse=True)
                    recent_file = f'data/{opp_files[0]}'

                    with open(recent_file, 'r') as f:
                        data = json.load(f)

                    opportunities = data.get('opportunities', [])
                    total_opp = len(opportunities)

                    # Count by type
                    opp_types = {}
                    for opp in opportunities:
                        opp_type = opp.get('opportunity_type', 'unknown')
                        opp_types[opp_type] = opp_types.get(opp_type, 0) + 1

                    print(f"📊 Opportunities: {total_opp} found")
                    print(f"🎯 Top types: {', '.join([f'{k}({v})' for k,v in list(opp_types.items())[:3]])}")

            except Exception as e:
                print(f"⚠️  Opportunity data: {str(e)[:50]}...")

            # Show current time and next scan
            now = datetime.now().strftime("%H:%M:%S")
            print(f"🕐 Last update: {now}")
            print("⏳ Next scan in ~60 seconds...")
            print("-" * 50)
            time.sleep(10)

        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped by user")
            break
        except Exception as e:
            print(f"⚠️  Monitor error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_trading()








