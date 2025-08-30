#!/usr/bin/env python3
import os
import requests
from typing import List, Dict, Any


def fetch_top_assets(limit: int = 50) -> List[Dict[str, Any]]:
    """Fetch a list of Algorand ASAs from the Indexer REST API (first page only).
    Returns a list of asset dicts with id, params.
    """
    base = os.getenv('INDEXER_ADDRESS', 'https://mainnet-idx.algonode.cloud')
    token = os.getenv('INDEXER_TOKEN', '')
    headers = {'User-Agent': 'WealthyRobot/1.0'}
    if token:
        headers['X-API-Key'] = token
    url = base.rstrip('/') + f"/v2/assets?limit={int(max(1, min(limit, 100)))}"
    try:
        resp = requests.get(url, timeout=15, headers=headers)
        if resp.status_code != 200:
            return []
        data = resp.json() or {}
        return data.get('assets', []) or []
    except Exception:
        return []


if __name__ == '__main__':
    assets = fetch_top_assets()
    print(f"Fetched {len(assets)} assets")


