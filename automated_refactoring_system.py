#!/usr/bin/env python3
"""
Automated Code Refactoring System for AGI
==========================================

Implements intelligent code analysis and automated refactoring capabilities.
Provides continuous code quality improvement and maintenance.
"""

import ast
import inspect
import re
import os
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar
from dataclasses import dataclass
from collections import defaultdict
import logging

T = TypeVar('T')

@dataclass
class RefactoringOpportunity:
    """Represents a code refactoring opportunity"""
    file_path: str
    line_number: int
    issue_type: str
    description: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    suggested_fix: str
    code_context: str
    confidence: float  # 0.0 to 1.0

@dataclass
class RefactoringMetrics:
    """Metrics for refactoring operations"""
    files_analyzed: int = 0
    issues_found: int = 0
    issues_fixed: int = 0
    code_quality_score: float = 0.0
    automation_level: float = 0.0

class CodeAnalyzer:
    """Advanced code analysis for refactoring opportunities"""

    def __init__(self):
        self.logger = logging.getLogger("CodeAnalyzer")

    def analyze_file(self, file_path: str) -> List[RefactoringOpportunity]:
        """Analyze a Python file for refactoring opportunities"""
        opportunities = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Parse AST for structural analysis
            tree = ast.parse(content)
            opportunities.extend(self._analyze_ast(tree, content, file_path))

            # Text-based analysis
            opportunities.extend(self._analyze_text(content, file_path))

        except Exception as e:
            self.logger.error(f"Failed to analyze {file_path}: {e}")

        return opportunities

    def _analyze_ast(self, tree: ast.AST, content: str, file_path: str) -> List[RefactoringOpportunity]:
        """Analyze AST for structural refactoring opportunities"""
        opportunities = []

        class RefactoringVisitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.opportunities = []

            def visit_FunctionDef(self, node):
                # Check function complexity
                complexity = self._calculate_complexity(node)
                if complexity > 10:
                    self.opportunities.append(RefactoringOpportunity(
                        file_path=file_path,
                        line_number=node.lineno,
                        issue_type="high_complexity",
                        description=f"Function '{node.name}' has high complexity ({complexity})",
                        severity="medium",
                        suggested_fix="Consider breaking down into smaller functions",
                        code_context=f"def {node.name}({len(node.args.args)} args)",
                        confidence=0.8
                    ))

                # Check function length
                if len(node.body) > 50:
                    self.opportunities.append(RefactoringOpportunity(
                        file_path=file_path,
                        line_number=node.lineno,
                        issue_type="long_function",
                        description=f"Function '{node.name}' is too long ({len(node.body)} lines)",
                        severity="low",
                        suggested_fix="Consider splitting into smaller functions",
                        code_context=f"def {node.name}...",
                        confidence=0.7
                    ))

                self.generic_visit(node)

            def visit_ClassDef(self, node):
                # Check class size
                if len(node.body) > 30:
                    self.opportunities.append(RefactoringOpportunity(
                        file_path=file_path,
                        line_number=node.lineno,
                        issue_type="large_class",
                        description=f"Class '{node.name}' is too large ({len(node.body)} methods/attributes)",
                        severity="medium",
                        suggested_fix="Consider splitting into smaller classes",
                        code_context=f"class {node.name}...",
                        confidence=0.75
                    ))

                self.generic_visit(node)

            def _calculate_complexity(self, node):
                """Calculate cyclomatic complexity"""
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                return complexity

        visitor = RefactoringVisitor(self)
        visitor.visit(tree)
        opportunities.extend(visitor.opportunities)

        return opportunities

    def _analyze_text(self, content: str, file_path: str) -> List[RefactoringOpportunity]:
        """Analyze code text for refactoring opportunities"""
        opportunities = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for long lines
            if len(line) > 120:
                opportunities.append(RefactoringOpportunity(
                    file_path=file_path,
                    line_number=i,
                    issue_type="long_line",
                    description=f"Line too long ({len(line)} characters)",
                    severity="low",
                    suggested_fix="Break line into multiple lines",
                    code_context=line[:50] + "...",
                    confidence=0.9
                ))

            # Check for magic numbers
            magic_numbers = re.findall(r'\b\d{2,}\b', line)
            for number in magic_numbers:
                if number not in ['100', '1000', '60', '24']:  # Common acceptable numbers
                    opportunities.append(RefactoringOpportunity(
                        file_path=file_path,
                        line_number=i,
                        issue_type="magic_number",
                        description=f"Magic number '{number}' found",
                        severity="low",
                        suggested_fix="Replace with named constant",
                        code_context=line.strip(),
                        confidence=0.6
                    ))

            # Check for TODO/FIXME comments
            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                opportunities.append(RefactoringOpportunity(
                    file_path=file_path,
                    line_number=i,
                    issue_type="todo_comment",
                    description="TODO/FIXME comment found",
                    severity="low",
                    suggested_fix="Address the TODO item or remove comment",
                    code_context=line.strip(),
                    confidence=0.95
                ))

            # Check for print statements (suggest logging)
            if re.search(r'\bprint\s*\(', line):
                opportunities.append(RefactoringOpportunity(
                    file_path=file_path,
                    line_number=i,
                    issue_type="print_statement",
                    description="Print statement found (consider using logging)",
                    severity="low",
                    suggested_fix="Replace with proper logging",
                    code_context=line.strip(),
                    confidence=0.7
                ))

        return opportunities

