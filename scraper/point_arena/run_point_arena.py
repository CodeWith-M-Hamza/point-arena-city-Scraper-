import json
import os
from scraper.point_arena.driver_setup import create_driver
from scraper.point_arena.page_actions import open_page, dismiss_cookie_popup
from scraper.point_arena.chapter_scraper import scrape_title_page
from scraper.point_arena.section_scraper import get_sections
from scraper.point_arena.attachment_scraper import get_attachments
from scraper.point_arena.ordinance_scraper import get_ordinances
from scraper.point_arena.table_scrapper import extract_clickable_tables
from scraper.logging_setup import get_logger

CITY_NAME = "point_arena"
logger = get_logger(CITY_NAME)

TITLE_URL = "https://ecode360.com/42540590"
# TITLE_URL="https://ecode360.com/42541431"

with open("scraper/xpaths/ecode_xpaths.json", "r") as f:
    xpaths = json.load(f)


def run():
    final_data = {"title": None, "chapters": [],"attachments":[],"ordinances":[]}
    driver = create_driver()

    try:
        # Step 1: Open Title page, dismiss cookie popup, get chapter list
        open_page(driver, TITLE_URL)
        dismiss_cookie_popup(driver, xpaths)
        title_page_data = scrape_title_page(driver, xpaths)
        final_data["title"] = title_page_data["title"]
        final_data["attachments"]=title_page_data["attachments"]
        final_data["ordinances"]=title_page_data["ordinances"]

        # Step 2: Loop through each chapter
        for chapter in title_page_data["chapters"]:
            chapter_url = chapter["url"]
            logger.info(f"Opening chapter: {chapter['title']}")

            open_page(driver, chapter_url)

            sections = get_sections(driver, xpaths)
            attachments = get_attachments(driver, xpaths)
            ordinances = get_ordinances(driver)

            # Step 3: For each section, check for clickable tables
            for index, section in enumerate(sections, start=1):
                tables = extract_clickable_tables(driver, xpaths, chunk_count=index)
                section["tables"] = tables

            final_data["chapters"].append({
                "title": chapter["title"],
                "url": chapter_url,
                "sections": sections,
                "attachments": attachments,
                "ordinances": ordinances
            })

        logger.info("Scraping completed successfully")

    except Exception as e:
        logger.error(f"Unexpected error during run: {str(e)}")

    finally:
        driver.quit()
        logger.info("Driver closed")

    return final_data


if __name__ == "__main__":
    result = run()

    os.makedirs("output", exist_ok=True)
    with open("output/point_arena.json", "w") as f:
        json.dump(result, f, indent=2)

    logger.info("Data saved to output/point_arena.json")