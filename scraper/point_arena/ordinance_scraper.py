from selenium.webdriver.common.by import By
import os
from scraper.logging_setup import get_logger
from scraper.utils import clean_text
CITY_NAME = "point_arena"
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def get_ordinances(driver):
    ordinances_data = []
    try:
        rows = driver.find_elements(By.XPATH, "//table[@id='newLawsTable']/tbody/tr")

        if not rows:
            logger.info("No ordinances found on this page")
            return ordinances_data

        for row in rows:
            title = clean_text(row.get_attribute("data-title"))
            adopted = row.get_attribute("data-adopted")
            subject = clean_text(row.get_attribute("data-subject"))
            ordinances_data.append({
                "title": title,
                "adopted": adopted,
                "subject": subject
            })

        logger.info(f"Found {len(ordinances_data)} ordinances")

    except Exception as e:
        logger.warning(f"Issue while extracting ordinances: {str(e)}")

    return ordinances_data