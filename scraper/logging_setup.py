import logging
import os
def get_logger(city_name):
    logger = logging.getLogger(city_name)
    logger.setLevel(logging.DEBUG)  # logger khud sabse detailed level pe rahe

    if not logger.handlers:
        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)
        log_path = os.path.join(log_folder, f"{city_name}.log")

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)   # NAYA: file mein sirf ERROR+

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # console pe sab kuch

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger