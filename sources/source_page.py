
import time
from selenium import webdriver
from utilities.config import PAGES_BUTTONS, USER_AGENT, SEARCH_BAR, SEARCH_BUTTON, \
    CALENDAR, BAR
from sources.page import Page
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from sources.element import Element
import logging
logger = logging.getLogger()


class Website(Element):
    """
    A class to represent a booking.com website element.
    """
    page_offset = 25

    def __init__(self, main_url, page_limit):
        """
        Constructs all the necessary attributes for the Website object.

        :param main_url: the main website URL
        :type main_url: str
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument(f'user-agent={USER_AGENT}')  # Without this -> doesn't find pages
        self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        logger.info(f"Webdriver instantiated")
        self._driver.get(main_url)
        self._page_limit = page_limit
        logger.info(f"{main_url} loaded successfully")

    def insert_location(self, location):
        """
        - Finds & inserts location into the search bar.
        - Finds & clicks on the search button
        Upon failure to find anyone of them, stops the program.

        :param location: the desired country
        :type location: str
        """
        searchbar_element = self.get_element_by_name(self._driver, SEARCH_BAR, "quit")
        logger.info(f"searchbar found.")
        searchbar_element.send_keys(location)
        logger.info(f"searchbar filled with destination.")
        self.click_button(SEARCH_BUTTON)
        logger.info(f"search button found and clicked.")

    def select_date(self, start_date, end_date):
        """
        Chooses the start & end dates of visit from the calendar and clicks search button.
        Upon failure to find the calendar, stops the program.

        :param start_date: the start date of visit
        :type start_date: datetime
        :param end_date: the end date of visit
        :type end_date: datetime
        """
        self.get_elements(self._driver, CALENDAR, on_exception="quit")
        logger.info(f"calendar found")
        self._driver.find_element_by_css_selector(
            f"span[aria-label='{start_date.day} {start_date.strftime('%B')} {start_date.year}']").click()
        logger.info(f"start date filled.")
        self._driver.find_elements_by_css_selector(".sb-date-field__display")[1].click()
        self._driver.find_element_by_css_selector(
            f"span[aria-label='{end_date.day} {end_date.strftime('%B')} {end_date.year}']").click()
        logger.info(f"end date filled.")
        self._driver.find_element_by_css_selector(SEARCH_BUTTON["selector"]).click()
        logger.info(f"calendar search button found and clicked.")

    def _get_next_page_element(self, page_number):
        """
        gets the adequate page number element from the DOM
        :param page_number: the current page to be processed
        :type page_number: int
        :return:  Webdriver element
        """

        pages_elements = self.get_elements(self._driver, PAGES_BUTTONS, on_exception='quit')
        logger.info(f"pages elements were found on page {page_number}")
        if page_number < 8:
            return pages_elements[page_number + 1]
        else:
            return pages_elements[7]

    def get_all_data(self):
        """
        gets all data from all pages
        :return: a pandas DataFrame with columns as a stay service, records as stays
        """

        pages_elements = self.get_elements(self._driver, PAGES_BUTTONS, on_exception='quit')
        number_of_pages = int(pages_elements[-2].text)
        logger.info(f"Total number of pages: {number_of_pages}")
        print(f"Found {number_of_pages} pages.")
        print(f"processing {self._page_limit} pages")
        for page_number in range(1, self._page_limit+1):  # number_of_pages + 1
            print(f"Processing page number  {page_number}/{number_of_pages}... \n {BAR}")
            page = Page(self._driver)
            if page_number == 1:
                data = page.get_data()
            else:
                data = data.append(page.get_data(), ignore_index=True)
            next_page_element = self._get_next_page_element(page_number)
            logger.info(f"finished page {page_number}.")
            next_page_element.click()
            logger.info(f"moved to page {page_number + 1}.")
            time.sleep(2)

        # number_of_failed_pages = Page.failed_pages
        # number_of_failed_stays = Page.failed_stays
        # number_of_tricky_pages = Page.tricky_page_count
        return data, number_of_pages  # , number_of_failed_pages, number_of_failed_stays, number_of_tricky_pages

    def teardown(self):
        """
        closes the webdriver
        """
        logger.info(f"webdriver instance closed.")
        self._driver.quit()
