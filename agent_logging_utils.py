#!/usr/bin/env python3
"""
Enhanced Logging Utilities for WealthyRobot Agents
Provides standardized logging, timeouts, and retry logic
"""

import os
import json
import time
import logging
import asyncio
import threading
from typing import Any, Dict, Optional, Callable
from functools import wraps
import subprocess
import requests
from datetime import datetime

class AgentLogger:
    """Enhanced logging for agents with structured output"""

    def __init__(self, name: str, log_level: str = "INFO"):
        self.name = name
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # File handler
        log_file = f"{self.log_dir}/{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s - %(name)s - %(message)s'
        ))
        self.logger.addHandler(console_handler)

    def info(self, message: str, **kwargs):
        """Log info message with optional structured data"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs)}"
        self.logger.info(message)

    def error(self, message: str, **kwargs):
        """Log error message with optional structured data"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs)}"
        self.logger.error(message)

    def warning(self, message: str, **kwargs):
        """Log warning message with optional structured data"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs)}"
        self.logger.warning(message)

    def debug(self, message: str, **kwargs):
        """Log debug message with optional structured data"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs)}"
        self.logger.debug(message)

def with_timeout(timeout_seconds: int = 30):
    """Thread-safe decorator to add timeout to functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=target, daemon=True)
            thread.start()
            thread.join(timeout_seconds)

            if thread.is_alive():
                raise TimeoutError(f"Function {func.__name__} timed out after {timeout_seconds}s")

            if exception[0]:
                raise exception[0]

            return result[0]
        return wrapper
    return decorator

def with_retry(max_retries: int = 3, backoff_factor: float = 2.0, base_delay: float = 1.0):
    """Decorator to add exponential backoff retry logic"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = kwargs.get('logger', AgentLogger(func.__name__))

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries", error=str(e))
                        raise

                    delay = base_delay * (backoff_factor ** attempt)
                    logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}), retrying in {delay:.2f}s", error=str(e))
                    time.sleep(delay)

            return None
        return wrapper
    return decorator

class AgentUtils:
    """Utility functions for agents"""

    @staticmethod
    @with_timeout(30)
    @with_retry(max_retries=3)
    def run_subprocess(cmd: list, logger: Optional[AgentLogger] = None, **kwargs) -> Dict[str, Any]:
        """Run subprocess with timeout and retry"""
        if logger is None:
            logger = AgentLogger("subprocess")

        logger.info("Running subprocess", command=' '.join(cmd))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                **kwargs
            )

            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }

        except subprocess.TimeoutExpired:
            logger.error("Subprocess timed out", command=' '.join(cmd))
            raise
        except Exception as e:
            logger.error("Subprocess failed", command=' '.join(cmd), error=str(e))
            raise

    @staticmethod
    @with_timeout(30)
    @with_retry(max_retries=3)
    def http_request(url: str, method: str = 'GET', logger: Optional[AgentLogger] = None, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with timeout and retry"""
        if logger is None:
            logger = AgentLogger("http_request")

        logger.info(f"Making {method} request", url=url)

        try:
            response = requests.request(method, url, timeout=30, **kwargs)

            return {
                'success': response.status_code < 400,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'json': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            }

        except requests.exceptions.Timeout:
            logger.error("HTTP request timed out", url=url)
            raise
        except Exception as e:
            logger.error("HTTP request failed", url=url, error=str(e))
            raise

    @staticmethod
    def save_json(data: Any, filepath: str, logger: Optional[AgentLogger] = None) -> bool:
        """Save data to JSON file with error handling"""
        if logger is None:
            logger = AgentLogger("json_save")

        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info("JSON saved successfully", filepath=filepath)
            return True
        except Exception as e:
            logger.error("Failed to save JSON", filepath=filepath, error=str(e))
            return False

    @staticmethod
    def load_json(filepath: str, logger: Optional[AgentLogger] = None) -> Optional[Any]:
        """Load data from JSON file with error handling"""
        if logger is None:
            logger = AgentLogger("json_load")

        try:
            if not os.path.exists(filepath):
                logger.warning("JSON file does not exist", filepath=filepath)
                return None

            with open(filepath, 'r') as f:
                data = json.load(f)
            logger.info("JSON loaded successfully", filepath=filepath)
            return data
        except Exception as e:
            logger.error("Failed to load JSON", filepath=filepath, error=str(e))
            return None
