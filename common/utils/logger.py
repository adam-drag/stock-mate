import logging
import os
import sys
from datetime import datetime

now = datetime.now()
timestamp = datetime.timestamp(now)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_logger(name):
    """
        Sets log level to INFO for prod.
        For everything else (dev, staging, None), it is DEBUG.
    """
    environment = os.environ.get("APP_ENV")
    if environment == "production":
        desired_log_level = logging.INFO
    else:
        desired_log_level = logging.DEBUG

    logger = logging.getLogger(name)
    logger.setLevel(desired_log_level)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(desired_log_level)

    stdout_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    return logger
