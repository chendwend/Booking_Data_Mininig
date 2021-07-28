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
    LOCATIONS_LOCATOR = (By.CLASS_NAME, IDENTIFIER_LOCATIONS)
    NAME_LOCATOR = (By.CLASS_NAME, IDENTIFIER_NAME)
    SUB_LOCATION_LOCATOR = (By.CLASS_NAME, IDENTIFIER_SUB_LOCATION)
    PRICE_LOCATOR = (By.CLASS_NAME, IDENTIFIER_PRICE)
    RATING_LOCATOR = (By.CLASS_NAME, IDENTIFIER_RATING)
    REVIEWER_AMOUNT_LOCATOR = (By.CLASS_NAME, IDENTIFIER_REVIEWERS_AMOUNT)

    def __init__(self, search_page):
        self._search_page = search_page
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--blink-settings=imagesEnabled=false")
        self._driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
        # page = requests.get(self._search_page, headers={"User-Agent": USER_AGENT})
        # soup = BeautifulSoup(page.content, PARSER)
        # self._stays = soup.findAll(LOCATIONS[TAG], {LOCATIONS[TYPE]: LOCATIONS[ID]})[:-1]  # last element isn't location
        # if not self._stays:
        #     sys.exit(f"The following location tagging was not found: {LOCATIONS[TAG], LOCATIONS[TYPE], LOCATIONS[ID]}")
        self._features = []
        self._stays = []

    def extract_locations(self, attempts=DEFAULT_NUMBER_OF_ATTEMPTS):
        answer = requests.get(self._search_page, timeout=5)
        soup = BeautifulSoup(answer.content, PARSER)
        stays = soup.findAll(IDENTIFIER_LOCATIONS[TAG], {IDENTIFIER_LOCATIONS[TYPE]: IDENTIFIER_LOCATIONS[ID]})
        if not stays:
            sys.exit("didn't find location elements")

        # try:
        #     stays = WebDriverWait(self._driver, SEC_TO_WAIT).until(
        #         EC.presence_of_all_elements_located(Page.LOCATIONS_LOCATOR)
        #     )
        # except TimeoutException:
        #     self._driver.quit()
        #     sys.exit(f"Failed to find locations in url {self._search_page} or Timeout= {SEC_TO_WAIT} seconds passed.")
        return stays

    # @staticmethod
    def extract_features_per_location(self, stays_element):
        # # name
        # try:
        #     name = WebDriverWait(self._driver, SEC_TO_WAIT).until(
        #         EC.presence_of_all_elements_located(Page.NAME_LOCATOR)
        #     )
        # except TimeoutException:
        #     self._driver.quit()
        #     sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")
        #
        # # sub location
        # try:
        #     sub_location = WebDriverWait(self._driver, SEC_TO_WAIT).until(
        #         EC.presence_of_all_elements_located(Page.SUB_LOCATION_LOCATOR)
        #     )
        # except TimeoutException:
        #     self._driver.quit()
        #     sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")
        # # price
        # try:
        #     price = WebDriverWait(self._driver, SEC_TO_WAIT).until(
        #         EC.presence_of_all_elements_located(Page.PRICE_LOCATOR)
        #     )
        # except TimeoutException:
        #     self._driver.quit()
        #     sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")
        #
        # # rating
        # try:
        #     rating = WebDriverWait(self._driver, SEC_TO_WAIT).until(
        #         EC.presence_of_all_elements_located(Page.RATING_LOCATOR)
        #     )
        # except TimeoutException:
        #     self._driver.quit()
        #     sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")
        #
        # # reviewers amount
        # try:
        #     reviewers_amount = WebDriverWait(self._driver, SEC_TO_WAIT).until(
        #         EC.presence_of_all_elements_located(Page.REVIEWER_AMOUNT_LOCATOR)
        #     )
        # except TimeoutException:
        #     self._driver.quit()
        #     sys.exit(f"Failed to find the name or Timeout= {SEC_TO_WAIT} seconds passed.")



        try:
            name = stays_element.find(FEATURES_DICT["name"][TAG], {FEATURES_DICT["name"][TYPE]: FEATURES_DICT["name"][ID]}).get_text()
        except AttributeError:
            sys.exit(f"{FEATURES_DICT['name'][ID]} not found in {self._search_page}")
            name = 'empty'
        try:
            sub_location = stays_element.find(FEATURES_DICT["sub_location"][TAG], {FEATURES_DICT["sub_location"][TYPE]: FEATURES_DICT["sub_location"][ID]}).get_text()
        except AttributeError:
            sub_location = 'empty'
        try:
            price_full_string = stays_element.find(FEATURES_DICT["price"][TAG], {FEATURES_DICT["price"][TYPE]: FEATURES_DICT["price"][ID]}).get_text()
            price = re.search(PRICE_REGEX, price_full_string).group()
        except AttributeError:
            price = 'empty'
        try:
            rating_full_string = stays_element.find(FEATURES_DICT["rating"][TAG], {FEATURES_DICT["rating"][TYPE]: FEATURES_DICT["rating"][ID]}).get_text()
            rating = re.findall(RATING_REGEX, rating_full_string)[1]
        except AttributeError:
            rating = 'empty'
        try:
            reviewers_amount_full_string = stays_element.find(FEATURES_DICT["reviewers_amount"][TAG], {FEATURES_DICT["reviewers_amount"][TYPE]: FEATURES_DICT["reviewers_amount"][ID]}).get_text()
            reviewers_amount = re.search(REVIEWERS_REGEX, reviewers_amount_full_string).group()
        except AttributeError:
            reviewers_amount = 'empty'
        # guests_amount = stays_element.find(FEATURES_DICT["guests_amount"][TAG], {FEATURES_DICT["guests_amount"][TYPE]: FEATURES_DICT["guests_amount"][ID]}).get_text()
        # wifi = stays_element.find(FEATURES_DICT["wifi"][TAG], {FEATURES_DICT["wifi"][TYPE]: FEATURES_DICT["wifi"][ID]}).get_text()
        features = {
            # "url": url,
            "name": name,
            "sub_location": sub_location,
            "price": price,
            "rating": rating,
            "reviewers_amount": reviewers_amount
            # "guests_amount": guests_amount,
            # "wifi": wifi
        }
        return features

    def get_features(self):
        self._stays = self.extract_locations()
        self._features = [Page.extract_features_per_location(self, stays_element) for stays_element in self._stays]
        return self._features



# a = Page(PAGE_URL)
# a.get_stays_elements()
# features = a.get_features()
# print(features)


