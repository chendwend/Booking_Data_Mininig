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
            elements = WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, FACILITY_STRING))
            )
            print(len(elements))
            element = elements[-1]
            print(f"found {FACILITY_STRING}")
        except TimeoutException:
            try:
                element = self._driver.find_element_by_css_selector(FACILITY_STRING2)
                print(f"found {FACILITY_STRING2}")
            except TimeoutException:
                print(f"Failed to find all in {self._driver.current_url}")
                return [-1]*len(ROOM_FACILITIES)
        for service, selector_string in ROOM_FACILITIES.items():
            room_facilities[service] = self.extract_service(element, selector_string)
        return room_facilities
