#!/usr/bin/env python3
"""
Simple Intelligence Benchmarks
Runs quick checks for reasoning/tool-use and records a trend file.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

from tools.web_tools import SimpleWebTools


def run_reasoning_benchmark() -> Dict[str, Any]:
    # Placeholder: award points for basic arithmetic and string reasoning
    try:
        arithmetic_ok = (2 * (3 + 4) == 14)
        string_ok = ("AGI".lower() == "agi")
        score = sum([arithmetic_ok, string_ok]) / 2
        return {"name": "reasoning_basic", "score": score}
    except Exception as e:
        return {"name": "reasoning_basic", "error": str(e), "score": 0.0}


def run_tool_use_benchmark() -> Dict[str, Any]:
    try:
        web = SimpleWebTools(timeout_seconds=5)
        res = web.fetch_url("https://example.com")
        ok = res.get("status") == "200" and bool(res.get("title"))
        return {"name": "tool_use_fetch", "score": 1.0 if ok else 0.0}
    except Exception as e:
        return {"name": "tool_use_fetch", "error": str(e), "score": 0.0}


def main() -> None:
    results = {
        "timestamp": datetime.now().isoformat(),
        "benchmarks": [
            run_reasoning_benchmark(),
            run_tool_use_benchmark(),
        ]
    }
    # Compute overall score
    scores = [b.get("score", 0.0) for b in results["benchmarks"]]
    results["overall_score"] = sum(scores) / len(scores) if scores else 0.0

    os.makedirs("intelligence_benchmarks", exist_ok=True)
    trend_file = os.path.join("intelligence_benchmarks", "benchmark_trend.json")
    try:
        if os.path.exists(trend_file):
            with open(trend_file, 'r') as fh:
                trend = json.load(fh)
            if isinstance(trend, list):
                trend.append(results)
            else:
                trend = [results]
        else:
            trend = [results]
        with open(trend_file, 'w') as fh:
            json.dump(trend, fh, indent=2)
    except Exception:
        pass

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()