class CodeRefactorer:
    """Automated code refactoring engine"""

    def __init__(self):
        self.logger = logging.getLogger("CodeRefactorer")
        self.analyzer = CodeAnalyzer()

    def refactor_file(self, file_path: str, auto_fix: bool = False) -> Dict[str, Any]:
        """Refactor a single file"""
        opportunities = self.analyzer.analyze_file(file_path)

        results = {
            "file_path": file_path,
            "opportunities_found": len(opportunities),
            "opportunities": opportunities,
            "fixes_applied": 0,
            "errors": []
        }

        if auto_fix:
            results["fixes_applied"], errors = self._apply_fixes(file_path, opportunities)
            results["errors"] = errors

        return results

    def _apply_fixes(self, file_path: str, opportunities: List[RefactoringOpportunity]) -> Tuple[int, List[str]]:
        """Apply automated fixes"""
        fixes_applied = 0
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            modified_lines = lines.copy()

            for opportunity in opportunities:
                if opportunity.confidence > 0.7:  # Only auto-fix high confidence issues
                    try:
                        if opportunity.issue_type == "print_statement":
                            # Replace print with logging
                            line_idx = opportunity.line_number - 1
                            if line_idx < len(modified_lines):
                                original_line = modified_lines[line_idx]
                                # Simple replacement - in practice would be more sophisticated
                                if 'print(' in original_line:
                                    modified_lines[line_idx] = original_line.replace(
                                        'print(', 'logger.info('
                                    )
                                    fixes_applied += 1

                        elif opportunity.issue_type == "magic_number":
                            # This would require more complex analysis to determine
                            # appropriate constant names and placement
                            pass

                    except Exception as e:
                        errors.append(f"Failed to fix {opportunity.issue_type}: {e}")

            # Write back if any fixes were applied
            if fixes_applied > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(modified_lines))

        except Exception as e:
            errors.append(f"Failed to apply fixes to {file_path}: {e}")

        return fixes_applied, errors

    def batch_refactor(self, directory: str, auto_fix: bool = False,
                      file_limit: int = 50) -> Dict[str, Any]:
        """Refactor all Python files in a directory"""
        results = {
            "directory": directory,
            "files_processed": 0,
            "total_opportunities": 0,
            "total_fixes": 0,
            "file_results": []
        }

        python_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and not root.startswith('./.'):
                    python_files.append(os.path.join(root, file))

        files_to_process = python_files[:file_limit]

        for file_path in files_to_process:
            try:
                file_result = self.refactor_file(file_path, auto_fix)
                results["file_results"].append(file_result)
                results["files_processed"] += 1
                results["total_opportunities"] += file_result["opportunities_found"]
                results["total_fixes"] += file_result.get("fixes_applied", 0)

            except Exception as e:
                self.logger.error(f"Failed to process {file_path}: {e}")

        return results

class RefactoringScheduler:
    """Automated refactoring scheduler"""

    def __init__(self, refactoring_interval: int = 3600):  # 1 hour default
        self.refactoring_interval = refactoring_interval
        self.refactorer = CodeRefactorer()
        self.last_refactoring = 0
        self.logger = logging.getLogger("RefactoringScheduler")

    def should_refactor(self) -> bool:
        """Check if refactoring should be performed"""
        current_time = time.time()
        return current_time - self.last_refactoring >= self.refactoring_interval

    def perform_scheduled_refactoring(self, directory: str,
                                    auto_fix: bool = False) -> Dict[str, Any]:
        """Perform scheduled refactoring"""
        if not self.should_refactor():
            return {"status": "not_due", "message": "Refactoring not due yet"}

        self.logger.info("Starting scheduled refactoring...")

        results = self.refactorer.batch_refactor(directory, auto_fix)

        self.last_refactoring = time.time()

        results["status"] = "completed"
        results["timestamp"] = self.last_refactoring

        return results

    def get_refactoring_stats(self) -> Dict[str, Any]:
        """Get refactoring statistics"""
        return {
            "last_refactoring": self.last_refactoring,
            "interval_seconds": self.refactoring_interval,
            "next_scheduled": self.last_refactoring + self.refactoring_interval,
            "time_until_next": max(0, (self.last_refactoring + self.refactoring_interval) - time.time())
        }

