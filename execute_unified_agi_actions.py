#!/usr/bin/env python3
"""
EXECUTE UNIFIED AGI ACTIONS (ONE-SHOT)
PURPOSE: Generate fresh unified AGI insights (WHY), execute them via HOW engine,
         and summarize results.
STATUS: Active
FREQUENCY: On-demand
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List

from UNIFIED_AGI_SYSTEM import UnifiedAGISystem
from REAL_AGI_HOW_EXECUTION_ENGINE import real_how_engine


async def run_once() -> Dict[str, Any]:
    await real_how_engine.initialize()

    unified = UnifiedAGISystem()

    # Generate insights (WHY)
    insights: List[Dict[str, Any]] = await unified._generate_agi_insights()  # noqa: SLF001

    execution_results: List[Dict[str, Any]] = []
    successes = 0
    failures = 0

    # Execute each insight (HOW)
    for insight in insights:
        result = await real_how_engine.execute_insight(insight)
        execution_results.append(result)
        if result.get("execution_successful"):
            successes += 1
        else:
            failures += 1

    summary = {
        "timestamp": datetime.now().isoformat(),
        "insights": insights,
        "results": execution_results,
        "successes": successes,
        "failures": failures,
        "total": len(execution_results),
    }

    return summary


def print_human(summary: Dict[str, Any]) -> None:
    print("\n🚀 Unified AGI Execution - One-shot")
    print("=" * 40)
    print(f"Insights: {len(summary.get('insights', []))}")
    print(f"Executed: {summary.get('total', 0)} | ✅ {summary.get('successes', 0)} | ❌ {summary.get('failures', 0)}")

    # Show brief per-result status
    for idx, res in enumerate(summary.get("results", []), 1):
        status = "SUCCESS" if res.get("execution_successful") else "FAIL"
        label = res.get("execution_record", {}).get("insight_summary") or res.get("error", "action")
        print(f"- [{status}] {label}")


async def amain() -> None:
    summary = await run_once()

    # Persist for auditing
    try:
        with open("unified_agi_execution_results.json", "w") as fh:
            json.dump(summary, fh, indent=2)
    except Exception:
        pass

    print_human(summary)


if __name__ == "__main__":
    asyncio.run(amain())


