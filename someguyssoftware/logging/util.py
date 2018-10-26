# for logging
import logging
from logging.handlers import RotatingFileHandler

def create_rotating_log(path, name):
    """
    Creates a rotating log
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=250000,
                                  backupCount=5)
    c_handler = logging.StreamHandler() # add to the console

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    c_handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(c_handler)
    return logger
