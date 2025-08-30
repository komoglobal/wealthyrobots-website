
#!/usr/bin/env python3
"""
Async Network Operations for Optimized Data Transfer
"""

import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Callable
import time

class AsyncNetworkManager:
    def __init__(self, max_concurrent=20, timeout=30):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=10,
            ttl_dns_cache=300,
            use_dns_cache=True,
            keepalive_timeout=30
        )
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_url(self, url: str, **kwargs) -> Dict[str, Any]:
        """Fetch URL with connection pooling and error handling"""
        async with self.semaphore:
            try:
                async with self.session.get(url, **kwargs) as response:
                    return {
                        'status': response.status,
                        'url': str(response.url),
                        'headers': dict(response.headers),
                        'data': await response.text(),
                        'elapsed': response.elapsed.total_seconds()
                    }
            except Exception as e:
                return {
                    'error': str(e),
                    'url': url,
                    'timestamp': time.time()
                }

    async def batch_fetch(self, urls: List[str], **kwargs) -> List[Dict[str, Any]]:
        """Fetch multiple URLs concurrently"""
        tasks = [self.fetch_url(url, **kwargs) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions in results
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({'error': str(result)})
            else:
                processed_results.append(result)

        return processed_results

    async def post_json_batch(self, url: str, data_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Post batch of JSON data concurrently"""
        async with self.semaphore:
            tasks = []
            for data in data_batch:
                tasks.append(self.session.post(url, json=data))

            responses = await asyncio.gather(*tasks, return_exceptions=True)

            results = []
            for response in responses:
                if isinstance(response, Exception):
                    results.append({'error': str(response)})
                else:
                    result = {
                        'status': response.status,
                        'data': await response.text()
                    }
                    results.append(result)

            return results

async def optimized_batch_download(urls: List[str], max_concurrent: int = 20) -> List[Dict[str, Any]]:
    """Optimized batch download of multiple URLs"""
    async with AsyncNetworkManager(max_concurrent=max_concurrent) as manager:
        return await manager.batch_fetch(urls)

async def example_usage():
    """Example of optimized network operations"""
    urls = [
        "https://api.github.com/user",
        "https://api.github.com/repos/octocat/Hello-World",
        "https://httpbin.org/get"
    ]

    print("Starting optimized batch download...")
    start_time = time.time()

    async with AsyncNetworkManager() as manager:
        results = await manager.batch_fetch(urls)

    end_time = time.time()

    print(f"Downloaded {len(results)} URLs in {end_time - start_time:.2f} seconds")
    successful = len([r for r in results if 'error' not in r])
    print(f"Successful requests: {successful}/{len(results)}")

    return results
