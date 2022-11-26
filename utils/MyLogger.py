import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class MyLogger:
    def __init__(self):            
        pass

    def createLoggerConfigs(self, log_dir_to_save: str) -> 'logging.Logger':
        Path(log_dir_to_save).mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} [p%(process)s]: %(message)s')

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(filename=log_dir_to_save + '/ldb-consumer.log', 
            mode='w', 
            maxBytes=100*1000*1000, 
            backupCount=4)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)

        return logger