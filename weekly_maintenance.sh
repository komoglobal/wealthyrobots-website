#!/bin/bash
# Weekly space/performance maintenance
set -euo pipefail
cd /home/ubuntu/wealthyrobot

# 1) Run data management and optimizer agents
python3 data_management_agent.py || true
python3 optimizer_agent.py || true

# 2) Archive likely-unused backups/variants and zero-size test files
TS=$(date +%Y%m%d_%H%M%S)
OUT="archive/unused_code_${TS}.tar.gz"
mkdir -p archive
TMP_LIST=$(mktemp)
find . -type f \
  -not -path "./archive/*" -not -path "./.venv/*" -not -path "./logs/*" -not -path "./tiktok_system_env/*" -not -path "./__pycache__/*" \
  \( -iname "*backup*" -o -name "*.BACKUP" -o -name "*.INTEGRATED" -o -name "*.pre_*_backup" -o -name "*.pre_*" \) \
  -printf "%p\n" >> "$TMP_LIST"
find ./claude_blackbox_tests/sandbox -type f -name "*.py" -size 0 -printf "%p\n" 2>/dev/null >> "$TMP_LIST" || true
sort -u "$TMP_LIST" -o "$TMP_LIST"
if [ -s "$TMP_LIST" ]; then
  tar -czf "$OUT" -T "$TMP_LIST" && xargs -a "$TMP_LIST" -r rm -f || true
fi
rm -f "$TMP_LIST"

# 3) Compress any uncompressed archive directories
for d in archive/*; do
  [ -d "$d" ] || continue
  base=$(basename "$d")
  out="archive/${base}.tar.gz"
  if [ ! -f "$out" ]; then
    tar -C archive -czf "$out" "$base" && rm -rf "$d" || true
  fi
done

# 4) Report disk space
printf "[weekly_maintenance] %s disk:\n" "$(date -Is)"
df -h | sed -n "1,2p"

