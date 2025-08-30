#!/usr/bin/env python3
"""
Live Trading Monitor - Shows real-time trading activity
"""

import time
import subprocess
import json
from datetime import datetime

def monitor_live_trades():
    print("🔥 LIVE TRADING MONITOR")
    print("=" * 50)
    print("Monitoring for real transactions (not fallbacks)")
    print()

    last_log_size = 0

    while True:
        try:
            # Check if engine is running
            result = subprocess.run(['pgrep', '-f', 'run_hybrid_trading_empire'],
                                  capture_output=True, text=True)

            if result.returncode != 0:
                print("❌ Trading engine not running!")
                break

            # Check log file for new activity
            try:
                with open('logs/hybrid_empire_20250826.log', 'r') as f:
                    lines = f.readlines()
                    current_size = len(lines)

                    if current_size > last_log_size:
                        # Get new lines
                        new_lines = lines[last_log_size:]
                        last_log_size = current_size

                        # Look for trading activity
                        for line in new_lines:
                            if any(keyword in line for keyword in [
                                'validator_app_id: 1002541853',
                                'Transaction submitted',
                                'Transaction confirmed',
                                'Round',
                                'tx [A-Z0-9]',
                                '✅ ASA expansion: Seeded',
                                'Application does not exist'
                            ]):
                                timestamp = datetime.now().strftime('%H:%M:%S')
                                print(f"[{timestamp}] {line.strip()}")

                            elif 'Scan interval triggered' in line:
                                timestamp = datetime.now().strftime('%H:%M:%S')
                                print(f"[{timestamp}] 🔄 SCAN CYCLE STARTED")

                            elif 'Top opp summary' in line:
                                timestamp = datetime.now().strftime('%H:%M:%S')
                                print(f"[{timestamp}] 🎯 OPPORTUNITIES FOUND")

                            elif 'Triggering execution' in line:
                                timestamp = datetime.now().strftime('%H:%M:%S')
                                print(f"[{timestamp}] 🚀 EXECUTION STARTED")

            except FileNotFoundError:
                print("Waiting for log file...")
                time.sleep(5)
                continue

            time.sleep(1)  # Check every second

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_live_trades()