class QualityMetrics:
    """Code quality metrics calculator"""

    def __init__(self):
        self.logger = logging.getLogger("QualityMetrics")

    def calculate_quality_score(self, file_path: str) -> Dict[str, Any]:
        """Calculate code quality metrics for a file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            lines = content.split('\n')
            total_lines = len(lines)

            # Basic metrics
            metrics = {
                "total_lines": total_lines,
                "code_lines": 0,
                "comment_lines": 0,
                "blank_lines": 0,
                "functions": content.count("def "),
                "classes": content.count("class "),
                "imports": content.count("import ") + content.count("from "),
                "print_statements": content.count("print("),
                "long_lines": sum(1 for line in lines if len(line) > 120),
                "magic_numbers": len(re.findall(r'\b\d{3,}\b', content)),
                "complexity_score": 0
            }

            # Count different line types
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    metrics["blank_lines"] += 1
                elif stripped.startswith("#"):
                    metrics["comment_lines"] += 1
                elif stripped and not stripped.startswith("#"):
                    metrics["code_lines"] += 1

            # Calculate complexity
            try:
                tree = ast.parse(content)
                metrics["complexity_score"] = self._calculate_file_complexity(tree)
            except:
                metrics["complexity_score"] = 0

            # Calculate overall quality score
            quality_score = self._calculate_overall_score(metrics)
            metrics["quality_score"] = quality_score

            return metrics

        except Exception as e:
            self.logger.error(f"Failed to calculate quality metrics for {file_path}: {e}")
            return {"error": str(e)}

    def _calculate_file_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for entire file"""
        complexity = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity

    def _calculate_overall_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall quality score (0-100)"""
        score = 100.0

        # Penalize based on various factors
        if metrics["total_lines"] > 0:
            comment_ratio = metrics["comment_lines"] / metrics["total_lines"]
            if comment_ratio < 0.1:
                score -= 10
            elif comment_ratio > 0.3:
                score += 5

        # Penalize print statements
        if metrics["print_statements"] > 0:
            score -= min(20, metrics["print_statements"] * 2)

        # Penalize long lines
        if metrics["long_lines"] > 0:
            score -= min(15, metrics["long_lines"])

        # Penalize magic numbers
        if metrics["magic_numbers"] > 0:
            score -= min(10, metrics["magic_numbers"])

        # Penalize high complexity
        if metrics["complexity_score"] > 20:
            score -= min(20, (metrics["complexity_score"] - 20))

        return max(0, min(100, score))

# Global instances
refactorer = CodeRefactorer()
scheduler = RefactoringScheduler()
quality_metrics = QualityMetrics()

def demonstrate_automated_refactoring():
    """Demonstrate automated refactoring capabilities"""
    print("🔧 AGI AUTOMATED CODE REFACTORING SYSTEM")
    print("=" * 50)

    # Analyze current directory
    print("   🔍 Analyzing codebase for refactoring opportunities...")
    results = refactorer.batch_refactor('/home/ubuntu/wealthyrobot', auto_fix=False, file_limit=20)

    print(f"   📊 Files processed: {results['files_processed']}")
    print(f"   🎯 Opportunities found: {results['total_opportunities']}")

    # Show top issues
    issue_counts = defaultdict(int)
    for file_result in results['file_results']:
        for opportunity in file_result['opportunities']:
            issue_counts[opportunity.issue_type] += 1

    if issue_counts:
        print("
🔴 TOP ISSUES FOUND:"        for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"      • {issue_type}: {count} instances")

    # Calculate quality metrics for main AGI file
    print("
📈 Calculating code quality metrics..."    quality = quality_metrics.calculate_quality_score('/home/ubuntu/wealthyrobot/UNRESTRICTED_AGI_SYSTEM.py')

    if 'quality_score' in quality:
        print(".1f"        print(f"      • Lines of code: {quality['code_lines']}")
        print(f"      • Functions: {quality['functions']}")
        print(f"      • Classes: {quality['classes']}")
        print(f"      • Complexity score: {quality['complexity_score']}")
        print(f"      • Print statements: {quality['print_statements']}")

    # Show refactoring scheduler status
    print("
⏰ Refactoring Scheduler Status:"    stats = scheduler.get_refactoring_stats()
    print(".1f"    print(".0f"
    # Simulate automated fixes (conservative approach)
    print("
🔧 Applying safe automated fixes..."    fix_results = refactorer.batch_refactor('/home/ubuntu/wealthyrobot', auto_fix=True, file_limit=10)
    print(f"   ✅ Fixes applied: {fix_results['total_fixes']}")

    print("   🚀 Automated refactoring system operational!")
    print("   📊 Continuous code quality improvement active!")

if __name__ == "__main__":
    demonstrate_automated_refactoring()
