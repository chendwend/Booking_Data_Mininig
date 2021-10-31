from utilities.config import FORMATTER_STRING, OUTPUT_DIR, LOGGING_FILE
import logging.config
import sys
import os


def init_logger():
    # Create the path for the log file
    path = os.path.join(OUTPUT_DIR, LOGGING_FILE)
    # Create logger
    log = logging.getLogger()
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