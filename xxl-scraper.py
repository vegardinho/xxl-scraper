import os
import sys
from typing import Any


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_TOOLS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "python-tools"))
if PYTHON_TOOLS_DIR not in sys.path:
    sys.path.insert(0, PYTHON_TOOLS_DIR)

from my_logger import default_logger
from scraper import Scraper


SITE_NAME = "XXL"
TARGET_TEXT = "Ikke tilgjengelig online"
SECRETS_FILE = os.path.join(BASE_DIR, "input", "secrets.yaml")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "xxl_scraper.log")
ELEMENTS_OUT_FILE = os.path.join(BASE_DIR, "data", "elements.json")
HISTORY_FILE = os.path.join(BASE_DIR, "logs", "history.txt")
SEARCHES_FILE = os.path.join(BASE_DIR, "input", "searches.yaml")
EMAIL = "landsverk.vegard@gmail.com"
EMAIL_PWD_FILE = os.path.join(BASE_DIR, ".email_pwd")


class XXLAvailabilityScraper(Scraper):
    def __init__(self):
        logger = default_logger(log_dir=LOG_DIR)
        super().__init__(
            site_name=SITE_NAME,
            secrets_file=SECRETS_FILE,
            elements_out_file=ELEMENTS_OUT_FILE,
            history_file=HISTORY_FILE,
            searches_file=SEARCHES_FILE,
            email=EMAIL,
            log_file=LOG_FILE,
            logger=logger,
            email_pwd_file=EMAIL_PWD_FILE,
        )

    def _get_elements(self, page) -> list[dict[str, str]]:
        target_found = page.find(
            string=lambda text: text and " ".join(text.split()) == TARGET_TEXT
        )
        if target_found:
           self.logger.info("Not available. (Availability status matches target text)")
           return []

        availability_element = page.find(
            attrs={"data-testid": "availability-online"}
        )
        if availability_element is not None:
            status = " ".join(availability_element.get_text(" ").split())
        else:
            status = "Sannsynligvis tilgjengelig. Se lenke."
        self.logger.info("Availability status: %s", status)
        return [{"availability": status}]

    def _get_attrs(
        self,
        element: dict[str, str],
        elements: dict[str, Any],
        search: dict[str, str],
    ) -> dict[str, Any]:
        element["search"] = {
            "name": search["search_title"],
            "visit_url": search["display_url"],
            "search_url": search["search_url"],
        }
        element["title"] = search["search_title"]
        elements[search["search_url"]] = element
        return elements

    def _get_next_page(self, page, page_url: str) -> str | None:
        return None

    def _ad_string_format(
        self, offer_link: str, search_link: str, element: dict[str, Any]
    ) -> str:
        return (
            f"\nStatus for {element['title']}: {element['availability']}"
        )


if __name__ == "__main__":
    XXLAvailabilityScraper().main()