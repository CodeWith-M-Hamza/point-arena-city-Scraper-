# from selenium.webdriver.common.by import By
# import os
# from scraper.logging_setup import get_logger
# from scraper.exceptions import ScrapperError
# from scraper.utils import clean_text
# CITY_NAME = "point_arena"
# FILE_NAME = os.path.basename(__file__)
# logger = get_logger(CITY_NAME)

# GENERIC_SECTION_XPATH = "//div[@data-code-content-type='section']"
# def get_sections(driver, xpaths):
#     sections_data = []
#     try:
#         section_blocks = driver.find_elements(By.XPATH, GENERIC_SECTION_XPATH)

#         if not section_blocks:
#             raise ScrapperError(
#                 message="No sections found",
#                 file=FILE_NAME,
#                 url=driver.current_url,
#                 xpath=xpaths[GENERIC_SECTION_XPATH],
#                 city=CITY_NAME
#             )

#         for block in section_blocks:
#             guid = block.get_attribute("data-guid")
#             full_title =clean_text(block.get_attribute("data-full-title"))

#             try:
#                 body_xpath = f".//following::div[@id='{guid}_content']"
#                 body = clean_text(driver.find_element(By.XPATH, body_xpath).text)
#             except Exception:
#                 body = None
#                 logger.warning(f"Body not found for section guid {guid}")

#             sections_data.append({"title": full_title, "body": body})

#         logger.info(f"Found {len(sections_data)} sections")

#     except ScrapperError as e:
#         logger.error(f"{e.message} | xpath: {e.xpath} | url: {e.url}")

#     return sections_data




from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from scraper.logging_setup import get_logger
from scraper.exceptions import ScrapperError
from scraper.utils import clean_text

CITY_NAME = 'point_arena'
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def get_sections(driver, xpaths,depth=0,max_depth=6,visited=None):
    sections_data = []
    if visited is None:
        visited=set()
    current_url = driver.current_url
    if current_url in visited:
        return []
    visited.add(current_url)
    if depth > max_depth:
        logger.error(f"Max recursion depth reached | file: {FILE_NAME} | city: {CITY_NAME} | url: {current_url}")

    content_present = driver.find_elements(By.XPATH, xpaths['data'])

    if content_present:
        titles = driver.find_elements(By.XPATH, xpaths['chunks_title'])
        bodies = driver.find_elements(By.XPATH, xpaths['chunks_data'])

        if not titles:
            logger.error(
                f"XPath failed | file: {FILE_NAME} | city: {CITY_NAME} | url: {current_url} | xpath: {xpaths['chunks_title']}"
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
                f"XPath failed | file: {FILE_NAME} | city: {CITY_NAME} | url: {current_url} | xpath: {xpaths['urls']}"
            )
            return sections_data

        # next_urls = [el.get_attribute("href") for el in next_urls_elements]
        next_urls = list(set(el.get_attribute("href") for el in next_urls_elements))

        for next_url in next_urls:
            try:
                driver.get(next_url)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpaths['data']))
                )
            except Exception:
                pass

            child_sections = get_sections(driver, xpaths,depth=depth+1,max_depth=max_depth)
            sections_data.extend(child_sections)
            driver.get(current_url)

    logger.info(f"Found {len(sections_data)} sections on/under {current_url}")
    return sections_data