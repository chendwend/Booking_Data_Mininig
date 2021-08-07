from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.config import *
from sources.page import Page
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time
import sys
import re


class Website:
    SEARCH_BUTTON_SELECTOR = (By.CLASS_NAME, SEARCH_BUTTON_STRING)
    SEARCH_LOCATION_SELECTOR = (By.NAME, SEARCH_LOCATION_STRING)
    PAGE_BUTTONS_SELECTOR = (By.CSS_SELECTOR, PAGES_LINKS_STRING)
    SEC_TO_WAIT = 10
    page_offset = 25

    def __init__(self, main_url):
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument(f'user-agent={USER_AGENT}')
        self._driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
        self._driver.get(main_url)
        self._pages = []

    def enter_location(self, location):
        try:
            search_location = WebDriverWait(self._driver, Website.SEC_TO_WAIT).until(
                EC.presence_of_element_located(Website.SEARCH_LOCATION_SELECTOR)
            )
            search_location.send_keys(location)

        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the form for input or Timeout= {SEC_TO_WAIT} seconds passed.")

    def click_search_button(self):
        try:
            search_button = WebDriverWait(self._driver, Website.SEC_TO_WAIT).until(
                EC.presence_of_element_located(Website.SEARCH_BUTTON_SELECTOR)
            )
            search_button.click()
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the search button or Timeout= {SEC_TO_WAIT} seconds passed.")

    def select_date(self, start_date, end_date):
        try:
            WebDriverWait(self._driver, Website.SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".bui-calendar__date"))
            )
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the checkin field or Timeout= {SEC_TO_WAIT} seconds passed.")
        self._driver.find_element_by_css_selector(f"span[aria-label='{start_date.day} {start_date.strftime('%B')} {start_date.year}']").click()
        jack = self._driver.find_elements_by_css_selector(".sb-date-field__display")[1].click()
        self._driver.find_element_by_css_selector(f"span[aria-label='{end_date.day} {end_date.strftime('%B')} {end_date.year}']").click()
        # self._driver.find_element_by_css_selector("span[aria-label='11 August 2021']").click()
        self._driver.find_element_by_css_selector(".sb-searchbox__button ").click()

    def _get_urls(self):
        list_urls = []
        first_page_url = self._driver.current_url
        time.sleep(Website.SEC_TO_WAIT)
        list_urls.append(first_page_url)
        try:
            page_buttons = WebDriverWait(self._driver, Website.SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located(Website.PAGE_BUTTONS_SELECTOR)
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

    def get_all_features(self):
        pages_url_list = self._get_urls()
        features_list = []
        for page_url in pages_url_list:
            features_list.append(Page(page_url, self._driver).get_data())
        return features_list

    def teardown(self):
        self._driver.quit()





