#  accepts a page URL and extracts a list of links of locations
import requests
from bs4 import BeautifulSoup
import re
from utilities.config import *
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class Page:
    stays_selector = (By.CSS_SELECTOR, STAYS_STRING)
    name_selector = (By.CSS_SELECTOR, FEATURES_DICT["name"])
    sub_location_selector = (By.CSS_SELECTOR, FEATURES_DICT["sub_location"])
    price_selector = (By.CLASS_NAME, IDENTIFIER_PRICE)
    rating_selector = (By.CSS_SELECTOR, FEATURES_DICT["rating"])
    reviewers_amount_selector = (By.CSS_SELECTOR, FEATURES_DICT["reviewers_amount"])

    def __init__(self, search_page, driver):
        self._search_page = search_page
        self._driver = driver
        self._driver.get(search_page)
        # self._driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
        # page = requests.get(self._search_page, headers={"User-Agent": USER_AGENT})
        # soup = BeautifulSoup(page.content, PARSER)
        # self._stays = soup.findAll(LOCATIONS[TAG], {LOCATIONS[TYPE]: LOCATIONS[ID]})[:-1]  # last element isn't location
        # if not self._stays:
        #     sys.exit(f"The following location tagging was not found: {LOCATIONS[TAG], LOCATIONS[TYPE], LOCATIONS[ID]}")
        self._features = []
        self._stays = []

    def extract_locations(self, attempts=DEFAULT_NUMBER_OF_ATTEMPTS):
        # answer = requests.get(self._search_page, timeout=5)
        # soup = BeautifulSoup(answer.content, PARSER)
        # stays = soup.findAll(IDENTIFIER_LOCATIONS[TAG], {IDENTIFIER_LOCATIONS[TYPE]: IDENTIFIER_LOCATIONS[ID]})
        # if not stays:
        #     sys.exit("didn't find location elements")
        print(self._driver.current_url)
        try:
            stays = WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located(Page.stays_selector)
            )
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find locations in url {self._search_page} or Timeout= {SEC_TO_WAIT} seconds passed.")
        return stays

    # @staticmethod
    def extract_features_per_location(self, stays_element):
        # name
        try:
            name = WebDriverWait(stays_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located(Page.name_selector)
            ).text
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")

        # sub location
        # sub_location = stays_element.get
        try:
            sub_location = WebDriverWait(stays_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located(Page.sub_location_selector)
            ).text
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")
        # price
        # try:
        #     price = WebDriverWait(self._driver, SEC_TO_WAIT).until(
        #         EC.presence_of_element_located(Page.price_selector)
        #     )
        # except TimeoutException:
        #     self._driver.quit()
        #     sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")

        # rating
        try:
            rating = WebDriverWait(stays_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located(Page.rating_selector)
            ).text
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")

        # reviewers amount
        try:
            reviewers_amount_full = WebDriverWait(stays_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located(Page.reviewers_amount_selector)
            ).text
            reviewers_amount = re.search(REVIEWERS_REGEX, reviewers_amount_full).group()
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")

        features = {
            # "url": url,
            "name": name,
            "sub_location": sub_location,
            # "price": price,
            "rating": rating,
            "reviewers_amount": reviewers_amount
            # "guests_amount": guests_amount,
            # "wifi": wifi
        }
        return features

    def get_features(self):
        self._stays = self.extract_locations()
        for stays_element in self._stays:
            self._features.append(Page.extract_features_per_location(self, stays_element))
        # self._features = [Page.extract_features_per_location(self, stays_element) for stays_element in self._stays]
        return self._features



