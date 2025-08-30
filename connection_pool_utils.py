
#!/usr/bin/env python3
"""
Connection Pooling Utilities for Network Optimization
"""

import aiohttp
import asyncio
import time
from typing import Dict, List, Any, Optional
from urllib3.util.retry import Retry
import urllib3

class ConnectionPoolManager:
    def __init__(self, max_connections=100, max_keepalive=30):
        self.max_connections = max_connections
        self.max_keepalive = max_keepalive
        self.pools = {}
        self.session = None

    def get_http_pool(self, base_url: str):
        """Get or create HTTP pool for a base URL"""
        if base_url not in self.pools:
            retry_strategy = Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=[429, 500, 502, 503, 504],
            )

            self.pools[base_url] = urllib3.PoolManager(
                num_pools=5,
                maxsize=self.max_connections,
                block=False,
                retries=retry_strategy
            )

        return self.pools[base_url]

    async def get_async_session(self):
        """Get async HTTP session with connection pooling"""
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(
                limit=self.max_connections,
                limit_per_host=10,
                ttl_dns_cache=300,
                use_dns_cache=True,
                keepalive_timeout=self.max_keepalive,
                enable_cleanup_closed=True
            )

            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )

        return self.session

    async def make_pooled_request(self, method: str, url: str, **kwargs):
        """Make a request using the connection pool"""
        session = await self.get_async_session()

        try:
            async with session.request(method, url, **kwargs) as response:
                return {
                    'status': response.status,
                    'headers': dict(response.headers),
                    'data': await response.text()
                }
        except Exception as e:
            return {'error': str(e)}

    def cleanup(self):
        """Clean up connection pools"""
        for pool in self.pools.values():
            pool.clear()

        if self.session and not self.session.closed:
            asyncio.create_task(self.session.close())

# Global connection pool manager
connection_manager = ConnectionPoolManager()

async def optimized_http_request(method: str, url: str, **kwargs):
    """Make an optimized HTTP request using connection pooling"""
    return await connection_manager.make_pooled_request(method, url, **kwargs)
