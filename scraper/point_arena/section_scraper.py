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


def get_sections(driver, xpaths):
    """
    Chapter (ya Article/Sub-article) page pe check karta hai:
    - Agar 'data' xpath se content mile -> seedha sections nikalo (chunks_title/chunks_data)
    - Agar na mile -> 'urls' xpath se agle level ke links dhoondo, har ek pe navigate + recurse
    """
    sections_data = []
    current_url = driver.current_url

    try:
        content_present = driver.find_elements(By.XPATH, xpaths['data'])

        if content_present:
            # Content isi page pe hai -> seedha titles + bodies nikalo
            titles = driver.find_elements(By.XPATH, xpaths['chunks_title'])
            bodies = driver.find_elements(By.XPATH, xpaths['chunks_data'])

            if not titles:
                raise ScrapperError(
                    message="Content present but no section titles found",
                    file=FILE_NAME,
                    url=current_url,
                    xpath=xpaths['chunks_title'],
                    city=CITY_NAME
                )

            for i, title_el in enumerate(titles):
                title = clean_text(title_el.text)
                body = clean_text(bodies[i].text) if i < len(bodies) else None
                sections_data.append({"title": title, "url": current_url, "body": body})

        else:
            # Content nahi mila -> ye ek index/listing page hai, agle level ke links dhoondo
            next_urls_elements = driver.find_elements(By.XPATH, xpaths['urls'][0])
            if not next_urls_elements:
                next_urls_elements = driver.find_elements(By.XPATH, xpaths['urls'][1])
            if not next_urls_elements:
                next_urls_elements = driver.find_elements(By.XPATH, xpaths['urls'][2])

            if not next_urls_elements:
                raise ScrapperError(
                    message="No content and no next-level urls found",
                    file=FILE_NAME,
                    url=current_url,
                    xpath=str(xpaths['urls']),
                    city=CITY_NAME
                )

            next_urls = [el.get_attribute("href") for el in next_urls_elements]

            for next_url in next_urls:
                try:
                    driver.get(next_url)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpaths['data']))
                    )
                except Exception:
                    pass  # agar wait timeout ho, aage recursive call khud check kar lega

                # RECURSION: isi function ko dobara call karo naye page ke liye
                child_sections = get_sections(driver, xpaths)
                sections_data.extend(child_sections)

                driver.get(current_url)  # wapas is (parent) level pe aao, agla next_url process karne ke liye

        logger.info(f"Found {len(sections_data)} sections on/under {current_url}")

    except ScrapperError as e:
        logger.error(f"{e.message} | xpath: {e.xpath} | url: {e.url}")

    return sections_data