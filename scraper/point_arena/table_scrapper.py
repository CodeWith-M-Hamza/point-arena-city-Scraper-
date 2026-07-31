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

    xpath = xpaths["clickable_tables"].format(chunk_count=chunk_count)
    tables = driver.find_elements(By.XPATH, xpath)

    if not tables:
        return tables_data

    for table in tables:
        driver.execute_script("arguments[0].scrollIntoView(true);", table)

        try:
            table.click()
        except Exception as e:
            logger.error(f"Table click failed | url={driver.current_url} | error={e}")
            continue

        try:
            expanded = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, xpaths["expanded_table"]))
            )
        except Exception as e:
            logger.error(
                f"Expanded table did not appear | url={driver.current_url} | xpath={xpaths['expanded_table']} | error={e}"
            )
            continue

        tables_data.append(expanded.text)

        close_buttons = expanded.find_elements(By.XPATH, xpaths["close_clickable_table"])
        if not close_buttons:
            logger.error(
                f"Close button not found | url={driver.current_url} | xpath={xpaths['close_clickable_table']}"
            )
            continue

        try:
            close_buttons[0].click()
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, xpaths["expanded_table"]))
            )
        except Exception as e:
            logger.error(f"Table close failed | url={driver.current_url} | error={e}")

    logger.info(f"Extracted {len(tables_data)} tables")
    return tables_data