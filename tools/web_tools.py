#!/usr/bin/env python3
"""
Simple Web Tools
Provides minimal web fetch and lightweight search utilities without external APIs.
"""

import re
import time
import html
from typing import List, Dict

import requests


class SimpleWebTools:
    def __init__(self, timeout_seconds: int = 10, user_agent: str = "WealthyRobotBot/1.0"):
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    def fetch_url(self, url: str) -> Dict[str, str]:
        """Fetch a URL and return basic metadata (status, title, content snippet)."""
        try:
            response = self.session.get(url, timeout=self.timeout_seconds)
            text = response.text or ""
            title_match = re.search(r"<title>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
            title = html.unescape(title_match.group(1).strip()) if title_match else ""
            snippet = html.unescape(re.sub(r"\s+", " ", text[:500]))
            return {
                "status": str(response.status_code),
                "title": title,
                "snippet": snippet,
                "url": url,
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "url": url}

    def search_duckduckgo(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """Very lightweight HTML scraping of DuckDuckGo results page (no API).
        Returns a list of {title, url} dicts. Best-effort only.
        """
        try:
            q = {"q": query, "t": "h_"}
            resp = self.session.get("https://duckduckgo.com/html/", params=q, timeout=self.timeout_seconds)
            html_text = resp.text
            # Extract result blocks: anchors inside <a class="result__a" ...>
            results: List[Dict[str, str]] = []
            for match in re.finditer(r"<a[^>]*class=\"result__a\"[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", html_text, flags=re.IGNORECASE | re.DOTALL):
                url = html.unescape(match.group(1))
                title = html.unescape(re.sub(r"<.*?>", "", match.group(2))).strip()
                if url and title:
                    results.append({"title": title, "url": url})
                if len(results) >= max(1, limit):
                    break
            return results
        except Exception:
            return []


def main():
    tools = SimpleWebTools()
    print("Testing fetch_url on example.com...")
    print(tools.fetch_url("https://example.com"))
    print("Testing search on 'WealthyRobot AI'...")
    print(tools.search_duckduckgo("WealthyRobot AI", limit=3))


if __name__ == "__main__":
    main()


