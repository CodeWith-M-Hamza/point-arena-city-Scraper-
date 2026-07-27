from selenium.webdriver.common.by import By
import os
from scraper.logging_setup import get_logger
from scraper.exceptions import ScrapperError
from scraper.utils import clean_text
CITY_NAME = "point_arena"
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def get_sections(driver, xpaths):
    sections_data = []
    try:
        section_blocks = driver.find_elements(By.XPATH, xpaths["chunks_title"])

        if not section_blocks:
            raise ScrapperError(
                message="No sections found",
                file=FILE_NAME,
                url=driver.current_url,
                xpath=xpaths["chunks_title"],
                city=CITY_NAME
            )

        for block in section_blocks:
            guid = block.get_attribute("data-guid")
            full_title =clean_text(block.get_attribute("data-full-title"))

            try:
                body_xpath = f".//following::div[@id='{guid}_content']"
                body = clean_text(driver.find_element(By.XPATH, body_xpath).text)
            except Exception:
                body = None
                logger.warning(f"Body not found for section guid {guid}")

            sections_data.append({"title": full_title, "body": body})

        logger.info(f"Found {len(sections_data)} sections")

    except ScrapperError as e:
        logger.error(f"{e.message} | xpath: {e.xpath} | url: {e.url}")

    return sections_data
