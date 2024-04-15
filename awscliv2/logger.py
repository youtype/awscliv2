"""
Logging utils.
"""

import logging

from awscliv2.constants import LOGGER_NAME

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
TIME_FORMAT = "%H:%M:%S"


def get_logger(level: int = logging.DEBUG) -> logging.Logger:
    """
    Get default logger.

    Arguments:
        level -- Python log level

    Returns:
        New or existing logger instance.
    """
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)
    logger.setLevel(level)

    return logger
