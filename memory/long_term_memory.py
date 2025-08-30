#!/usr/bin/env python3
"""
Long-Term Memory (JSON-backed)
Simple append-only memory with tag/time retrieval for unified AGI cycles.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class LongTermMemory:
    def __init__(self, memory_file: str = "long_term_memory.json"):
        self.memory_file = memory_file
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'w') as fh:
                    json.dump({"entries": []}, fh)
            except Exception:
                pass

    def add(self, content: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "tags": tags or []
        }
        try:
            data = self._read()
            data["entries"].append(entry)
            with open(self.memory_file, 'w') as fh:
                json.dump(data, fh, indent=2)
        except Exception:
            pass

    def recall_by_tag(self, tag: str, limit: int = 20) -> List[Dict[str, Any]]:
        entries = self._read().get("entries", [])
        filtered = [e for e in entries if tag in (e.get("tags") or [])]
        return filtered[-limit:]

    def recall_recent(self, hours: int = 24, limit: int = 50) -> List[Dict[str, Any]]:
        entries = self._read().get("entries", [])
        try:
            cutoff = datetime.now() - timedelta(hours=hours)
            recent = [e for e in entries if datetime.fromisoformat(e.get("timestamp", "1970-01-01")) >= cutoff]
            return recent[-limit:]
        except Exception:
            return entries[-limit:]

    def _read(self) -> Dict[str, Any]:
        try:
            with open(self.memory_file, 'r') as fh:
                return json.load(fh)
        except Exception:
            return {"entries": []}


def main():
    mem = LongTermMemory()
    mem.add({"demo": "hello"}, tags=["demo"])
    print(mem.recall_by_tag("demo", limit=1))


if __name__ == "__main__":
    main()


