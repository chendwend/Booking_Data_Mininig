import re
from utilities.config import *
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class Page:
    """
    A Class to represent each page in a search result
    """
    failed_pages = 0
    url_number = 1

    def __init__(self, search_page, driver):
        """
        Constructs all the necessary attributes for the Page object.

        :param search_page: the URL of the page
        :type search_page: str
        :param driver: a webdriver object
        """
        self._search_page = search_page
        self._driver = driver
        self._driver.get(search_page)
        self._features = []

    def get_elements(self, base_element, selector_string=MAIN_STRING):
        """
        gets all elements from a webdriver from the given base element and selector string

        :param base_element: a Webdriver element in which to search for the selector
        :param selector_string: the selector string by which to search for specific elements
        :type selector_string: str
        :return: list of elements
        :rtype: list
        """
        try:
            elements = WebDriverWait(base_element, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_string))
            )
        except TimeoutException:
            self._driver.quit()
            sys.exit(
                f"Failed to find {selector_string} in url {self._search_page} or Timeout= {SEC_TO_WAIT} seconds passed.")
        return elements

    @staticmethod
    def get_element(base_element, selector_string=MAIN_STRING):
        """
        gets an element from a webdriver from the given base element and selector string

        :param base_element: a Webdriver element in which to search for the selector
        :param selector_string: the selector string by which to search for specific element
        :type selector_string: str
        :return: webdriver element
        """
        try:
            element = WebDriverWait(base_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_string))
            )
        except TimeoutException:
            element = ""
        return element

    def extract_upper_data(self, upper_elements):
        """
        Extracts the data from the upper part of each possible location

        :param upper_elements: list of webdriver elements representing each upper part
        :type upper_elements: list
        :return: list of dictionaries with the data, for each location
        :rtype: list
        """
        empty_dict = {}
        data_list = []
        for element in upper_elements:
            single_data_dict = empty_dict.copy()
            for data_name, (data_string, data_regex) in DATA_TYPES_UPPER.items():
                try:
                    single_data_dict[data_name] = re.search(data_regex,
                                                            self.get_element(element, data_string).text).group()
                except AttributeError:  # in case data is missing in the element
                    single_data_dict[data_name] = "empty"
            data_list.append(single_data_dict)
        return data_list

    def extract_lower_data(self, lower_elements):
        """
        Extracts the data from the lower part of each possible location

        :param lower_elements: list of webdriver elements representing each lower part
        :type lower_elements: list
        :return: list of dictionaries with the data, for each location
        :rtype: list
        """
        list_of_prices = []
        max_persons_elements_list = []
        empty_list = []
        lower_data = empty_list.copy()
        for lower_element in lower_elements:
            price = lower_element.find_elements_by_css_selector(PRICE_STRING)
            price = price[1].text
            list_of_prices.append(price)

            max_persons_elements_list.append(self.get_element(lower_element, MAX_PERSONS_STRING))

        prices = [int(re.search(PRICE_REGEX, price).group().replace(',', ''))
                  if price else "empty"
                  for price in list_of_prices]

        max_persons_full_string = [element.text for element in max_persons_elements_list]

        max_persons = [re.search(MAX_PERSONS_REGEX, unfiltered).group()
                       if unfiltered else "empty"
                       for unfiltered in max_persons_full_string]

        if len(prices) != len(max_persons):
            return lower_data

        lower_data = [{"price": price, "max persons": max_person} for price, max_person in zip(prices, max_persons)]
        return lower_data

    def get_data(self):
        """
        Extracts data from the page by combining lower & upper parts to single dictionary, for each location.

        :return: list of dictionaries for each location
        :rtype: list
        """
        data = []
        print(f"processing page number {Page.url_number}... \n {BAR}")
        Page.url_number += 1
        main_element = self.get_element(self._driver)
        upper_elements, lower_elements = self.get_elements(main_element, UPPER_STRING), \
                                         self.get_elements(main_element, LOWER_STRING)
        if len(upper_elements) != len(lower_elements):  # when encountered a mismatch, it's an irregular page
            Page.failed_pages += 1
            return data

        upper_data, lower_data = self.extract_upper_data(upper_elements), self.extract_lower_data(lower_elements)
        if not lower_data or not upper_data:  # when either lower or upper failed to acquire data, irregular page
            Page.failed_pages += 1
            return data
        for first, second in zip(upper_data, lower_data):
            first.update(second)
            data.append(first)

        return data
