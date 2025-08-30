#!/bin/bash
# Daily log rotation: compress large logs and truncate originals
set -euo pipefail
cd /home/ubuntu/wealthyrobot
mkdir -p logs/archive

# Rotate logs > 20MB
for f in logs/*; do
	[ -f "$f" ] || continue
	sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
	if [ "$sz" -gt $((20*1024*1024)) ]; then
		gz="logs/archive/$(basename "$f").$(date +%F).gz"
		gzip -c "$f" > "$gz" && : > "$f" || true
	fi
done

# Compress compliance_audit.jsonl if large (best-effort; may require root ownership)
if [ -f compliance_audit.jsonl ]; then
	sz=$(stat -c%s compliance_audit.jsonl 2>/dev/null || echo 0)
	if [ "$sz" -gt $((50*1024*1024)) ]; then
		gzip -c compliance_audit.jsonl > compliance_audit.jsonl.$(date +%F).gz 2>/dev/null || true
		: > compliance_audit.jsonl 2>/dev/null || true
	fi
fi

# Report
printf "[log_rotate] %s done.\n" "$(date -Is)"

