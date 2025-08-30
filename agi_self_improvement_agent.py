#!/usr/bin/env python3
"""
AGI Self-Improvement Agent
Enables AGI to autonomously implement its own fixes and improvements
"""

import os
import json
import re
import ast
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional

from agent_logging_utils import AgentLogger, AgentUtils, with_timeout, with_retry

class AGISelfImprovementAgent:
    """Agent that enables AGI to autonomously implement its own improvements"""

    def __init__(self):
        self.logger = AgentLogger("agi_self_improvement_agent")
        self.improvement_history = []
        self.safe_edit_patterns = self._load_safe_patterns()
        self.backup_dir = "backups/agi_improvements"
        os.makedirs(self.backup_dir, exist_ok=True)

    def _load_safe_patterns(self) -> Dict[str, Any]:
        """Load patterns for safe code modifications"""
        return {
            "logging_replacements": {
                r"print\(": "self.logger.info(",
                r"print\('([^']+)'\)": r"self.logger.info('\1'",
                r'print\("([^"]+)"\)': r'self.logger.info("\1"'
            },
            "timeout_additions": {
                r"subprocess\.run\(": "subprocess.run(..., timeout=30",
                r"requests\.get\(": "requests.get(..., timeout=30",
                r"urllib\.request\.urlopen\(": "urllib.request.urlopen(..., timeout=30"
            },
            "retry_patterns": {
                r"def ([a-zA-Z_][a-zA-Z0-9_]*)\(": r"@with_retry\n    def \1("
            }
        }

    @with_timeout(300)  # 5 minutes max for self-improvement
    def analyze_and_implement_improvements(self, analysis_report: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze issues and autonomously implement fixes"""
        self.logger.info("Starting autonomous self-improvement cycle")

        results = {
            "timestamp": datetime.now().isoformat(),
            "issues_analyzed": len(analysis_report.get("issues", [])),
            "improvements_implemented": 0,
            "files_modified": [],
            "backups_created": [],
            "errors": []
        }

        # Process each issue
        for issue in analysis_report.get("issues", []):
            try:
                if self._can_fix_autonomously(issue):
                    fix_result = self._implement_fix(issue)
                    if fix_result["success"]:
                        results["improvements_implemented"] += 1
                        results["files_modified"].extend(fix_result["files_modified"])
                        results["backups_created"].extend(fix_result["backups_created"])
                    else:
                        results["errors"].append(f"Fix failed for {issue['type']}: {fix_result.get('error')}")
            except Exception as e:
                results["errors"].append(f"Error processing {issue['type']}: {str(e)}")

        self.logger.info("Self-improvement cycle completed", results=results)
        return results

    def _can_fix_autonomously(self, issue: Dict[str, Any]) -> bool:
        """Check if this issue can be fixed autonomously"""
        fixable_types = [
            "logging_issues",
            "print_statements",
            "missing_timeouts",
            "missing_retries",
            "simple_syntax_fixes"
        ]

        return (
            issue.get("type") in fixable_types and
            issue.get("severity") in ["low", "medium"] and
            not issue.get("requires_human_approval", False)
        )

    def _implement_fix(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Implement a specific fix"""
        issue_type = issue.get("type")

        if issue_type == "logging_issues":
            return self._fix_logging_issues(issue)
        elif issue_type == "print_statements":
            return self._fix_print_statements(issue)
        elif issue_type == "missing_timeouts":
            return self._add_timeouts(issue)
        elif issue_type == "missing_retries":
            return self._add_retries(issue)
        else:
            return {"success": False, "error": f"Unknown issue type: {issue_type}", "files_modified": [], "backups_created": []}

    def _fix_logging_issues(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Fix logging configuration issues"""
        target_files = issue.get("affected_files", [])

        for file_path in target_files:
            if not os.path.exists(file_path):
                continue

            self._create_backup(file_path)

            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Add proper logging import if missing
                if "from agent_logging_utils import" not in content:
                    content = self._add_logging_import(content)

                # Replace basic logging setup with proper logger
                content = self._replace_basic_logging(content, file_path)

                with open(file_path, 'w') as f:
                    f.write(content)

                self.logger.info("Fixed logging in file", file=file_path)

            except Exception as e:
                return {"success": False, "error": str(e), "files_modified": [], "backups_created": []}

        return {"success": True, "files_modified": target_files, "backups_created": []}

    def _fix_print_statements(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Replace print statements with proper logging"""
        target_files = issue.get("affected_files", [])
        modified_files = []

        for file_path in target_files:
            if not os.path.exists(file_path):
                continue

            self._create_backup(file_path)

            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Replace print statements with logging
                for pattern, replacement in self.safe_edit_patterns["logging_replacements"].items():
                    content = re.sub(pattern, replacement, content)

                # Add logger initialization if missing
                if "self.logger =" not in content and "AgentLogger" in content:
                    content = self._add_logger_initialization(content, file_path)

                with open(file_path, 'w') as f:
                    f.write(content)

                modified_files.append(file_path)
                self.logger.info("Replaced print statements with logging", file=file_path)

            except Exception as e:
                return {"success": False, "error": str(e), "files_modified": [], "backups_created": []}

        return {"success": True, "files_modified": modified_files}

    def _add_timeouts(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Add timeouts to network/subprocess calls"""
        target_files = issue.get("affected_files", [])
        modified_files = []

        for file_path in target_files:
            if not os.path.exists(file_path):
                continue

            self._create_backup(file_path)

            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Add timeouts to common patterns
                for pattern, replacement in self.safe_edit_patterns["timeout_additions"].items():
                    content = re.sub(pattern, replacement, content)

                with open(file_path, 'w') as f:
                    f.write(content)

                modified_files.append(file_path)
                self.logger.info("Added timeouts to file", file=file_path)

            except Exception as e:
                return {"success": False, "error": str(e), "files_modified": [], "backups_created": []}

        return {"success": True, "files_modified": modified_files}

    def _add_retries(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Add retry logic to functions"""
        target_files = issue.get("affected_files", [])
        modified_files = []

        for file_path in target_files:
            if not os.path.exists(file_path):
                continue

            self._create_backup(file_path)

            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Add retry decorators to function definitions
                content = re.sub(
                    r'def ([a-zA-Z_][a-zA-Z0-9_]*)\(',
                    r'@with_retry\n    def \1(',
                    content
                )

                with open(file_path, 'w') as f:
                    f.write(content)

                modified_files.append(file_path)
                self.logger.info("Added retry logic to file", file=file_path)

            except Exception as e:
                return {"success": False, "error": str(e), "files_modified": [], "backups_created": []}

        return {"success": True, "files_modified": modified_files}

    def _create_backup(self, file_path: str) -> str:
        """Create a backup of the file before modification"""
        import shutil

        backup_name = f"{os.path.basename(file_path)}.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = os.path.join(self.backup_dir, backup_name)

        shutil.copy2(file_path, backup_path)
        self.logger.info("Backup created", original=file_path, backup=backup_path)

        return backup_path

    def _add_logging_import(self, content: str) -> str:
        """Add logging import to file"""
        if "from agent_logging_utils import" not in content:
            lines = content.split('\n')
            # Find a good place to add the import (after existing imports)
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    insert_index = i + 1
                elif line.strip() and not line.startswith('#'):
                    break

            lines.insert(insert_index, "from agent_logging_utils import AgentLogger, AgentUtils, with_timeout, with_retry")
            content = '\n'.join(lines)

        return content

    def _replace_basic_logging(self, content: str, file_path: str) -> str:
        """Replace basic logging setup with proper logger"""
        # Extract class name from file path
        class_name = os.path.basename(file_path).replace('.py', '').replace('_', ' ').title().replace(' ', '')

        # Replace logging setup with proper logger
        if "logging.getLogger(__name__)" in content:
            content = content.replace(
                "logging.getLogger(__name__)",
                f"AgentLogger('{class_name.lower()}')"
            )

        return content

    def _add_logger_initialization(self, content: str, file_path: str) -> str:
        """Add logger initialization to class"""
        class_name = os.path.basename(file_path).replace('.py', '').replace('_', ' ').title().replace(' ', '')

        # Find __init__ method
        init_pattern = r'def __init__\([^)]*\):'
        if re.search(init_pattern, content):
            # Add logger initialization after the first line of __init__
            content = re.sub(
                r'(def __init__\(self[^)]*\):\s*\n\s*)',
                f'\\1        self.logger = AgentLogger("{class_name.lower()}")\n        ',
                content
            )

        return content

    def generate_self_improvement_report(self, results: Dict[str, Any]) -> str:
        """Generate a report of self-improvement activities"""
        report = f"""
🤖 AGI SELF-IMPROVEMENT REPORT
{'=' * 50}
Timestamp: {results.get('timestamp', 'Unknown')}

📊 IMPROVEMENT SUMMARY:
• Issues Analyzed: {results.get('issues_analyzed', 0)}
• Improvements Implemented: {results.get('improvements_implemented', 0)}
• Files Modified: {len(results.get('files_modified', []))}
• Backups Created: {len(results.get('backups_created', []))}

📁 MODIFIED FILES:
"""

        for file in results.get('files_modified', []):
            report += f"• {file}\n"

        if results.get('errors'):
            report += "\n❌ ERRORS ENCOUNTERED:\n"
            for error in results.get('errors'):
                report += f"• {error}\n"

        report += "\n🎯 AUTONOMOUS IMPROVEMENT CAPABILITIES:\n"
        report += "• Logging Enhancement\n"
        report += "• Timeout Implementation\n"
        report += "• Retry Logic Addition\n"
        report += "• Code Structure Optimization\n"

        return report.strip()

def main():
    """Test the AGI self-improvement agent"""
    agent = AGISelfImprovementAgent()

    # Simulate an analysis report
    test_report = {
        "issues": [
            {
                "type": "print_statements",
                "severity": "medium",
                "affected_files": ["test_agent.py"],
                "description": "Replace print statements with logging"
            },
            {
                "type": "logging_issues",
                "severity": "low",
                "affected_files": ["test_agent.py"],
                "description": "Improve logging configuration"
            }
        ]
    }

    results = agent.analyze_and_implement_improvements(test_report)
    report = agent.generate_self_improvement_report(results)

    print(report)

if __name__ == "__main__":
    main()
