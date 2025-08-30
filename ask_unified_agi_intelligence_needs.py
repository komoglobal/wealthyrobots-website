#!/usr/bin/env python3
"""
ASK UNIFIED AGI INTELLIGENCE NEEDS
PURPOSE: Evaluate what the unified AGI needs to improve its intelligence
         (memory, learning, reasoning, evaluation, data, tools) and output
         a prioritized list of suggestions.
STATUS: Active
FREQUENCY: On-demand
"""

import os
import json
import glob
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple


def exists_any(paths: List[str]) -> bool:
    return any(os.path.exists(p) for p in paths)


def find_any(patterns: List[str]) -> List[str]:
    found: List[str] = []
    for pattern in patterns:
        found.extend(glob.glob(pattern, recursive=True))
    return found


def assess_memory() -> Dict[str, Any]:
    """Check for long-term memory/knowledge base capabilities."""
    indicators = find_any([
        '**/*memory*.json', '**/*memory*.db', '**/knowledge*', '**/kb*', '**/vector*'
    ])
    needs: List[str] = []
    if not indicators:
        needs.append('Implement long-term memory store (JSON/SQLite/Vector DB) with retrieval API')
    else:
        # Check for recency/usage
        recent = max((os.path.getmtime(p) for p in indicators if os.path.isfile(p)), default=0)
        if recent == 0:
            needs.append('Populate and actively use memory store (currently empty or unused)')
    return {
        'present': bool(indicators),
        'artifacts': sorted(list(set(indicators)))[:25],
        'needs': needs
    }


def assess_meta_cognition() -> Dict[str, Any]:
    """Check for meta-cognitive/self-evaluation components."""
    files = find_any(['**/meta_cognitive*.*', '**/META_COGNITIVE*.*', '**/*self_interrogation*.py', '**/*intelligence_analysis*.py'])
    needs: List[str] = []
    if not files:
        needs.append('Add meta-cognitive loop (self-evaluation, stuck detection, self-repair)')
    return {
        'present': bool(files),
        'artifacts': sorted(list(set(files)))[:25],
        'needs': needs
    }


def assess_learning() -> Dict[str, Any]:
    """Check for learning datasets and continual learning hooks."""
    datasets = find_any(['**/data/**', '**/datasets/**', '**/*training*', '**/*curriculum*'])
    hooks = find_any(['**/*learn*hook*.py', '**/*continual*learn*.py'])
    needs: List[str] = []
    if not (datasets or hooks):
        needs.append('Create learning dataset and continual learning hooks (curriculum + feedback)')
    return {
        'present': bool(datasets or hooks),
        'artifacts': sorted(list(set(datasets + hooks)))[:25],
        'needs': needs
    }


def assess_evaluation() -> Dict[str, Any]:
    """Check for evaluation/benchmarks and scoring."""
    evals = find_any(['**/*benchmark*', '**/*eval*', '**/*scorecard*.json', '**/*capability*score*'])
    needs: List[str] = []
    if not evals:
        needs.append('Add benchmarking suite with tasks and success metrics (reasoning, tools, trading)')
    return {
        'present': bool(evals),
        'artifacts': sorted(list(set(evals)))[:25],
        'needs': needs
    }


def assess_tools() -> Dict[str, Any]:
    """Check for tool learning/grounding (search, web, data)."""
    tools = find_any(['**/*connector*.py', '**/*tool*.py', '**/*web_search*', '**/*browser*'])
    needs: List[str] = []
    if not tools:
        needs.append('Expand toolset (web search, structured data access) and add tool-use learning')
    return {
        'present': bool(tools),
        'artifacts': sorted(list(set(tools)))[:25],
        'needs': needs
    }


def assess_reasoning() -> Dict[str, Any]:
    """Check for reasoning enhancers and self-consistency mechanisms."""
    reasoners = find_any(['**/*reasoning*enhancer*.py', '**/*SystematicReasoning*.py', '**/dual_reasoning_enhancer.py', '**/simple_reasoning_enhancer.py'])
    needs: List[str] = []
    if not reasoners:
        needs.append('Add advanced reasoning strategies (self-consistency, debate, planning memory)')
    return {
        'present': bool(reasoners),
        'artifacts': sorted(list(set(reasoners)))[:25],
        'needs': needs
    }


def aggregate_intelligence_needs() -> Dict[str, Any]:
    report: Dict[str, Any] = {
        'timestamp': datetime.now().isoformat(),
        'areas': {},
        'summary_needs': []
    }
    areas = {
        'memory': assess_memory(),
        'meta_cognition': assess_meta_cognition(),
        'learning': assess_learning(),
        'evaluation': assess_evaluation(),
        'tools': assess_tools(),
        'reasoning': assess_reasoning()
    }
    report['areas'] = areas
    # Collect needs in priority order
    priority_order = ['memory', 'reasoning', 'meta_cognition', 'evaluation', 'learning', 'tools']
    for area in priority_order:
        report['summary_needs'].extend(areas[area]['needs'])
    # Dedup
    seen = set()
    report['summary_needs'] = [n for n in report['summary_needs'] if not (n in seen or seen.add(n))]
    return report


def print_human(report: Dict[str, Any]) -> None:
    print("\n🧠 Unified AGI - Intelligence Needs")
    print("=" * 40)
    if report['summary_needs']:
        print("\nTop needs:")
        for n in report['summary_needs'][:10]:
            print(f"- {n}")
    else:
        print("No critical intelligence needs detected.")
    print("\nAreas:")
    for area, data in report['areas'].items():
        status = 'present' if data['present'] else 'missing'
        print(f"- {area}: {status}")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description='Ask unified AGI what it needs for further intelligence')
    parser.add_argument('--json', action='store_true', help='Print JSON only')
    args = parser.parse_args()

    report = aggregate_intelligence_needs()
    try:
        with open('unified_agi_intelligence_needs.json', 'w') as fh:
            json.dump(report, fh, indent=2)
    except Exception:
        pass

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)


if __name__ == '__main__':
    main()


