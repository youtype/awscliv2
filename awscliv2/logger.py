import logging


def get_logger(level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger("awscliv2")
    if logger.handlers:
        return logger

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)
    logger.setLevel(level)

    return logger
