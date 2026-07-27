from selenium import webdriver
import os 
from selenium.webdriver.chrome.options import Options
from scraper.logging_setup import get_logger
from scraper.exceptions import ScrapperError
CITY_NAME='point_arena'
logger=get_logger(CITY_NAME)
FILE_NAME=os.path.basename(__file__)
def create_driver():
    try:
        option=Options()
        option.add_argument("--start-maximized")
        driver=webdriver.Chrome(options=option)
        logger.info("chrome driver is created and window maximized")
        return driver
    except Exception as e:
        raise ScrapperError(
            message=f"failed to start chrome driver {str(e)}",
            file=FILE_NAME,
            url="N/A",
            xpath="N/A",
            city=CITY_NAME
        )   