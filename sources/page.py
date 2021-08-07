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

    def __init__(self, search_page, driver):
        self._search_page = search_page
        self._driver = driver
        self._driver.get(search_page)
        self._features = []

    def get_elements(self, base_element, selector_string=MAIN_STRING):
        try:
            elements = WebDriverWait(base_element, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_string))
            )
        except TimeoutException:
            self._driver.quit()
            sys.exit(
                f"Failed to find {selector_string} in url {self._search_page} or Timeout= {SEC_TO_WAIT} seconds passed.")
        return elements

    def get_element(self, base_element, selector_string=MAIN_STRING):
        try:
            element = WebDriverWait(base_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_string))
            )
        except TimeoutException:
            element = ""
        return element

    def extract_upper_data(self, upper_elements):
        single_data_dict = {}
        data_list = []
        for element in upper_elements:
            for data_name, (data_string, data_regex) in DATA_TYPES_UPPER.items():
                try:
                    single_data_dict[data_name] = re.search(data_regex, self.get_element(element, data_string).text).group()
                except AttributeError:
                    single_data_dict[data_name] = "empty"
            data_list.append(single_data_dict)
        return data_list

    def extract_lower_data(self, lower_elements):
        list_of_prices = []
        max_persons_elements_list = []
        for lower_element in lower_elements:
            price = lower_element.find_elements_by_css_selector(PRICE_STRING)
            price = price[1].text
            if not price:  # orange price
                price = self.get_element(lower_element, ".tpi_price_label tpi_price_label__orange")
                print(f"orange price = {price}")
            list_of_prices.append(price)

            max_persons_elements_list.append(self.get_element(lower_element, MAX_PERSONS_STRING))

        try:
            prices = [int(re.search(PRICE_REGEX, price).group().replace(',', ''))
                      if price else "empty"
                      for price in list_of_prices]
        except AttributeError:
            self._driver.quit()
            sys.exit(f"Encountered a NoneType for prices in {self._search_page}.")

        # max_persons_elements_list = [self.get_element(lower_element, MAX_PERSONS_STRING) for lower_element in lower_elements]
        max_persons_full_string = [element.text for element in max_persons_elements_list]
        try:
            max_persons = [re.search(MAX_PERSONS_REGEX, unfiltered).group()
                           if unfiltered else "empty"
                           for unfiltered in max_persons_full_string]
        except AttributeError:
            print(f"len(max_persons_full_string)={len(max_persons_full_string)}")
            self._driver.quit()
            sys.exit(f"Encountered a NoneType for max_persons in {self._search_page}.")

        if len(prices) != len(max_persons):
            self._driver.quit()
            print(f"len(prices) = {len(prices)}, len(persons)={len(max_persons)}")
            sys.exit(f"lengths of prices & max_persons don't match in URL={self._search_page}.")
        lower_data = [{"price": price, "max persons": max_person} for price, max_person in zip(prices, max_persons)]
        return lower_data

    def get_data(self):
        print(f"processing URL:\n {self._search_page}... \n -------------------------------")
        main_element = self.get_element(self._driver)
        upper_elements, lower_elements = self.get_elements(main_element, UPPER_STRING), \
                                         self.get_elements(main_element, LOWER_STRING)
        if len(upper_elements) != len(lower_elements):
            self._driver.quit()
            sys.exit(f"lengths of lower and upper elements don't match in URL={self._search_page}.")

        upper_data, lower_data = self.extract_upper_data(upper_elements), self.extract_lower_data(lower_elements)
        data = []
        for first, second in zip(upper_data, lower_data):
            first.update(second)
            data.append(first)

        return data

