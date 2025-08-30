#!/usr/bin/env python3
"""
COMPETITOR WATCHER AGENT
PURPOSE: Track competitor pages for selected queries and produce gap hints
CATEGORY: SEO Intelligence
STATUS: Active (best-effort)
"""

import json
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime
import re

DEFAULT_CONFIG = {
  "queries": [
    {"q": "ai automation revenue strategies", "competitors": [
      "https://neilpatel.com/blog/",
      "https://backlinko.com/blog"
    ]}
  ]
}

class CompetitorWatcher:
    def __init__(self, config_path="competitor_watcher.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return DEFAULT_CONFIG

    def _fetch(self, url):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=20) as r:
                return r.read().decode('utf-8', errors='ignore')
        except (HTTPError, URLError) as e:
            return None

    def _extract_headings(self, html):
        headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', html, flags=re.IGNORECASE|re.DOTALL)
        cleaned = [re.sub('<[^<]+?>', '', h).strip() for h in headings]
        return [h for h in cleaned if h]

    def _word_count(self, html):
        text = re.sub('<[^<]+?>', ' ', html)
        words = re.findall(r'\w+', text)
        return len(words)

    def run(self):
        snapshots = []
        for item in self.config.get("queries", []):
            q = item.get("q")
            for url in item.get("competitors", []):
                html = self._fetch(url)
                if not html:
                    snapshots.append({"query": q, "url": url, "error": True})
                    continue
                snapshot = {
                    "query": q,
                    "url": url,
                    "word_count": self._word_count(html),
                    "headings": self._extract_headings(html)[:20]
                }
                snapshots.append(snapshot)
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "snapshots": snapshots
        }
        name = f"competitor_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(name, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Competitor report saved: {name}")
        return report

if __name__ == "__main__":
    CompetitorWatcher().run()
