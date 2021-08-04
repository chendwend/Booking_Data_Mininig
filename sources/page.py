#  accepts a page URL and extracts a list of links of locations

import re
from utilities.config import *
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import os


class Page:
    stays_selector = (By.CSS_SELECTOR, STAYS_STRING)
    name_selector = (By.CSS_SELECTOR, FEATURES_DICT["name"])
    location_selector = (By.CSS_SELECTOR, FEATURES_DICT["location"])
    price_selector = (By.XPATH, FEATURES_DICT["price"])
    rating_selector = (By.CSS_SELECTOR, FEATURES_DICT["rating"])
    reviewers_amount_selector = (By.CSS_SELECTOR, FEATURES_DICT["reviewers_amount"])
    beds_selector = (By.CSS_SELECTOR, FEATURES_DICT["beds"])
    main_selector = (By.CSS_SELECTOR, MAIN_STRING)

    def __init__(self, search_page, driver):
        self._search_page = search_page
        self._driver = driver
        self._driver.get(search_page)
        self._features = []

    def extract_locations(self):
        print(self._driver.current_url)
        try:
            stays = WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located(Page.stays_selector)
            )
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find locations in url {self._search_page} or Timeout= {SEC_TO_WAIT} seconds passed.")
        return stays

    def get_price_accommodation(self):
        price_accommodation = self._driver.find_elements_by_css_selector(".bui-u-sr-only")[3:]
        prices = price_accommodation[1::2]
        accommodations = price_accommodation[0::2]
        return prices, accommodations

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
        try:
            location = WebDriverWait(stays_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located(Page.location_selector)
            ).text.split()[:-2]
        except TimeoutException:
            # self._driver.quit()
            print(f"Failed to find the sub_location or Timeout= {SEC_TO_WAIT} seconds passed.")

        # rating
        try:
            rating = float(WebDriverWait(stays_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located(Page.rating_selector)
            ).text)
        except TimeoutException:
            rating = 0

        # reviewers amount
        try:
            reviewers_amount_full = WebDriverWait(stays_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located(Page.reviewers_amount_selector)
            ).text
            reviewers_amount = int(re.search(REVIEWERS_REGEX, reviewers_amount_full).group())
        except TimeoutException:
            reviewers_amount = 0

        self._driver.get_screenshot_as_file(os.getcwd() + "/Selenium0.png")

        features = {
            # "url": url,
            "name": name,
            "location": location,
            # "price": price,
            "rating": rating,
            "reviewers_amount": reviewers_amount
            # "beds": beds
            # "guests_amount": guests_amount,
            # "wifi": wifi
        }
        return features

    def get_features(self):
        basic_info_list = self.extract_locations()
        prices, accommodations = self.get_price_accommodation()
        index = 0
        for stays_element in basic_info_list:
            features = self.extract_features_per_location(stays_element)
            price = prices[index].text
            accommodation = accommodations[index].text
            print(f"price = {price}, accommodation = {accommodation}")
            if "Max" in price:
                features["price"] = int(re.search(NUMBERS_REGEX, accommodations[index].text).group())
                features["accommodation"] = int(re.search(NUMBERS_REGEX, price[index].text).group())
            else:
                features["price"] = int(re.search(NUMBERS_REGEX, prices[index].text).group())
                features["accommodation"] = int(re.search(NUMBERS_REGEX, accommodations[index].text).group())
            self._features.append(features)
            index += 1
        return self._features
