from selenium.webdriver.common.by import By
import os
from scraper.logging_setup import get_logger

CITY_NAME = "point_arena"
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)

def get_attachments(driver, xpaths):
    attachments_data = []
    try:
        attachments_section_exists = driver.find_elements(By.XPATH, "//div[@class='attachmentsTitle']")
        attachments = driver.find_elements(By.XPATH, xpaths["attachments"])

        if attachments_section_exists and not attachments:
            logger.warning("Attachments section exists but no links extracted — possible xpath issue")
        elif not attachments_section_exists:
            logger.info("No attachments section on this page")

        for attachment in attachments:
            name = attachment.text
            link = attachment.get_attribute("href")
            attachments_data.append({"name": name, "link": link})

        if attachments:
            logger.info(f"Found {len(attachments_data)} attachments")

    except Exception as e:
        logger.warning(f"Issue while extracting attachments: {str(e)}")

    return attachments_data