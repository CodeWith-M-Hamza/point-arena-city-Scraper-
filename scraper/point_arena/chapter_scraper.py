from selenium.webdriver.common.by import By
import os 
from scraper.logging_setup import get_logger
from scraper.exceptions import ScrapperError

CITY_NAME = 'point_arena'
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def get_title(driver, xpaths):
    try:
        prefix = driver.find_element(By.XPATH, xpaths['title_prefix']).text
        suffix = driver.find_element(By.XPATH, xpaths['title_suffix']).text
        full_title = f"{prefix} : {suffix}"
        logger.info(f"Page Title : {full_title}")
        return full_title
    except Exception as e:
        logger.warning(f"couldn't extract title : {str(e)}")
        return None


def get_chapters(driver, xpaths):
    chapters_data = []
    try:
        chapters = []
        matched_xpath = None
        for xpath_option in xpaths['urls']:
            chapters = driver.find_elements(By.XPATH, xpath_option)
            if chapters:
                matched_xpath = xpath_option
                break

        if not chapters:
            raise ScrapperError(
                message="No chapters found",
                file=FILE_NAME,
                url=driver.current_url,
                xpath=str(xpaths["urls"]),
                city=CITY_NAME
            )

        for chapter in chapters:
            href = chapter.get_attribute("href")
            title = chapter.text
            chapters_data.append({"title": title, "url": href})

        logger.info(f"Found {len(chapters_data)} chapters using xpath: {matched_xpath}")

    except ScrapperError as e:
        logger.error(f"{e.message} | xpath: {e.xpath} | url:{e.url} ")

    return chapters_data


def scrape_title_page(driver, xpaths):
    title = get_title(driver, xpaths)
    chapters = get_chapters(driver, xpaths)
    return {"title": title, "chapters": chapters}