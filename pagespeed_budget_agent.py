#!/usr/bin/env python3
"""
PAGESPEED BUDGET AGENT
PURPOSE: Monitor Core Web Vitals against budgets (optional API)
CATEGORY: Performance
STATUS: Active (best-effort)
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime

class PageSpeedBudgetAgent:
    def __init__(self):
        self.api_key = os.environ.get("PAGESPEED_API_KEY")
        self.url = "https://wealthyrobots.com"
        self.strategy = "mobile"
        self.budgets = {
            "LCP": 2500,  # ms
            "CLS": 0.10,
            "INP": 200   # ms
        }

    def _fetch(self, page_path="/"):
        if not self.api_key:
            return {"skipped": True, "reason": "PAGESPEED_API_KEY not set"}
        api = (
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            f"?url={self.url}{page_path}&strategy={self.strategy}&category=PERFORMANCE&key={self.api_key}"
        )
        try:
            with urllib.request.urlopen(api, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8", errors="ignore"))
                return data
        except Exception as e:
            return {"error": str(e)}

    def _extract_vitals(self, data):
        try:
            audits = data["lighthouseResult"]["audits"]
            lcp = audits.get("largest-contentful-paint", {}).get("numericValue")
            cls = audits.get("cumulative-layout-shift", {}).get("numericValue")
            inp = audits.get("experimental-interaction-to-next-paint", {}).get("numericValue")
            return {"LCP": lcp, "CLS": cls, "INP": inp}
        except Exception:
            return {}

    def check_page(self, path="/"):
        data = self._fetch(path)
        if data.get("skipped") or data.get("error"):
            return {"path": path, **data}
        vitals = self._extract_vitals(data)
        verdicts = {}
        for k, v in vitals.items():
            if v is None:
                verdicts[k] = "unknown"
            else:
                limit = self.budgets[k]
                verdicts[k] = "pass" if (v <= limit if k != "CLS" else v <= limit) else "fail"
        return {"path": path, "vitals": vitals, "verdicts": verdicts}

    def run(self):
        pages = ["/", "/articles/", "/strategies/", "/tools/", "/resources/", "/about/", "/contact/"]
        results = [self.check_page(p) for p in pages]
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "url": self.url,
            "strategy": self.strategy,
            "results": results
        }
        name = f"pagespeed_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(name, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 PageSpeed report saved: {name}")
        return report

if __name__ == "__main__":
    PageSpeedBudgetAgent().run()
