"""
Logging configuration for the accounts app.
Provides a pre-configured logger that writes to stdout so all errors
are visible in Railway (and any other 12-factor) deployment logs.
"""
import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger that always writes to stdout.

    Usage:
        from accounts.logging_config import get_logger
        logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if the logger is retrieved more than once
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Propagate to the root logger so Django's LOGGING config also captures it
    logger.propagate = True

    return logger
