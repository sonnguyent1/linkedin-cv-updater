import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger that writes to a centralized log file,
    ensuring stdout is clean for MCP JSON-RPC communication.
    """
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, assume it's configured to prevent duplicate logs
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    # Define log directory in user's home folder
    log_dir = Path.home() / ".linkedin-cv-updater" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "server.log"
    
    # Create a rotating file handler (max 5MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    
    # Define a robust log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger
