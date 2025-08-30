#!/usr/bin/env python3
"""
ASK UNIFIED AGI NEEDS
PURPOSE: Directly query the Unified AGI (HOW + WHY) analysis to report what it
         needs to upgrade or improve right now, with a proposed action plan.
CATEGORY: System Management
STATUS: Active
FREQUENCY: On-demand
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List

from UNIFIED_AGI_SYSTEM import UnifiedAGISystem
from REAL_AGI_HOW_EXECUTION_ENGINE import real_how_engine


async def collect_unified_needs() -> Dict[str, Any]:
    # Initialize HOW engine used by the unified system
    await real_how_engine.initialize()

    unified = UnifiedAGISystem()

    # Generate fresh insights (WHY/analysis)
    insights: List[Dict[str, Any]] = await unified._generate_agi_insights()  # noqa: SLF001

    # Build proposed actions (HOW/execution plan) without executing
    actions: List[Dict[str, Any]] = await real_how_engine.create_real_action_plan(insights)

    # Construct a compact needs report
    report: Dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "insights_count": len(insights),
        "actions_count": len(actions),
        "insights": insights,
        "proposed_actions": actions,
    }

    return report


def print_human(report: Dict[str, Any]) -> None:
    print("\n🧠 Unified AGI - Current Needs (HOW + WHY)")
    print("=" * 50)

    print(f"💡 Insights: {report['insights_count']}")
    for ins in report.get("insights", [])[:10]:
        summary = ins.get("summary", "(no summary)")
        priority = ins.get("priority", "-")
        ins_type = ins.get("type", "-")
        print(f"- [{priority}] {ins_type}: {summary}")

    if report['insights_count'] > 10:
        print(f"  ... and {report['insights_count'] - 10} more")

    print(f"\n🛠️  Proposed actions: {report['actions_count']}")
    for act in report.get("proposed_actions", [])[:10]:
        atype = act.get("type", "-")
        action = act.get("action", "-")
        target = act.get("target_system", "-")
        priority = act.get("priority", "-")
        print(f"- [{priority}] {atype} -> {action} (target: {target})")

    if report['actions_count'] > 10:
        print(f"  ... and {report['actions_count'] - 10} more")


async def amain() -> None:
    report = await collect_unified_needs()

    # Save JSON for downstream review
    try:
        with open("unified_agi_needs_report.json", "w") as fh:
            json.dump(report, fh, indent=2)
    except Exception:
        pass

    print_human(report)


if __name__ == "__main__":
    asyncio.run(amain())


