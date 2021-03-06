import threading
import logging
from django.conf import settings

_LOCALS = threading.local()

def get_logger():
    logger = getattr(_LOCALS, 'logger', None)
    if logger is not None:
        return logger
        
    logger = logging.getLogger()
    hdlr = logging.FileHandler(settings.LOG_FILE)
    formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S') 
    
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)

    setattr(_LOCALS, 'logger', logger)
    return logger

def debug(msg):
    logger = get_logger()
    logger.debug(msg)