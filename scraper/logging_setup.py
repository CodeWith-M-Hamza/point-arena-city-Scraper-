import logging
import os
from datetime import datetime


def get_logger(city_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger_name = f"{city_name}_{timestamp}"

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)
        log_path = os.path.join(log_folder, f"{logger_name}.log")

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.ERROR)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger