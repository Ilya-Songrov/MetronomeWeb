import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class MyLogger:
    def __init__(self):            
        pass

    def createLoggerConfigsStdout() -> 'logging.Logger':
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} [p%(process)s]: %(message)s')

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)

        logger.addHandler(stdout_handler)

        return logger 

    def createLoggerConfigs(log_dir_to_save: str, fileName: str) -> 'logging.Logger':
        if log_dir_to_save is None or fileName is None:
            return logging.getLogger()
        Path(log_dir_to_save).mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} [p%(process)s]: %(message)s')

        file_handler = RotatingFileHandler(filename=log_dir_to_save + "/" + fileName, 
            mode='w', 
            maxBytes=100*1000*1000, 
            backupCount=4)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger