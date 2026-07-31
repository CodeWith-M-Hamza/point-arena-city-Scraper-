from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
from scraper.logging_setup import get_logger

CITY_NAME = 'point_arena'
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def open_page(driver, url):
    try:
        driver.get(url)
        logger.info(f"Opened URL: {url}")
    except Exception as e:
        logger.error(f"Failed to open url | file={FILE_NAME} | url={url} | error={e}")


def dismiss_cookie_popup(driver, xpaths):
    cookie_buttons = driver.find_elements(By.XPATH, xpaths['dismiss_message'])

    if not cookie_buttons:
        logger.error(f"No cookie popup found | url={driver.current_url} | xapth={xpaths['dismiss_message']}")
        return

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['dismiss_message']))
        )
        cookie_buttons[0].click()
        logger.info("Cookie popup dismissed")
    except Exception as e:
        logger.error(
            f"Cookie popup found but click failed | url={driver.current_url} | xpath={xpaths['dismiss_message']} | error={e}"
        )