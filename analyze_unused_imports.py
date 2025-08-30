#!/usr/bin/env python3
"""
Analyze Unused Imports Tool
===========================

This script analyzes Python files to identify unused imports and suggests removals.
"""

import os
import ast
import re
from typing import Dict, Set, List
from collections import defaultdict

class ImportAnalyzer:
    """Analyzes Python files for unused imports"""

    def __init__(self):
        self.results = {}

    def analyze_file(self, filepath: str) -> Dict:
        """Analyze a single Python file for unused imports"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Parse the AST
            tree = ast.parse(content)

            # Extract imports
            imports = self._extract_imports(tree)
            if not imports:
                return {'unused_imports': [], 'total_imports': 0}

            # Extract used names
            used_names = self._extract_used_names(tree, content)

            # Find unused imports
            unused_imports = []
            for import_info in imports:
                if not self._is_import_used(import_info, used_names):
                    unused_imports.append(import_info)

            return {
                'unused_imports': unused_imports,
                'total_imports': len(imports),
                'used_imports': len(imports) - len(unused_imports)
            }

        except Exception as e:
            return {'error': str(e), 'unused_imports': [], 'total_imports': 0}

    def _extract_imports(self, tree: ast.AST) -> List[Dict]:
        """Extract all import statements from AST"""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'asname': alias.asname,
                        'lineno': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        imports.append({
                            'type': 'from',
                            'module': node.module,
                            'name': alias.name,
                            'asname': alias.asname,
                            'lineno': node.lineno
                        })

        return imports

    def _extract_used_names(self, tree: ast.AST, content: str) -> Set[str]:
        """Extract all used names from the code"""
        used_names = set()

        # Walk through all nodes to find name usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, (ast.Load, ast.AugLoad)):
                    used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # Handle module.attribute patterns
                full_name = self._get_full_attribute_name(node)
                used_names.add(full_name)

        # Also check for string-based usage (like in getattr, hasattr, etc.)
        string_patterns = [
            r'getattr\([^,]+,\s*[\'"]([^\'"]+)[\'"]',
            r'hasattr\([^,]+,\s*[\'"]([^\'"]+)[\'"]',
            r'setattr\([^,]+,\s*[\'"]([^\'"]+)[\'"]',
            r'delattr\([^,]+,\s*[\'"]([^\'"]+)[\'"]'
        ]

        for pattern in string_patterns:
            matches = re.findall(pattern, content)
            used_names.update(matches)

        return used_names

    def _get_full_attribute_name(self, node: ast.Attribute) -> str:
        """Get the full name of an attribute access"""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_full_attribute_name(node.value)}.{node.attr}"
        else:
            return node.attr

    def _is_import_used(self, import_info: Dict, used_names: Set[str]) -> bool:
        """Check if an import is actually used"""
        if import_info['type'] == 'import':
            # Direct import: import module
            module_name = import_info['module']
            as_name = import_info['asname'] or module_name.split('.')[-1]

            # Check if the module name or as_name is used
            if as_name in used_names or module_name in used_names:
                return True

            # Check for submodule usage
            for used in used_names:
                if used.startswith(f"{as_name}."):
                    return True

        elif import_info['type'] == 'from':
            # From import: from module import name
            imported_name = import_info['asname'] or import_info['name']

            # Check if the imported name is used
            if imported_name in used_names:
                return True

            # Check for qualified usage
            for used in used_names:
                if used == f"{import_info['module']}.{import_info['name']}":
                    return True

        return False

    def analyze_directory(self, directory: str, file_limit: int = 50) -> Dict:
        """Analyze all Python files in a directory"""
        results = {}
        python_files = []

        # Find all Python files
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and not root.startswith('./.'):
                    python_files.append(os.path.join(root, file))

        # Limit analysis for performance
        files_to_analyze = python_files[:file_limit]
        total_unused = 0

        print(f"🔍 Analyzing {len(files_to_analyze)} Python files for unused imports...")

        for filepath in files_to_analyze:
            result = self.analyze_file(filepath)
            if 'error' not in result:
                results[filepath] = result
                total_unused += len(result['unused_imports'])

                if result['unused_imports']:
                    print(f"📄 {os.path.basename(filepath)}: {len(result['unused_imports'])} unused imports")
            else:
                print(f"⚠️  Error analyzing {filepath}: {result['error']}")

        return {
            'files_analyzed': len(results),
            'total_unused_imports': total_unused,
            'results': results
        }

def main():
    """Main analysis function"""
    analyzer = ImportAnalyzer()

    # Analyze the main directory
    results = analyzer.analyze_directory('/home/ubuntu/wealthyrobot', file_limit=100)

    print(f"\n📊 UNUSED IMPORTS ANALYSIS COMPLETE")
    print(f"=" * 50)
    print(f"Files Analyzed: {results['files_analyzed']}")
    print(f"Total Unused Imports: {results['total_unused_imports']}")

    # Show top offenders
    file_unused_counts = {}
    for filepath, result in results['results'].items():
        if result['unused_imports']:
            file_unused_counts[filepath] = len(result['unused_imports'])

    if file_unused_counts:
        print("\n🔴 TOP FILES WITH UNUSED IMPORTS:")
        sorted_files = sorted(file_unused_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        for filepath, count in sorted_files:
            print(f"  • {os.path.basename(filepath)}: {count} unused imports")

    return results

if __name__ == "__main__":
    main()
