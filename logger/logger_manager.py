import logging, os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class LoggerManager:
    def __init__(self):
        self.setup()

    def create_directory(self):
        try:
            if not os.path.exists("__logs__"):
                os.makedirs("__logs__")
        except FileExistsError:
            pass

    def setup(self):
        self.create_directory()
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_handler = TimedRotatingFileHandler(f"__logs__/{current_date}.log", when="midnight", interval=1)
        log_handler.suffix = "%Y-%m-%d"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
            log_handler,
            logging.StreamHandler()])
        
    def log_info(self, message):
        logging.info(message)

    def log_error(self, exception):
        logging.error(f"An error occurred: {exception}")