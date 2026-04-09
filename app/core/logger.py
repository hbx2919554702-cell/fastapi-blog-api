import logging
import os
from logging.handlers import TimedRotatingFileHandler

BASE_DIR =os.getcwd()
LOG_DIR=os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger=logging.getLogger("blog_api")
logger.setLevel(logging.INFO)

if not logger.handlers:
    console_handler=logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter=logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s)] [%(filename)s:%(lineno)d] -> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_file_path=os.path.join(LOG_DIR, "api.log")
    file_handler=TimedRotatingFileHandler(
        filename=log_file_path,
        when="midnight",
        interval=1,
        encoding="utf-8",
        backupCount=7,
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)