from utilities.config import *
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import MaxRetryError
from selenium.webdriver.common.by import By
from sources.element import Element


class PlaceOfStay(Element):

    def __init__(self, driver):
        """
        Constructs all the necessary attributes for the Place_of_stay object.

        :param driver: a webdriver object
        """
        self._driver = driver

    @staticmethod
    def extract_service(element, selector_string):
        condition = selector_string in element.text.lower()
        return 1 if condition else 0

    def extract_data(self):
        room_facilities = {}
        try:
            element = self._driver.find_elements_by_css_selector(FACILITY_STRING)[1]  # facilities element
        except MaxRetryError:
            try:
                element = self._driver.find_element_by_css_selector(FACILITY_STRING2)
            except MaxRetryError:
                print(f"Failed to find both in {self._driver.current_url}")
                sys.exit()
                return [None]*len(ROOM_FACILITIES)
        except IndexError:
            element = self._driver.find_elements_by_css_selector(FACILITY_STRING)[0]
        for service, selector_string in ROOM_FACILITIES.items():
            room_facilities[service] = self.extract_service(element, selector_string)
        return room_facilities
