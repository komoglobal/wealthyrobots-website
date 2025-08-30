#!/usr/bin/env python3
"""
Nightly maintenance:
- Run intelligence benchmarks
- Ask needs (ops and intelligence)
- Save a consolidated maintenance report
"""

import json
import subprocess
from datetime import datetime
import os


def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, cwd=os.path.abspath(os.path.dirname(__file__)))
        return out.strip()
    except subprocess.CalledProcessError as e:
        return e.output.strip()


def main():
    report = {"timestamp": datetime.now().isoformat()}
    # Benchmarks
    bench = run_cmd("PYTHONPATH=. python3 intelligence_benchmarks/run_benchmarks.py")
    report["benchmarks"] = bench
    # Ops needs
    ops = run_cmd("python3 ask_agi_needs.py --json")
    report["ops_needs"] = ops
    # Intelligence needs
    intel = run_cmd("python3 ask_unified_agi_intelligence_needs.py --json")
    report["intelligence_needs"] = intel
    # Save
    with open("nightly_maintenance_report.json", "w") as fh:
        json.dump(report, fh, indent=2)
    print("Nightly maintenance complete.")


if __name__ == "__main__":
    main()


