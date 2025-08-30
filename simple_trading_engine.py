#!/usr/bin/env python3
"""
Simplified Trading Engine - Core functionality only
"""

import time
import os
from datetime import datetime

def main():
    print("🚀 SIMPLE TRADING ENGINE STARTED")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Simple scan interval
    scan_interval = 60  # 60 seconds for testing
    last_scan = 0

    print("🔄 Starting main loop...")
    iteration = 0

    try:
        while iteration < 10:  # Limit iterations for testing
            now = time.time()
            print(f"🔄 Main loop iteration {iteration + 1} at {now:.0f} (last_scan: {last_scan:.0f})")

            # Check scan interval
            if now - last_scan >= scan_interval:
                print(f"⏰ Scan interval triggered: now={now:.0f}, last_scan={last_scan:.0f}, diff={now-last_scan:.0f}s")

                # Simulate opportunity sweep
                print("🔄 Starting opportunity sweep...")
                try:
                    # Import and run sweep
                    from run_hybrid_trading_empire import do_defillama_sweep
                    sweep = do_defillama_sweep()

                    if sweep.get('top'):
                        print(f"📊 Sweep completed - found {len(sweep['top'])} top opportunities")
                        print(f"🎯 Top opp summary: {[ (o.get('source'), o.get('opportunity_type'), o.get('opportunity_score')) for o in sweep['top'] ]}")

                        # Simulate execution attempt
                        print("🚀 Triggering execution attempt...")
                        print("✅ Execution attempt completed")
                    else:
                        print("⚠️ No top opportunities found")

                except Exception as e:
                    print(f"❌ Sweep failed: {e}")
                    import traceback
                    traceback.print_exc()

                # Update last_scan
                print(f"🔄 Updating last_scan from {last_scan:.0f} to {now:.0f}")
                last_scan = now

            iteration += 1
            time.sleep(2)  # Small delay between iterations

        print("✅ SIMPLE ENGINE TEST COMPLETED")

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"❌ ENGINE ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()








