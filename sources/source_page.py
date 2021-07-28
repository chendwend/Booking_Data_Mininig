from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.config import *
from sources.page import Page
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import sys
import re


class Website:
    SEARCH_BUTTON_LOCATOR = (By.CLASS_NAME, IDENTIFIER_SEARCH_BUTTON)
    # SEARCH_LOCATION_LOCATOR = (By.NAME, IDENTIFIER_SEARCH_LOCATION)
    SEARCH_LOCATION_LOCATOR = (By.CLASS_NAME, IDENTIFIER_SEARCH_LOCATION)
    PAGE_BUTTONS_LOCATOR = (By.CLASS_NAME, IDENTIFIER_PAGE_BUTTONS)
    SEC_TO_WAIT = 20

    def __init__(self, main_url):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--blink-settings=imagesEnabled=false")
        self._driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
        self._driver.get(main_url)
        self._pages = []

    def enter_location(self, location):
        try:
            search_location = WebDriverWait(self._driver, Website.SEC_TO_WAIT).until(
                EC.presence_of_element_located(Website.SEARCH_LOCATION_LOCATOR)
            )
            search_location.send_keys(location)
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the form for input or Timeout= {SEC_TO_WAIT} seconds passed.")

    def click_search_button(self):
        try:
            search_button = WebDriverWait(self._driver, Website.SEC_TO_WAIT).until(
                EC.presence_of_element_located(Website.SEARCH_BUTTON_LOCATOR)
            )
            search_button.click()
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the search button or Timeout= {SEC_TO_WAIT} seconds passed.")

    def _get_urls(self):
        list_urls = []
        first_page_url = self._driver.current_url
        time.sleep(Website.SEC_TO_WAIT)
        list_urls.append(first_page_url)
        try:
            page_buttons = WebDriverWait(self._driver, Website.SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located(Website.PAGE_BUTTONS_LOCATOR)
            )
            last_url = page_buttons[-1]
            last_offset_number = int(re.search(OFFSET_REGEX, last_url).group())
            last_equal_sign_index = last_url.rfind('=')
            base_url = last_url[:last_equal_sign_index]
            number_of_pages = last_offset_number/25 + 1
            for i in range(2, number_of_pages):
                list_urls.append(base_url + '=' + str(i*25))
            # number_of_pages_minus_one = len(page_buttons)  # pages 2..<last_page>
            # if number_of_pages_minus_one >= 1:
            #     page_buttons[number_of_pages_minus_one - 1].click()
            #     time.sleep(Website.SEC_TO_WAIT)
            #     url_page = self._driver.current_url  # last page
            #     time.sleep(Website.SEC_TO_WAIT)
            #     url_first_part = url_page.split("offset=")[0]
            #     url_second_part = url_page.split("offset=")[1]
            #     the_constant_offset = url_page.split("offset=")[2]
            #     the_last_offset = url_second_part.split("&")[0]
            #     the_third_part = url_second_part.split("&")[1]
            #     for j in range(MAX_STAYS_IN_PAGE, int(the_last_offset) + MAX_STAYS_IN_PAGE, MAX_STAYS_IN_PAGE):
            #         list_urls.append(
            #             url_first_part + "offset=" + str(j) + "&" + the_third_part + "offset=" + the_constant_offset)
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the page buttons or Timeout= {SEC_TO_WAIT} seconds passed.")
        return list_urls

    def get_all_features(self):
        pages_url_list = self._get_urls()
        self._pages = [Page(page_url) for page_url in pages_url_list]
        features_list = [page_obj.get_features() for page_obj in self._pages]
        return features_list

    def teardown(self):
        self._driver.quit()





