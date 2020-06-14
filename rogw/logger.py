from datetime import datetime
import logging
import os

from rogw.config import config
from rogw.timezone import Timezone


def main_logger(formatter: logging.Formatter) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def report_logger(formatter: logging.Formatter) -> logging.Logger:
    logger = logging.getLogger(f'{__name__}.report')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(config['REPORT_FILEPATH']))
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
formatter.converter = lambda *args: datetime.now(tz=Timezone()).timetuple()
logger = main_logger(formatter)
report = report_logger(formatter)
