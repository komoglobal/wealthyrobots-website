#!/usr/bin/env python3
"""
AGI Logging System
==================

Centralized logging configuration for the AGI system.
Provides structured logging with different levels and formats.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any

class AGILogger:
    """Centralized logging system for AGI components"""

    def __init__(self, name: str = "AGI", log_level: str = "INFO"):
        self.name = name
        self.log_level = log_level
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with proper formatting and handlers"""
        logger = logging.getLogger(self.name)
        logger.setLevel(getattr(logging, self.log_level.upper(), logging.INFO))

        # Remove any existing handlers
        logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s [%(name)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )

        # Console handler (simple format)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)

        # File handler (detailed format)
        log_dir = "/tmp/agi_logs"
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f"agi_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

        return logger

    def debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message"""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message"""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self.logger.critical(message, *args, **kwargs)

    def log_performance(self, operation: str, duration: float, metadata: Optional[Dict[str, Any]] = None):
        """Log performance metrics"""
        message = f"PERFORMANCE: {operation} completed in {duration:.4f}s"
        if metadata:
            message += f" | {metadata}"
        self.logger.info(message)

    def log_agi_cycle(self, cycle_number: int, intelligence_level: str, insights_gained: int):
        """Log AGI cycle completion"""
        self.logger.info(f"AGI_CYCLE: Cycle {cycle_number} completed | Intelligence: {intelligence_level} | Insights: {insights_gained}")

    def log_error_recovery(self, error_type: str, recovery_action: str, success: bool):
        """Log error recovery attempts"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.warning(f"ERROR_RECOVERY: {error_type} -> {recovery_action} [{status}]")

    def log_quantum_operation(self, operation: str, qubits: int, success: bool):
        """Log quantum-inspired operations"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"QUANTUM: {operation} with {qubits} qubits [{status}]")

# Global logger instances
agi_logger = AGILogger("AGI_SYSTEM")
performance_logger = AGILogger("AGI_PERFORMANCE", "DEBUG")
quantum_logger = AGILogger("AGI_QUANTUM", "INFO")

def get_logger(name: str, level: str = "INFO") -> AGILogger:
    """Get a logger instance for a specific component"""
    return AGILogger(name, level)

def log_agi_status(intelligence_level: str, goals: int, agents: int, profit: float):
    """Log current AGI system status"""
    agi_logger.info(f"AGI_STATUS: Intelligence={intelligence_level}, Goals={goals}, Agents={agents}, Profit=${profit:.2f}")

def log_system_health(component: str, health_status: str, metrics: Optional[Dict[str, Any]] = None):
    """Log system component health"""
    message = f"SYSTEM_HEALTH: {component} = {health_status}"
    if metrics:
        message += f" | {metrics}"
    agi_logger.info(message)
