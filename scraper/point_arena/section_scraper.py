
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from scraper.logging_setup import get_logger
from scraper.utils import clean_text

CITY_NAME = 'point_arena'
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def get_sections(driver, xpaths, depth=0, max_depth=6, visited=None):
    sections_data = []
    if visited is None:
        visited = set()

    current_url = driver.current_url
    if current_url in visited:
        return []
    visited.add(current_url)

    if depth > max_depth:
        logger.error(f"Max recursion depth reached | file={FILE_NAME} | url={current_url}")
        return sections_data

    content_present = driver.find_elements(By.XPATH, xpaths['data'])

    if content_present:
        titles = driver.find_elements(By.XPATH, xpaths['chunks_title'])
        bodies = driver.find_elements(By.XPATH, xpaths['chunks_data'])

        if not titles:
            logger.error(
                f"Titles xpath failed | file={FILE_NAME} | url={current_url} | xpath={xpaths['chunks_title']}"
            )
            return sections_data

        for i, title_el in enumerate(titles):
            title = clean_text(title_el.text)
            body = clean_text(bodies[i].text) if i < len(bodies) else None
            sections_data.append({"title": title, "url": current_url, "body": body})

    else:
        next_urls_elements = driver.find_elements(By.XPATH, xpaths['urls'][0])
        if not next_urls_elements:
            next_urls_elements = driver.find_elements(By.XPATH, xpaths['urls'][1])
        if not next_urls_elements:
            next_urls_elements = driver.find_elements(By.XPATH, xpaths['urls'][2])

        if not next_urls_elements:
            logger.error(
                f"All url xpath variants failed | file={FILE_NAME} | url={current_url} | xpaths={xpaths['urls']}"
            )
            return sections_data

        next_urls = list(set(el.get_attribute("href") for el in next_urls_elements))

        for next_url in next_urls:
            driver.get(next_url)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpaths['data']))
                )
            except Exception as e:
                logger.error(
                    f"Content wait timed out | file={FILE_NAME} | url={next_url} | xpath={xpaths['data']} | error={e}"
                )

            child_sections = get_sections(driver, xpaths, depth=depth + 1, max_depth=max_depth, visited=visited)
            sections_data.extend(child_sections)
            driver.get(current_url)

    logger.info(f"Found {len(sections_data)} sections on/under {current_url}")
    return sections_data