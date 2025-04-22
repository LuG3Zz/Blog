import logging
import sys
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class Logger:
    """Logger utility class for consistent logging across the application."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log an info message."""
        self.logger.info(message, extra=extra)
    
    def error(self, message: str, exc_info: bool = False, extra: Optional[Dict[str, Any]] = None):
        """Log an error message."""
        self.logger.error(message, exc_info=exc_info, extra=extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log a warning message."""
        self.logger.warning(message, extra=extra)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log a debug message."""
        self.logger.debug(message, extra=extra)
    
    def critical(self, message: str, exc_info: bool = False, extra: Optional[Dict[str, Any]] = None):
        """Log a critical message."""
        self.logger.critical(message, exc_info=exc_info, extra=extra)

def get_logger(name: str) -> Logger:
    """Get a logger instance for the given name."""
    return Logger(name)
