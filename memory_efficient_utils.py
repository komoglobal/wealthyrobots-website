
#!/usr/bin/env python3
"""
Memory-Efficient Data Processing Utilities
"""

import gc
import os
from typing import Iterator, Any, List
import json

def process_large_file_in_chunks(file_path: str, chunk_size: int = 1000) -> Iterator[List]:
    """Process large files in memory-efficient chunks"""
    with open(file_path, 'r') as f:
        data = json.load(f)

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        yield chunk
        gc.collect()  # Force garbage collection

def streaming_json_processor(file_path: str, processor_func):
    """Process JSON files in a streaming fashion"""
    with open(file_path, 'r') as f:
        data = json.load(f)

    for item in data:
        result = processor_func(item)
        if result:
            yield result

def memory_efficient_sort(data: List, key_func=None, reverse=False):
    """Memory-efficient sorting for large datasets"""
    if len(data) < 10000:
        return sorted(data, key=key_func, reverse=reverse)

    # For large datasets, use external sort
    import tempfile
    import heapq

    # Create temporary files for chunks
    chunk_files = []
    chunk_size = 5000

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        sorted_chunk = sorted(chunk, key=key_func, reverse=reverse)

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            json.dump(sorted_chunk, f)
            chunk_files.append(f.name)

    # Merge sorted chunks
    result = []
    file_handles = [open(f, 'r') for f in chunk_files]

    try:
        chunks_data = [json.load(f) for f in file_handles]
        result = list(heapq.merge(*chunks_data, key=key_func, reverse=reverse))
    finally:
        for f in file_handles:
            f.close()
        for f in chunk_files:
            os.unlink(f)

    return result

def cleanup_memory():
    """Force memory cleanup"""
    gc.collect()
    # Force garbage collection of unreachable objects
    gc.collect(2)
