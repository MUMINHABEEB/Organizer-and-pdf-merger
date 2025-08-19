import logging
import os

# Configure the logging settings
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Create a file handler that logs debug and higher level messages
log_file_path = os.path.join(os.path.dirname(__file__), 'app.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(LOG_LEVEL)

# Create a console handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

# Create and set the formatter for the handlers
formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message)

def log_debug(message):
    logger.debug(message)