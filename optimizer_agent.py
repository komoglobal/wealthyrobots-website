#!/usr/bin/env python3
"""
OPTIMIZER AGENT
PURPOSE: Safely reduce redundancy, archive old variants/logs, and validate active agents
CATEGORY: Maintenance
STATUS: Active
"""

import os
import re
import json
import shutil
from datetime import datetime

PRIMARY_KEEP = {
    "social_media_agent.py",
    "unified_twitter_empire.py",
    "live_orchestrator.py",
    "dynamic_content_selector.py",
    "twitter_safety_config.py",
    "twitter_api_working.py",
    # deployment/testing core
    "integrated_deployment_system.py",
    "agent_coordinator.py",
    "enhanced_visual_testing_agent.py",
}

REDUNDANT_PATTERNS = [
    re.compile(r".*\.(BACKUP|INTEGRATED)$", re.I),
    re.compile(r".*_backup_\d{8}_\d{6}.*", re.I),
    re.compile(r"^(agent_backup_|backup_|empire_backup_).+", re.I),
]

LOG_PATTERNS = [
    re.compile(r".*\.log$", re.I),
    re.compile(r".*_log\.json$", re.I),
]

ARCHIVE_DIR = "archive"

class OptimizerAgent:
    def __init__(self, root="."):
        self.root = os.path.abspath(root)
        self.dry_run = os.getenv("OPTIMIZER_DRY_RUN", "0") == "1"
        self.now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.target_dir = os.path.join(self.root, ARCHIVE_DIR, self.now)
        self.manifest = {"timestamp": self.now, "dry_run": self.dry_run, "moved": []}

    def _is_redundant(self, relpath):
        name = os.path.basename(relpath)
        if name in PRIMARY_KEEP:
            return False
        for rx in REDUNDANT_PATTERNS:
            if rx.match(name) or rx.match(relpath):
                return True
        return False

    def _is_log(self, relpath):
        name = os.path.basename(relpath)
        for rx in LOG_PATTERNS:
            if rx.match(name):
                return True
        return False

    def _collect_candidates(self):
        red, logs = [], []
        for entry in os.listdir(self.root):
            if entry.startswith(ARCHIVE_DIR):
                continue
            path = os.path.join(self.root, entry)
            if os.path.isdir(path):
                # archive entire backup directories that match patterns
                for rx in REDUNDANT_PATTERNS:
                    if rx.match(entry):
                        red.append(entry)
                        break
            else:
                rel = entry
                if self._is_redundant(rel):
                    red.append(rel)
                elif self._is_log(rel):
                    logs.append(rel)
        return red, logs

    def _ensure_archive_dir(self):
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir, exist_ok=True)

    def _move(self, relpath):
        src = os.path.join(self.root, relpath)
        dst = os.path.join(self.target_dir, relpath)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if self.dry_run:
            return
        shutil.move(src, dst)
        self.manifest["moved"].append(relpath)

    def run(self):
        red, logs = self._collect_candidates()
        self._ensure_archive_dir()
        for rel in red + logs:
            self._move(rel)
        # save manifest
        if not self.dry_run:
            with open(os.path.join(self.target_dir, "archive_manifest.json"), 'w') as f:
                json.dump(self.manifest, f, indent=2)
        report = {
            "timestamp": self.now,
            "dry_run": self.dry_run,
            "redundant_candidates": red,
            "log_candidates": logs,
            "archive_path": self.target_dir,
        }
        print(json.dumps(report, indent=2))
        return report

if __name__ == "__main__":
    OptimizerAgent().run()



