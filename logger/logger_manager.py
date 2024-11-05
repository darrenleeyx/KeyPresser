import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class LoggerManager:
    def __init__(self):
        self.setup()

    def setup(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_handler = TimedRotatingFileHandler(f"__logs__/{current_date}.log", when="midnight", interval=1)
        log_handler.suffix = "%Y-%m-%d"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
            log_handler,
            logging.StreamHandler()])
        
    def log_info(self, message):
        logging.info(message)