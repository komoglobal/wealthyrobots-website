
#!/usr/bin/env python3
"""
Async I/O Utilities for Optimized File Operations
"""

import asyncio
import json
import os
from typing import List, Dict, Any, AsyncIterator
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import gzip
import bz2

class AsyncFileManager:
    def __init__(self, max_concurrent=10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)

    async def read_json_async(self, file_path: str) -> Dict[str, Any]:
        """Async JSON file reading"""
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(self.executor, self._read_json_sync, file_path)
            return content

    def _read_json_sync(self, file_path: str) -> Dict[str, Any]:
        """Synchronous JSON reading"""
        with open(file_path, 'r') as f:
            return json.load(f)

    async def write_json_async(self, file_path: str, data: Dict[str, Any]):
        """Async JSON file writing"""
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, self._write_json_sync, file_path, data)

    def _write_json_sync(self, file_path: str, data: Dict[str, Any]):
        """Synchronous JSON writing"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    async def read_large_file_async(self, file_path: str, chunk_size: int = 8192):
        """Async reading of large files in chunks"""
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.executor, self._read_large_file_sync, file_path, chunk_size)

    def _read_large_file_sync(self, file_path: str, chunk_size: int = 8192) -> str:
        """Synchronous large file reading"""
        content = ""
        with open(file_path, 'r') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                content += chunk
        return content

    async def batch_file_operations(self, operations: List[Dict[str, Any]]):
        """Batch multiple file operations asynchronously"""
        tasks = []

        for op in operations:
            if op['type'] == 'read_json':
                tasks.append(self.read_json_async(op['file_path']))
            elif op['type'] == 'write_json':
                tasks.append(self.write_json_async(op['file_path'], op['data']))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def compress_file_async(self, input_path: str, output_path: str, method: str = 'gzip'):
        """Async file compression"""
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, self._compress_file_sync, input_path, output_path, method)

    def _compress_file_sync(self, input_path: str, output_path: str, method: str = 'gzip'):
        """Synchronous file compression"""
        with open(input_path, 'rb') as f_in:
            data = f_in.read()

        if method == 'gzip':
            compressed = gzip.compress(data, compresslevel=6)
        elif method == 'bz2':
            compressed = bz2.compress(data, compresslevel=6)
        else:
            compressed = data

        with open(output_path, 'wb') as f_out:
            f_out.write(compressed)

# Global async file manager instance
async_file_manager = AsyncFileManager()

async def optimized_json_batch_processor(file_paths: List[str], processor_func):
    """Process multiple JSON files asynchronously with batching"""
    batch_size = 10
    results = []

    for i in range(0, len(file_paths), batch_size):
        batch = file_paths[i:i + batch_size]

        # Read batch asynchronously
        read_tasks = [async_file_manager.read_json_async(fp) for fp in batch]
        batch_data = await asyncio.gather(*read_tasks)

        # Process batch
        for data in batch_data:
            result = await processor_func(data)
            results.append(result)

    return results
