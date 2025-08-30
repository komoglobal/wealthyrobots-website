#!/usr/bin/env python3
"""
Weekly Claude Upgrade Cycle
1) Generate agent capability scorecard
2) Run a focused Claude optimization cycle (functional agent)
3) Write a short summary file for CEO
"""

import json
from datetime import datetime
from agent_capability_scorecard import main as scorecap
from functional_claude_agent import FunctionalClaudeAgent

def main():
    # 1) Scorecard
    scorecap()

    # 2) Claude optimization
    agent = FunctionalClaudeAgent()
    results = agent.run_optimization_cycle()

    # 3) Summary for CEO
    summary = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_analyzed": results.get("files_analyzed", 0),
            "problems_found": results.get("problems_found", 0),
            "optimizations_applied": results.get("optimizations_applied", 0),
            "real_improvements": results.get("real_improvements", 0)
        }
    }
    with open("weekly_upgrade_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("✅ Weekly upgrade summary written: weekly_upgrade_summary.json")

if __name__ == "__main__":
    main()





