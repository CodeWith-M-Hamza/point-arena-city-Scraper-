from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from scraper.logging_setup import get_logger

CITY_NAME = 'point_arena'
logger = get_logger(CITY_NAME)
FILE_NAME = os.path.basename(__file__)


def create_driver():
    try:
        option = Options()
        option.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=option)
        logger.info("chrome driver is created and window maximized")
        return driver
    except Exception as e:
        logger.error(f"Failed to start chrome driver | file={FILE_NAME} | error={e}")
        return None