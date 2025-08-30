
#!/usr/bin/env python3
"""
Optimized File I/O Patterns for Better Performance
"""

import os
import json
import mmap
import tempfile
from typing import Iterator, List, Dict, Any
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor

class OptimizedFileIO:
    def __init__(self, buffer_size=8192, max_workers=4):
        self.buffer_size = buffer_size
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def memory_mapped_read(self, file_path: str) -> str:
        """Read file using memory mapping for large files"""
        with open(file_path, 'r') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                return mm.read().decode('utf-8', errors='ignore')

    def buffered_json_reader(self, file_path: str, chunk_size: int = 1000) -> Iterator[List[Dict]]:
        """Read large JSON files in buffered chunks"""
        with open(file_path, 'r') as f:
            buffer = []
            for line in f:
                try:
                    item = json.loads(line.strip())
                    buffer.append(item)

                    if len(buffer) >= chunk_size:
                        yield buffer
                        buffer = []
                except json.JSONDecodeError:
                    continue

            if buffer:
                yield buffer

    def parallel_file_processor(self, file_paths: List[str], processor_func, max_workers: int = 4):
        """Process multiple files in parallel"""
        def process_file(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                return processor_func(data)
            except Exception as e:
                return {"error": str(e), "file": file_path}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(process_file, file_paths))

        return results

    def write_with_buffering(self, file_path: str, data: List[Dict], buffer_size: int = 1000):
        """Write data with output buffering for better performance"""
        with open(file_path, 'w') as f:
            buffer = []

            for item in data:
                buffer.append(json.dumps(item))

                if len(buffer) >= buffer_size:
                    f.write('\n'.join(buffer) + '\n')
                    buffer = []

            if buffer:
                f.write('\n'.join(buffer) + '\n')

    def create_temp_buffered_writer(self, final_path: str):
        """Create a temporary buffered writer for large data sets"""
        temp_fd, temp_path = tempfile.mkstemp(suffix='.json')

        def write_data(data):
            with os.fdopen(temp_fd, 'w') as f:
                if isinstance(data, list):
                    self.write_with_buffering(temp_path, data)
                else:
                    json.dump(data, f, indent=2)

        def finalize():
            # Atomic move to final location
            os.rename(temp_path, final_path)

        return write_data, finalize

# Global optimized file I/O instance
optimized_io = OptimizedFileIO()

def smart_file_reader(file_path: str):
    """Smart file reader that chooses optimal method based on file size"""
    file_size = os.path.getsize(file_path)

    if file_size > 100 * 1024 * 1024:  # > 100MB
        # Use memory mapping for very large files
        return optimized_io.memory_mapped_read(file_path)
    elif file_size > 10 * 1024 * 1024:  # > 10MB
        # Use buffered reading for large files
        content = ""
        with open(file_path, 'r') as f:
            while True:
                chunk = f.read(optimized_io.buffer_size)
                if not chunk:
                    break
                content += chunk
        return content
    else:
        # Standard reading for smaller files
        with open(file_path, 'r') as f:
            return f.read()
