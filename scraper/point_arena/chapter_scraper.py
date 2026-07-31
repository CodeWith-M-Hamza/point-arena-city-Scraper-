from selenium.webdriver.common.by import By
import os
from scraper.logging_setup import get_logger
from scraper.point_arena.attachment_scraper import get_attachments
from scraper.point_arena.ordinance_scraper import get_ordinances
from scraper.utils import clean_text

CITY_NAME = 'point_arena'
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def get_title(driver, xpaths):
    prefix_els = driver.find_elements(By.XPATH, xpaths['title_prefix'])
    suffix_els = driver.find_elements(By.XPATH, xpaths['title_suffix'])

    if not prefix_els or not suffix_els:
        logger.error(
            f"Title xpath failed | file={FILE_NAME} | url={driver.current_url} | xpath={xpaths['title_prefix']} / {xpaths['title_suffix']}"
        )
        return None

    full_title = clean_text(f"{prefix_els[0].text} : {suffix_els[0].text}")
    logger.info(f"Page Title : {full_title}")
    return full_title


def get_chapters(driver, xpaths):
    chapters_data = []
    chapters = []
    matched_xpath = None

    for xpath_option in xpaths['urls']:
        chapters = driver.find_elements(By.XPATH, xpath_option)
        if chapters:
            matched_xpath = xpath_option
            break

    if not chapters:
        logger.error(
            f"All chapter xpath variants failed | file={FILE_NAME} | url={driver.current_url} | xpaths={xpaths['urls']}"
        )
        return chapters_data

    for chapter in chapters:
        href = chapter.get_attribute("href")
        title = clean_text(chapter.text)
        chapters_data.append({"title": title, "url": href})

    logger.info(f"Found {len(chapters_data)} chapters using xpath: {matched_xpath}")
    return chapters_data


def scrape_title_page(driver, xpaths):
    return {
        "title": get_title(driver, xpaths),
        "chapters": get_chapters(driver, xpaths),
        "attachments": get_attachments(driver, xpaths),
        "ordinances": get_ordinances(driver,xpaths),
    }