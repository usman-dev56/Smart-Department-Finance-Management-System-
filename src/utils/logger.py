# src/utils/logger.py
"""Logging configuration and utilities"""
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path


# Global logger instance
_logger = None
_logging_initialized = False


def setup_logging(log_level="INFO", log_file="data/logs/app.log", max_bytes=5*1024*1024, backup_count=3):
    """Setup logging configuration"""
    global _logging_initialized
    
    if _logging_initialized:
        return
    
    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (with rotation)
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create log file: {e}")
    
    _logging_initialized = True
    logging.info(f"Logging initialized. Log file: {log_file}")


def get_logger(name=None):
    """Get a logger instance"""
    global _logging_initialized, _logger
    
    if not _logging_initialized:
        setup_logging()
    
    if name:
        return logging.getLogger(name)
    
    if _logger is None:
        _logger = logging.getLogger('SDFFMS')
    
    return _logger


def log_info(message, name=None):
    """Log info message"""
    logger = get_logger(name)
    logger.info(message)


def log_error(message, name=None):
    """Log error message"""
    logger = get_logger(name)
    logger.error(message)


def log_warning(message, name=None):
    """Log warning message"""
    logger = get_logger(name)
    logger.warning(message)


def log_debug(message, name=None):
    """Log debug message"""
    logger = get_logger(name)
    logger.debug(message)


def log_exception(message, name=None):
    """Log exception with traceback"""
    logger = get_logger(name)
    logger.exception(message)


# Create a simple logger for quick imports
logger = get_logger()


# Example usage
if __name__ == "__main__":
    setup_logging()
    log_info("Logger test - info message")
    log_warning("Logger test - warning message")
    log_error("Logger test - error message")
    print("Logging test complete. Check data/logs/app.log")