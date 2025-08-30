
#!/usr/bin/env python3
"""
Request Batching Utilities for Network Optimization
"""

import asyncio
import aiohttp
import json
import time
from typing import List, Dict, Any, Callable
from collections import defaultdict
import threading

class RequestBatcher:
    def __init__(self, batch_size=50, batch_timeout=1.0):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.request_queue = defaultdict(list)
        self.response_handlers = {}
        self.processing_thread = None
        self.running = False

    def start(self):
        """Start the batching processor"""
        self.running = True
        self.processing_thread = threading.Thread(target=self._process_batches)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def stop(self):
        """Stop the batching processor"""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join()

    def add_request(self, endpoint: str, data: Dict[str, Any], callback: Callable = None):
        """Add a request to the batch queue"""
        request_id = f"{endpoint}_{time.time()}_{id(data)}"

        self.request_queue[endpoint].append({
            'id': request_id,
            'data': data,
            'timestamp': time.time()
        })

        if callback:
            self.response_handlers[request_id] = callback

        return request_id

    def _process_batches(self):
        """Process batched requests"""
        while self.running:
            try:
                current_time = time.time()

                # Process each endpoint's batch
                for endpoint, requests in list(self.request_queue.items()):
                    # Check batch size or timeout
                    if (len(requests) >= self.batch_size or
                        (requests and current_time - requests[0]['timestamp'] >= self.batch_timeout)):

                        batch = requests[:self.batch_size]
                        self.request_queue[endpoint] = requests[self.batch_size:]

                        # Process batch
                        asyncio.run(self._execute_batch(endpoint, batch))

                time.sleep(0.1)  # Prevent busy waiting

            except Exception as e:
                print(f"Batch processing error: {e}")
                time.sleep(1)

    async def _execute_batch(self, endpoint: str, batch: List[Dict[str, Any]]):
        """Execute a batch of requests"""
        try:
            # Here you would implement the actual batch processing logic
            # For now, we'll simulate processing

            batch_ids = [req['id'] for req in batch]
            batch_data = [req['data'] for req in batch]

            # Simulate batch processing
            await asyncio.sleep(0.1)  # Simulate network delay

            # Simulate responses
            responses = [{"status": "success", "id": req_id} for req_id in batch_ids]

            # Call response handlers
            for i, response in enumerate(responses):
                request_id = batch_ids[i]
                if request_id in self.response_handlers:
                    try:
                        self.response_handlers[request_id](response)
                    except Exception as e:
                        print(f"Response handler error: {e}")
                    finally:
                        del self.response_handlers[request_id]

        except Exception as e:
            print(f"Batch execution error: {e}")

# Global request batcher instance
request_batcher = RequestBatcher()

def batched_api_call(endpoint: str, data: Dict[str, Any], callback: Callable = None):
    """Make a batched API call"""
    return request_batcher.add_request(endpoint, data, callback)

# Example usage function
async def example_batch_processor():
    """Example of how to use the batch processor"""

    def response_handler(response):
        print(f"Received response: {response}")

    # Add multiple requests
    for i in range(10):
        batched_api_call(
            "https://api.example.com/data",
            {"request_id": i, "data": f"request_{i}"},
            response_handler
        )

    # Start processing
    request_batcher.start()

    # Wait a bit for processing
    await asyncio.sleep(2)

    # Stop processing
    request_batcher.stop()
