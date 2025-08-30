#!/usr/bin/env python3
"""
Agent Capability Scorecard
Evaluates key agents for reliability, observability, and safety heuristics and emits JSON + Markdown reports.
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List

AGENTS = [
    "smart_scheduler.py",
    "integrated_deployment_system.py",
    "enhanced_visual_testing_agent.py",
    "social_media_agent.py",
    "optimized_content_agent.py",
    "live_orchestrator.py",
    "ultimate_ceo_agent.py",
]


def read(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def score_agent(code: str) -> Dict:
    if not code:
        return {
            "exists": False,
            "score": 0,
            "checks": {},
            "recommendations": ["File missing"]
        }

    checks = {
        "has_logging": bool(re.search(r"\bimport\s+logging\b", code)),
        "print_count": code.count("print("),
        "try_except_blocks": len(re.findall(r"\btry:\s*[\s\S]*?\bexcept\b", code)),
        "timeouts_present": bool(re.search(r"timeout\s*=\s*\d+", code)),
        "retries_backoff": bool(re.search(r"(retry|backoff)", code, re.I)),
    }

    score = 0
    score += 20 if checks["has_logging"] else 0
    score += max(0, 20 - min(checks["print_count"], 20))  # fewer prints → more points
    score += min(checks["try_except_blocks"] * 5, 25)
    score += 10 if checks["timeouts_present"] else 0
    score += 10 if checks["retries_backoff"] else 0

    recs: List[str] = []
    if not checks["has_logging"]:
        recs.append("Add logging and replace print with logging.* where appropriate")
    if checks["print_count"] > 10:
        recs.append("Reduce excessive print statements; prefer logging with levels")
    if checks["try_except_blocks"] < 2:
        recs.append("Add error handling (try/except) around external calls")
    if not checks["timeouts_present"]:
        recs.append("Set timeouts for network/subprocess calls")
    if not checks["retries_backoff"]:
        recs.append("Implement retries with exponential backoff for flaky operations")

    return {
        "exists": True,
        "score": score,
        "checks": checks,
        "recommendations": recs,
    }


def main():
    results: Dict[str, Dict] = {}
    for agent in AGENTS:
        results[agent] = score_agent(read(agent))

    overall = sum(r["score"] for r in results.values()) / max(len(results), 1)
    report = {
        "timestamp": datetime.now().isoformat(),
        "overall_score": round(overall, 1),
        "agents": results,
    }

    # Save JSON
    json_path = f"capability_scorecard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Save Markdown summary
    md_lines = [
        f"# Agent Capability Scorecard ({report['timestamp']})",
        f"Overall Score: {report['overall_score']}/100\n",
    ]
    for name, res in results.items():
        md_lines.append(f"## {name}")
        md_lines.append(f"- Score: {res['score']}")
        md_lines.append(f"- Exists: {res['exists']}")
        md_lines.append(f"- Checks: {json.dumps(res['checks'])}")
        if res["recommendations"]:
            md_lines.append("- Recommendations:")
            for r in res["recommendations"]:
                md_lines.append(f"  - {r}")
        md_lines.append("")

    md_path = f"capability_scorecard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"✅ Capability scorecard saved: {json_path}, {md_path}")


if __name__ == "__main__":
    main()





