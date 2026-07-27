from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os 
from scraper.logging_setup import get_logger
from scraper.exceptions import ScrapperError
CITY_NAME='point_arena'
FILE_NAME = os.path.basename(__file__)
logger=get_logger(CITY_NAME)
def open_page(driver,url):
    try:
        driver.get(url)
        logger.info(f"Opened URL: {url}")
    except Exception as e:
        raise ScrapperError(
            message=f"failed to open url:{str(e)}",
            file=FILE_NAME,
            url=url,
            xpath='N/A',
            city=CITY_NAME
        )
def dismiss_cookie_popup(driver,xpaths):
    try:
        wait=WebDriverWait(driver,5)
        cookie_button=wait.until(
            EC.element_to_be_clickable((By.XPATH,xpaths['dismiss_message']))

        )
        cookie_button.click()
        logger.info("cookie popup dismissed")
    except TimeoutException:
        logger.info("No popup appeared")
    except Exception as e:
        logger.warning("cookie popup issue {str(e)}")