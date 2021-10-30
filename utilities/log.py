from utilities.config import FORMATTER_STRING
import logging.config
import sys
from utilities.config import OUTPUT_DIR
from utilities.config import FILE_NAME_LOG
import os


def init_logger():
    # Create the path for the log file
    path = os.path.join(OUTPUT_DIR, FILE_NAME_LOG)
    # Create logger
    log = logging.getLogger("booking")
    log.setLevel(logging.DEBUG)
    # Create Formatter
    formatter = logging.Formatter(FORMATTER_STRING)
    # create a file handler and add it to logger
    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    # create a stream handler and add it to logger
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log