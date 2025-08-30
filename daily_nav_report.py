#!/usr/bin/env python3
import os
import json
from datetime import datetime


def load_health_entries(date_str: str):
    path = f"logs/hybrid_health_{date_str}.json"
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, 'r') as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except Exception:
                continue
    return entries


def main():
    date_str = datetime.now().strftime('%Y%m%d')
    entries = load_health_entries(date_str)
    if not entries:
        print("No health entries for today")
        return
    navs = [e.get('nav_estimate_usd') for e in entries if 'nav_estimate_usd' in e]
    start_nav = next((n for n in navs if isinstance(n, (int, float))), None)
    end_nav = next((n for n in reversed(navs) if isinstance(n, (int, float))), None)
    delta = None
    if start_nav is not None and end_nav is not None:
        delta = end_nav - start_nav
    report = {
        'date': date_str,
        'num_entries': len(entries),
        'start_nav': start_nav,
        'end_nav': end_nav,
        'pnl': delta
    }
    os.makedirs('reports', exist_ok=True)
    out_path = f"reports/daily_nav_{date_str}.json"
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()


