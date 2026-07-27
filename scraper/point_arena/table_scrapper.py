from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from scraper.logging_setup import get_logger

CITY_NAME = "point_arena"
FILE_NAME = os.path.basename(__file__)
logger = get_logger(CITY_NAME)


def extract_clickable_tables(driver, xpaths, chunk_count):
    tables_data = []
    try:
        xpath = xpaths["clickable_tables"].format(chunk_count=chunk_count)
        tables = driver.find_elements(By.XPATH, xpath)

        if not tables:
            return tables_data

        for table in tables:
            driver.execute_script("arguments[0].scrollIntoView(true);", table)
            table.click()

            wait = WebDriverWait(driver, 5)
            expanded = wait.until(
                EC.visibility_of_element_located((By.XPATH, xpaths["expanded_table"]))
            )

            table_text = expanded.text
            tables_data.append(table_text)

            close_button = expanded.find_element(By.XPATH, xpaths["close_clickable_table"])
            close_button.click()

            wait.until(
                EC.invisibility_of_element_located((By.XPATH, xpaths["expanded_table"]))
            )

        logger.info(f"Extracted {len(tables_data)} tables")

    except Exception as e:
        logger.warning(f"Issue while extracting clickable tables: {str(e)}")

    return tables_data