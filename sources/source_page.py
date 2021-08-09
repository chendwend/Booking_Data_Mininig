from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.config import *
from sources.page import Page
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import sys
import re


class Website:
    """
    A class to represent a booking.com website
    """
    page_offset = 25

    def __init__(self, main_url):
        """
        Constructs all the necessary attributes for the Website object.

        :param main_url: the main website URL
        :type main_url: str
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument(f'user-agent={USER_AGENT}')
        self._driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
        self._driver.get(main_url)

    def enter_location(self, location):
        """
        Inserts the given location into the search bar.
        Upon failure to find the search bar, stops the program.

        :param location: the desired destination
        :type location: str
        """
        try:
            search_location = WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_element_located((By.NAME, SEARCH_LOCATION_STRING))
            )
            search_location.send_keys(location)

        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find search for input or Timeout= {SEC_TO_WAIT} seconds passed.")

    def click_search_button(self):
        """
        Finds and clicks the search button
        Upon failure to find the search button, stops the program.
        """
        try:
            search_button = WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_BUTTON_STRING))
            )
            search_button.click()
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the search button or Timeout= {SEC_TO_WAIT} seconds passed.")

    def select_date(self, start_date, end_date):
        """
        Chooses the start & end dates of visit from the calendar and clicks search button.
        Upon failure to find the calendar, stops the program.

        :param start_date: the start date of visit
        :type start_date: datetime
        :param end_date: the end date of visit
        :type end_date: datetime
        """
        try:
            WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, CALENDAR_STRING))
            )
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the calendar field or Timeout= {SEC_TO_WAIT} seconds passed.")
        self._driver.find_element_by_css_selector(
            f"span[aria-label='{start_date.day} {start_date.strftime('%B')} {start_date.year}']").click()
        self._driver.find_elements_by_css_selector(".sb-date-field__display")[1].click()
        self._driver.find_element_by_css_selector(
            f"span[aria-label='{end_date.day} {end_date.strftime('%B')} {end_date.year}']").click()
        self._driver.find_element_by_css_selector(SEARCH_BUTTON_STRING).click()

    def _get_urls(self):
        """
        Extracts list of URLs representing each page result.

        :return: list of URLs
        :rtype: list
        """
        list_urls = []
        first_page_url = self._driver.current_url
        list_urls.append(first_page_url)
        try:
            page_buttons = WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, PAGES_LINKS_STRING))
            )
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the page buttons or Timeout= {SEC_TO_WAIT} seconds passed.")

        last_url = page_buttons[-1].get_attribute("href")
        last_offset_number = int(re.search(OFFSET_REGEX, last_url).group())
        last_equal_sign_index = last_url.rfind('=')
        base_url = last_url[:last_equal_sign_index] + '='
        number_of_pages = int(last_offset_number / Website.page_offset) + 1
        for i in range(1, number_of_pages):
            list_urls.append(base_url + str(i * Website.page_offset))

        return list_urls

    def get_all_data(self):
        """
        Extracts all data from all pages

        :return: list of lists of dictionaries, number of total pages, number of failed pages
        :rtype: tuple
        """
        pages_url_list = self._get_urls()
        print(f"Got {len(pages_url_list)} pages. Starting to process...")
        data_list = []
        for page_url in pages_url_list:
            data_list.append(Page(page_url, self._driver).get_data())
        number_of_pages = len(pages_url_list)
        number_of_failed_pages = Page.failed_pages
        return data_list, number_of_pages, number_of_failed_pages

    def teardown(self):
        """
        closes the webdriver
        """
        self._driver.quit()
