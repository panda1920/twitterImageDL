import logging

from twitter_image_dl.global_constants import MODULE_NAME, LOGFILE_NAME

def setup_logger(log_location, level):
    logger = logging.getLogger(MODULE_NAME)
    handler = logging.FileHandler(
        log_location / LOGFILE_NAME, mode='w', encoding='utf-8'
    )
    formatter = logging.Formatter(
        '%(levelname)s %(asctime)s -- %(name)s:%(lineno)s -- %(message)s'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(level)
