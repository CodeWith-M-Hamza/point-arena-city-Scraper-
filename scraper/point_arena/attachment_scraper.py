from selenium.webdriver.common.by import By
import os
from scraper.logging_setup import get_logger
from scraper.utils import clean_text

CITY_NAME = "point_arena"
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def get_attachments(driver, xpaths):
    attachments_data = []
    attachments_section_exists = driver.find_elements(By.XPATH, xpaths["attachments_section"])
    attachments = driver.find_elements(By.XPATH, xpaths["attachments"])

    if attachments_section_exists and not attachments:
        logger.error(
            f"Attachments xpath failed | file={FILE_NAME} | url={driver.current_url} | xpath={xpaths['attachments']}"
        )
    elif not attachments_section_exists:
        logger.info(f"No attachments section on this page | url={driver.current_url}")

    for attachment in attachments:
        name = clean_text(attachment.text)
        link = attachment.get_attribute("href")
        attachments_data.append({"name": name, "link": link})

    if attachments:
        logger.info(f"Found {len(attachments_data)} attachments")

    return attachments_data