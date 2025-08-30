#!/usr/bin/env python3
"""
List likely-unused Python files in the repository.
Criteria:
- File extension: .py
- Not within: .venv/, tiktok_system_env/, archive/, logs/, __pycache__/
- Zero references (by basename) across the repo (excluding the file itself)
- Zero references in current user's crontab

Outputs top 50 entries, sorted by age (descending) then size (descending).
"""

import os
import subprocess
import shlex
from datetime import datetime
from typing import List, Tuple

EXCLUDE_DIRS = {'.venv', 'tiktok_system_env', 'archive', 'logs', '__pycache__'}
REPO_ROOT = os.path.abspath('.')


def iter_python_files(root: str) -> List[str]:
	files: List[str] = []
	for dirpath, dirnames, filenames in os.walk(root):
		# prune excluded dirs
		dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
		for name in filenames:
			if not name.endswith('.py'):
				continue
			files.append(os.path.join(dirpath, name))
	return files


def count_repo_refs(basename: str, this_path: str) -> int:
	# Use grep -R -F to count references excluding some dirs and excluding the file itself
	exclude_args = []
	for d in EXCLUDE_DIRS:
		exclude_args += ['--exclude-dir', d]
	cmd = ['grep', '-R', '-F', basename, '.', *exclude_args]
	try:
		res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, cwd=REPO_ROOT)
		if res.returncode not in (0, 1):
			return 0
		count = 0
		for line in res.stdout.splitlines():
			# line format: path:match
			if line.startswith('./'):
				path = line.split(':', 1)[0]
			else:
				path = line.split(':', 1)[0]
			# skip references that are the file itself
			# normalize both
			try:
				abs_line_path = os.path.abspath(os.path.join(REPO_ROOT, path))
				if os.path.samefile(abs_line_path, this_path):
					continue
			except Exception:
				pass
			count += 1
		return count
	except Exception:
		return 0


def count_cron_refs(basename: str) -> int:
	try:
		res = subprocess.run(['bash', '-lc', f"crontab -l 2>/dev/null | grep -F {shlex.quote(basename)} | wc -l"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
		return int(res.stdout.strip() or '0')
	except Exception:
		return 0


def human_age_days(mtime: float) -> int:
	return int((datetime.now().timestamp() - mtime) // 86400)


def main() -> None:
	files = iter_python_files(REPO_ROOT)
	candidates: List[Tuple[int, int, str]] = []  # (age_days, size_kb, relpath)
	for path in files:
		basename = os.path.basename(path)
		repo_refs = count_repo_refs(basename, path)
		cron_refs = count_cron_refs(basename)
		if repo_refs == 0 and cron_refs == 0:
			try:
				st = os.stat(path)
				age_days = human_age_days(st.st_mtime)
				size_kb = st.st_size // 1024
				rel = os.path.relpath(path, REPO_ROOT)
				candidates.append((age_days, size_kb, rel))
			except FileNotFoundError:
				continue
	# Sort by age desc, then size desc
	candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
	print("Likely-unused Python files (top 50):")
	for age, size, rel in candidates[:50]:
		print(f"age={age}d size={size}KB file={rel}")
	print(f"Total candidates: {len(candidates)}")


if __name__ == '__main__':
	main()

