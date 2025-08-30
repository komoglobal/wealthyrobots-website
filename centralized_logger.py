#!/usr/bin/env python3
"""
Centralized Logging System - WealthyRobot Empire
Provides unified logging across all agents with structured output and multiple destinations
"""

import os
import json
import logging
import logging.handlers
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import threading
import queue
import time

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    AGENT_ACTIVITY = "agent_activity"
    TRADING = "trading"
    WEBSITE = "website"
    CONTENT = "content"
    SYSTEM = "system"
    ERROR = "error"
    PERFORMANCE = "performance"

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: datetime
    level: LogLevel
    category: LogCategory
    agent_name: str
    message: str
    data: Dict[str, Any]
    error_details: Optional[Dict[str, Any]] = None

class CentralizedLogger:
    """Centralized logging system for all WealthyRobot agents"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self.log_queue = queue.Queue()
        self.is_running = False
        self.worker_thread = None

        # Configuration
        self.log_dir = "logs"
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.backup_count = 5
        self.flush_interval = 5  # seconds

        # Setup directories
        self._setup_directories()

        # Setup handlers
        self._setup_handlers()

        # Start background worker
        self._start_worker()

    def _setup_directories(self):
        """Setup logging directories"""
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(os.path.join(self.log_dir, "daily"), exist_ok=True)
        os.makedirs(os.path.join(self.log_dir, "agents"), exist_ok=True)
        os.makedirs(os.path.join(self.log_dir, "errors"), exist_ok=True)

    def _setup_handlers(self):
        """Setup logging handlers"""
        # Clear any existing handlers
        logging.getLogger().handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        json_formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
        )

        # File handler for all logs
        all_logs_file = os.path.join(self.log_dir, "wealthyrobot.log")
        file_handler = logging.handlers.RotatingFileHandler(
            all_logs_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        file_handler.setFormatter(detailed_formatter)

        # Daily log file
        daily_file = os.path.join(
            self.log_dir,
            "daily",
            f"wealthyrobot_{datetime.now().strftime('%Y%m%d')}.log"
        )
        daily_handler = logging.handlers.RotatingFileHandler(
            daily_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        daily_handler.setFormatter(detailed_formatter)

        # Error log file
        error_file = os.path.join(self.log_dir, "errors.log")
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(detailed_formatter)

        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(daily_handler)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(console_handler)

    def _start_worker(self):
        """Start background logging worker"""
        if self.is_running:
            return

        self.is_running = True
        self.worker_thread = threading.Thread(target=self._log_worker, daemon=True)
        self.worker_thread.start()

    def _log_worker(self):
        """Background worker to process log entries"""
        while self.is_running:
            try:
                # Process all pending log entries
                while not self.log_queue.empty():
                    log_entry = self.log_queue.get_nowait()
                    self._write_structured_log(log_entry)

                # Sleep before next iteration
                time.sleep(self.flush_interval)

            except Exception as e:
                print(f"❌ Logging worker error: {e}")

    def _write_structured_log(self, log_entry: LogEntry):
        """Write structured log entry to file"""
        try:
            # Create structured log file
            log_data = {
                "timestamp": log_entry.timestamp.isoformat(),
                "level": log_entry.level.value,
                "category": log_entry.category.value,
                "agent_name": log_entry.agent_name,
                "message": log_entry.message,
                "data": log_entry.data
            }

            if log_entry.error_details:
                log_data["error_details"] = log_entry.error_details

            # Write to agent-specific log
            agent_log_file = os.path.join(
                self.log_dir,
                "agents",
                f"{log_entry.agent_name}.log"
            )

            with open(agent_log_file, 'a') as f:
                f.write(json.dumps(log_data) + '\n')

            # Write to category-specific log
            category_log_file = os.path.join(
                self.log_dir,
                f"{log_entry.category.value}.log"
            )

            with open(category_log_file, 'a') as f:
                f.write(json.dumps(log_data) + '\n')

        except Exception as e:
            print(f"❌ Error writing structured log: {e}")

    def log(self, level: LogLevel, category: LogCategory, agent_name: str,
            message: str, data: Dict[str, Any] = None, error_details: Dict[str, Any] = None):
        """Log a message with structured data"""
        if data is None:
            data = {}

        log_entry = LogEntry(
            timestamp=datetime.now(),
            level=level,
            category=category,
            agent_name=agent_name,
            message=message,
            data=data,
            error_details=error_details
        )

        # Add to queue for background processing
        self.log_queue.put(log_entry)

        # Also log to standard Python logging
        logger = logging.getLogger(agent_name)
        log_method = getattr(logger, level.value.lower())

        formatted_message = f"[{category.value}] {message}"
        if data:
            formatted_message += f" | Data: {data}"

        log_method(formatted_message)

    def log_agent_activity(self, agent_name: str, action: str, details: Dict[str, Any] = None):
        """Log agent activity"""
        self.log(
            LogLevel.INFO,
            LogCategory.AGENT_ACTIVITY,
            agent_name,
            f"Agent activity: {action}",
            details or {}
        )

    def log_trading_activity(self, agent_name: str, action: str, details: Dict[str, Any] = None):
        """Log trading activity"""
        self.log(
            LogLevel.INFO,
            LogCategory.TRADING,
            agent_name,
            f"Trading activity: {action}",
            details or {}
        )

    def log_website_activity(self, agent_name: str, action: str, details: Dict[str, Any] = None):
        """Log website activity"""
        self.log(
            LogLevel.INFO,
            LogCategory.WEBSITE,
            agent_name,
            f"Website activity: {action}",
            details or {}
        )

    def log_content_activity(self, agent_name: str, action: str, details: Dict[str, Any] = None):
        """Log content activity"""
        self.log(
            LogLevel.INFO,
            LogCategory.CONTENT,
            agent_name,
            f"Content activity: {action}",
            details or {}
        )

    def log_performance(self, agent_name: str, metric: str, value: Any, details: Dict[str, Any] = None):
        """Log performance metrics"""
        self.log(
            LogLevel.INFO,
            LogCategory.PERFORMANCE,
            agent_name,
            f"Performance metric: {metric} = {value}",
            details or {"metric": metric, "value": value}
        )

    def log_error(self, agent_name: str, error: Exception, context: str = "", details: Dict[str, Any] = None):
        """Log an error with context"""
        error_details = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context
        }

        if details:
            error_details.update(details)

        self.log(
            LogLevel.ERROR,
            LogCategory.ERROR,
            agent_name,
            f"Error occurred: {str(error)}",
            {},
            error_details
        )

    def get_recent_logs(self, agent_name: str = None, category: LogCategory = None, limit: int = 100) -> list:
        """Get recent log entries"""
        try:
            logs = []

            # Determine which log file to read
            if agent_name:
                log_file = os.path.join(self.log_dir, "agents", f"{agent_name}.log")
            elif category:
                log_file = os.path.join(self.log_dir, f"{category.value}.log")
            else:
                log_file = os.path.join(self.log_dir, "wealthyrobot.log")

            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    lines = f.readlines()[-limit:]  # Get last N lines

                for line in lines:
                    try:
                        if agent_name or category:  # JSON format
                            logs.append(json.loads(line.strip()))
                        else:  # Plain text format
                            logs.append({"message": line.strip()})
                    except:
                        logs.append({"message": line.strip()})

            return logs

        except Exception as e:
            print(f"❌ Error reading logs: {e}")
            return []

    def get_system_status(self) -> Dict[str, Any]:
        """Get logging system status"""
        try:
            log_files = []
            for root, dirs, files in os.walk(self.log_dir):
                for file in files:
                    if file.endswith('.log'):
                        filepath = os.path.join(root, file)
                        size = os.path.getsize(filepath)
                        log_files.append({
                            "file": os.path.relpath(filepath, self.log_dir),
                            "size": size,
                            "size_mb": round(size / (1024 * 1024), 2)
                        })

            return {
                "status": "active" if self.is_running else "inactive",
                "log_directory": self.log_dir,
                "queue_size": self.log_queue.qsize(),
                "log_files": log_files,
                "total_files": len(log_files)
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def shutdown(self):
        """Shutdown the logging system"""
        print("🔄 Shutting down centralized logger...")
        self.is_running = False

        if self.worker_thread:
            self.worker_thread.join(timeout=5)

        print("✅ Centralized logger shutdown complete")

# Global logger instance
logger = CentralizedLogger()

# Convenience functions for easy logging
def log_agent_activity(agent_name: str, action: str, details: Dict[str, Any] = None):
    """Convenience function to log agent activity"""
    logger.log_agent_activity(agent_name, action, details)

def log_trading_activity(agent_name: str, action: str, details: Dict[str, Any] = None):
    """Convenience function to log trading activity"""
    logger.log_trading_activity(agent_name, action, details)

def log_website_activity(agent_name: str, action: str, details: Dict[str, Any] = None):
    """Convenience function to log website activity"""
    logger.log_website_activity(agent_name, action, details)

def log_content_activity(agent_name: str, action: str, details: Dict[str, Any] = None):
    """Convenience function to log content activity"""
    logger.log_content_activity(agent_name, action, details)

def log_performance(agent_name: str, metric: str, value: Any, details: Dict[str, Any] = None):
    """Convenience function to log performance metrics"""
    logger.log_performance(agent_name, metric, value, details)

def log_error(agent_name: str, error: Exception, context: str = "", details: Dict[str, Any] = None):
    """Convenience function to log errors"""
    logger.log_error(agent_name, error, context, details)

if __name__ == "__main__":
    # Test the logging system
    print("🧪 Testing Centralized Logging System")
    print("=" * 40)

    # Test different log types
    log_agent_activity("test_agent", "initialization", {"version": "1.0.0"})
    log_trading_activity("trading_agent", "market_scan", {"markets": ["BTC", "ETH"]})
    log_website_activity("website_agent", "content_update", {"pages": 5})
    log_content_activity("content_agent", "article_created", {"word_count": 1500})
    log_performance("system_agent", "response_time", 0.245, {"endpoint": "/api/status"})

    # Test error logging
    try:
        raise ValueError("Test error")
    except Exception as e:
        log_error("test_agent", e, "Testing error logging")

    # Get system status
    status = logger.get_system_status()
    print(f"📊 Logging System Status: {status}")

    # Get recent logs
    recent_logs = logger.get_recent_logs(limit=5)
    print(f"📋 Recent Logs ({len(recent_logs)} entries):")
    for log in recent_logs[-3:]:  # Show last 3
        print(f"   {log}")

    print("✅ Centralized Logging System test complete!")
