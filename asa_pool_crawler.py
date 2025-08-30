#!/usr/bin/env python3
import os
import json
import time
from typing import List, Dict, Any, Optional

import requests


def _indexer_headers() -> Dict[str, str]:
    headers = {'User-Agent': 'WealthyRobot/1.0'}
    token = os.getenv('INDEXER_TOKEN', '')
    if token:
        headers['X-API-Key'] = token
    return headers


def crawl_asas(max_pages: int = 2, page_limit: int = 100) -> List[Dict[str, Any]]:
    base = os.getenv('INDEXER_ADDRESS', 'https://mainnet-idx.algonode.cloud').rstrip('/')
    headers = _indexer_headers()
    next_token: Optional[str] = None
    assets: List[Dict[str, Any]] = []
    for _ in range(max_pages):
        url = f"{base}/v2/assets?limit={int(page_limit)}"
        if next_token:
            url += f"&next={next_token}"
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            if resp.status_code != 200:
                break
            data = resp.json() or {}
            assets.extend(data.get('assets', []) or [])
            next_token = data.get('next-token')
            if not next_token:
                break
        except Exception:
            break
    return assets


def crawl_pact_pools() -> List[Dict[str, Any]]:
    pools_data: List[Dict[str, Any]] = []
    try:
        from pactsdk import PactClient
        from algosdk.v2client import algod
        algod_client = algod.AlgodClient(os.getenv('ALGOD_TOKEN', ''), os.getenv('ALGOD_ADDRESS', 'https://mainnet-api.algonode.cloud'))
        pc = PactClient(algod_client, network='mainnet')
        pools = pc.list_pools()
        for p in pools:
            try:
                pools_data.append({
                    'pool_id': getattr(p, 'pool_id', None),
                    'asset1_id': int(getattr(p, 'asset1_id', getattr(p, 'asset_1_id', 0))),
                    'asset2_id': int(getattr(p, 'asset2_id', getattr(p, 'asset_2_id', 0))),
                    'asset1_reserves': float(getattr(p, 'asset1_reserves', getattr(p, 'asset_1_reserves', 0))),
                    'asset2_reserves': float(getattr(p, 'asset2_reserves', getattr(p, 'asset_2_reserves', 0))),
                })
            except Exception:
                continue
    except Exception:
        pass
    return pools_data


def crawl_tinyman_pools(candidate_assets: Optional[List[int]] = None) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    try:
        from tinyman.v2.client import TinymanV2MainnetClient
        from tinyman.v2.pools import get_pool_info
        from algosdk.v2client import algod
        algod_client = algod.AlgodClient(os.getenv('ALGOD_TOKEN', ''), os.getenv('ALGOD_ADDRESS', 'https://mainnet-api.algonode.cloud'))
        client = TinymanV2MainnetClient(algod_client)
        validator_app_id = client.validator_app_id
        if candidate_assets is None:
            candidate_assets = [0, 31566704, 312769, 386192725, 386195940]
        seen = set()
        for i, a in enumerate(candidate_assets):
            for b in candidate_assets[i + 1:]:
                key = tuple(sorted([a, b]))
                if key in seen:
                    continue
                seen.add(key)
                try:
                    pool = get_pool_info(algod_client, validator_app_id, key[0], key[1])
                    r1 = int(pool.get('asset_1_reserves', 0))
                    r2 = int(pool.get('asset_2_reserves', 0))
                    if r1 <= 0 or r2 <= 0:
                        continue
                    results.append({
                        'asset_1_id': key[0],
                        'asset_2_id': key[1],
                        'asset_1_reserves': r1,
                        'asset_2_reserves': r2,
                        'pool': pool,
                    })
                except Exception:
                    continue
    except Exception:
        pass
    return results


def main():
    os.makedirs('data/crawls', exist_ok=True)
    start = time.time()
    # Crawl ASAs (2 pages x 100 = up to 200 assets)
    asas = crawl_asas(max_pages=2, page_limit=100)
    with open('data/crawls/assets.json', 'w') as f:
        json.dump({'count': len(asas), 'assets': asas}, f)
    # Pact pools
    pact = crawl_pact_pools()
    with open('data/crawls/pact_pools.json', 'w') as f:
        json.dump({'count': len(pact), 'pools': pact}, f)
    # Tinyman pools (candidate set)
    tiny = crawl_tinyman_pools()
    with open('data/crawls/tinyman_pools.json', 'w') as f:
        json.dump({'count': len(tiny), 'pools': tiny}, f)
    print(f"Crawl done in {time.time()-start:.2f}s | assets={len(asas)} pact_pools={len(pact)} tinyman_pools={len(tiny)}")


if __name__ == '__main__':
    main()


