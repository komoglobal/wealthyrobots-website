#!/usr/bin/env python3
"""
AGI NEEDS QUERY
PURPOSE: Aggregate agent self-improvement suggestions, status signals, and optimization reports
         into a concise list of current "needs" for upgrades or assistance.
CATEGORY: System Management
STATUS: Active
FREQUENCY: On-demand
"""

import json
import os
import glob
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load a JSON file if it exists. Returns None if missing or invalid."""
    try:
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r") as file_handle:
            return json.load(file_handle)
    except Exception:
        return None


def find_latest_json(pattern: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    """Find and load the newest JSON file matching a glob pattern."""
    try:
        candidates = glob.glob(pattern)
        if not candidates:
            return None
        candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        latest_path = candidates[0]
        payload = load_json_file(latest_path)
        if payload is None:
            return None
        return latest_path, payload
    except Exception:
        return None


def summarize_optimization_actions(optimization_report: Dict[str, Any]) -> List[str]:
    """Convert optimization actions into human-readable needs."""
    needs: List[str] = []
    actions = optimization_report.get("optimization_actions", [])
    for action in actions:
        action_type = action.get("type")
        description = action.get("description")
        if action_type == "resolve_duplicate":
            involved = action.get("agents_involved") or action.get("agents") or []
            if isinstance(involved, list):
                involved_str = ", ".join(involved)
            else:
                involved_str = str(involved)
            recommendation = action.get("recommendation", {})
            rec_action = recommendation.get("action")
            primary = (recommendation.get("primary_agent") or
                       recommendation.get("primary") or "primary agent")
            secondary = (recommendation.get("secondary_agent") or
                         recommendation.get("secondary") or "secondary agent")
            if rec_action == "merge":
                needs.append(f"Merge duplicate agents: keep {primary}, integrate {secondary} (involved: {involved_str})")
            elif rec_action == "consolidate":
                needs.append(f"Consolidate agents: {involved_str} into a single optimized agent")
            else:
                if description:
                    needs.append(description)
    return needs


def extract_agents_with_errors(coordination_or_status: Dict[str, Any]) -> List[str]:
    """Find agents with status 'error' or explicit error messages in coordination/status reports."""
    needs: List[str] = []
    agent_status = coordination_or_status.get("agent_status")
    if isinstance(agent_status, dict):
        for agent_name, status_obj in agent_status.items():
            if isinstance(status_obj, dict) and status_obj.get("status") == "error":
                needs.append(f"Fix failing agent: {agent_name}")
    qa_results = coordination_or_status.get("qa_results")
    if isinstance(qa_results, dict):
        for _, value in qa_results.items():
            if isinstance(value, str) and value:
                needs.append(f"QA issue: {value}")
    return needs


def extract_agents_needing_attention(status_cycle: Dict[str, Any]) -> List[str]:
    """Summarize agents that are not running or flagged as needing attention."""
    needs: List[str] = []
    count = status_cycle.get("agents_needing_attention")
    if isinstance(count, int) and count > 0:
        needs.append(f"Start or investigate {count} agents marked as needing attention")
    running_agents = status_cycle.get("running_agents")
    if isinstance(running_agents, list):
        not_running = [a for a in running_agents if "not running" in a]
        if not_running:
            needs.append(f"Agents not running: {', '.join(not_running)}")
    return needs


def extract_empire_wide_improvements(suggestions: Dict[str, Any]) -> List[str]:
    items = suggestions.get("empire_wide_improvements")
    if isinstance(items, list):
        return [str(x) for x in items]
    return []


def extract_per_agent_suggestions(suggestions: Dict[str, Any]) -> List[str]:
    results: List[str] = []
    per_agent = suggestions.get("suggestions")
    if isinstance(per_agent, dict):
        for agent_file, agent_suggestions in per_agent.items():
            if isinstance(agent_suggestions, list) and agent_suggestions:
                joined = "; ".join(agent_suggestions)
                results.append(f"{agent_file}: {joined}")
    return results


def aggregate_needs() -> Dict[str, Any]:
    """Aggregate needs from multiple existing artifacts."""
    needs_report: Dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "sources": {},
        "needs": {
            "critical_fixes": [],
            "operations": [],
            "optimization": [],
            "system_improvements": [],
            "per_agent": []
        }
    }

    suggestions = load_json_file("agent_improvement_suggestions.json")
    if suggestions:
        needs_report["sources"]["agent_improvement_suggestions.json"] = True
        needs_report["needs"]["system_improvements"].extend(
            extract_empire_wide_improvements(suggestions)
        )
        needs_report["needs"]["per_agent"].extend(
            extract_per_agent_suggestions(suggestions)
        )
    else:
        needs_report["sources"]["agent_improvement_suggestions.json"] = False

    optimization = load_json_file("agent_optimization_report.json")
    if optimization:
        needs_report["sources"]["agent_optimization_report.json"] = True
        needs_report["needs"]["optimization"].extend(
            summarize_optimization_actions(optimization)
        )
        sys_improvements = optimization.get("system_improvements")
        if isinstance(sys_improvements, list):
            needs_report["needs"]["system_improvements"].extend(sys_improvements)
    else:
        needs_report["sources"]["agent_optimization_report.json"] = False

    upgrade_report = load_json_file("agent_upgrade_report.json")
    if upgrade_report:
        needs_report["sources"]["agent_upgrade_report.json"] = True
        health = upgrade_report.get("agent_health_status")
        if isinstance(health, dict):
            for agent_file, score in health.items():
                try:
                    numeric = float(score)
                except Exception:
                    continue
                if numeric < 6.0:
                    needs_report["needs"]["optimization"].append(
                        f"Improve agent health: {agent_file} (score {numeric}/10)"
                    )
    else:
        needs_report["sources"]["agent_upgrade_report.json"] = False

    latest_coordination = find_latest_json("agent_coordination_report_*.json")
    if latest_coordination:
        path, payload = latest_coordination
        needs_report["sources"][path] = True
        needs_report["needs"]["critical_fixes"].extend(
            extract_agents_with_errors(payload)
        )
    else:
        needs_report["sources"]["agent_coordination_report_*.json"] = False

    latest_status_cycle = find_latest_json("agent_status_cycle_*.json")
    if latest_status_cycle:
        path, payload = latest_status_cycle
        needs_report["sources"][path] = True
        needs_report["needs"]["operations"].extend(
            extract_agents_needing_attention(payload)
        )
    else:
        needs_report["sources"]["agent_status_cycle_*.json"] = False

    deployment = load_json_file("deployment_coordination.json")
    if deployment:
        needs_report["sources"]["deployment_coordination.json"] = True
    else:
        needs_report["sources"]["deployment_coordination.json"] = False

    deduped: Dict[str, List[str]] = {}
    for category, items in needs_report["needs"].items():
        seen: set = set()
        deduped[category] = []
        for item in items:
            if item not in seen:
                deduped[category].append(item)
                seen.add(item)
    needs_report["needs"] = deduped

    return needs_report


def print_human_readable(needs_report: Dict[str, Any]) -> None:
    print("\n🤖 AGI NEEDS - CURRENT ASSESSMENT")
    print("=" * 40)
    needs = needs_report.get("needs", {})

    critical = needs.get("critical_fixes", [])
    if critical:
        print("\n🚨 Critical fixes:")
        for item in critical:
            print(f"- {item}")

    ops = needs.get("operations", [])
    if ops:
        print("\n⚙️  Operations:")
        for item in ops:
            print(f"- {item}")

    optimization = needs.get("optimization", [])
    if optimization:
        print("\n🧠 Optimization:")
        for item in optimization:
            print(f"- {item}")

    sys_improvements = needs.get("system_improvements", [])
    if sys_improvements:
        print("\n🏗️  System improvements:")
        for item in sys_improvements:
            print(f"- {item}")

    per_agent = needs.get("per_agent", [])
    if per_agent:
        print("\n📌 Per-agent suggestions:")
        for item in per_agent:
            print(f"- {item}")

    print("\n📄 Source coverage:")
    for source, present in needs_report.get("sources", {}).items():
        status = "found" if present else "missing"
        print(f"- {source}: {status}")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Ask the AGI system what it needs")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    parser.add_argument("--out", type=str, default="agi_needs_report.json", help="Write aggregated report to this file")
    args = parser.parse_args()

    report = aggregate_needs()

    try:
        with open(args.out, "w") as fh:
            json.dump(report, fh, indent=2)
    except Exception:
        pass

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human_readable(report)


if __name__ == "__main__":
    main()


