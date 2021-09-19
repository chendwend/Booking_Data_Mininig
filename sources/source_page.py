from selenium import webdriver
from utilities.config import PAGES_LINKS_STRING, USER_AGENT, SEARCH_LOCATION_STRING, SEARCH_BUTTON_STRING, \
    CALENDAR_STRING, OFFSET_REGEX
from sources.page import Page
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from re import search as search_regex
from sources.element import Element


class Website(Element):
    """
    A class to represent a booking.com website element.
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
        options.add_argument(f'user-agent={USER_AGENT}')  # Without this -> doesn't find pages
        self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self._driver.get(main_url)

    def insert_location(self, location):
        """
        1. Finds & inserts location into the search bar.
        2. Finds & clicks the search button
        Upon failure to find anyone of them, stops the program.

        :param location: the desired destination
        :type location: str
        """
        searchbar_element = self.get_element(self._driver, SEARCH_LOCATION_STRING, selector_type="name")
        searchbar_element.send_keys(location)
        self.click_button(SEARCH_BUTTON_STRING)

    def select_date(self, start_date, end_date):
        """
        Chooses the start & end dates of visit from the calendar and clicks search button.
        Upon failure to find the calendar, stops the program.

        :param start_date: the start date of visit
        :type start_date: datetime
        :param end_date: the end date of visit
        :type end_date: datetime
        """
        self.get_elements(self._driver, CALENDAR_STRING)
        self._driver.find_element_by_css_selector(
            f"span[aria-label='{start_date.day} {start_date.strftime('%B')} {start_date.year}']").click()
        self._driver.find_elements_by_css_selector(".sb-date-field__display")[1].click()
        self._driver.find_element_by_css_selector(
            f"span[aria-label='{end_date.day} {end_date.strftime('%B')} {end_date.year}']").click()
        self._driver.find_element_by_css_selector(SEARCH_BUTTON_STRING).click()

    def _get_urls(self):
        """
        Extracts list of URLs, each representing a page result.

        :return: list of URLs
        :rtype: list
        """
        list_urls = []
        first_page_url = self._driver.current_url
        list_urls.append(first_page_url)
        page_buttons = self.get_elements(self._driver, PAGES_LINKS_STRING)

        last_url = page_buttons[-1].get_attribute("href")
        last_offset_number = int(search_regex(OFFSET_REGEX, last_url).group())
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
        print(f"Found {len(pages_url_list)} pages. Starting to process...")
        data_list = []
        for page_url in pages_url_list[:2]:
            page = Page(page_url, self._driver)
            data = page.get_data()
            if data:
                data_list.append(data)
        number_of_pages = len(pages_url_list)
        number_of_failed_pages = Page.failed_pages
        number_of_failed_stays = Page.failed_stays
        return data_list, number_of_pages, number_of_failed_pages, number_of_failed_stays

    def teardown(self):
        """
        closes the webdriver
        """
        self._driver.quit()
