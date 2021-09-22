from utilities.config import SEC_TO_WAIT, DEFAULT_VALUE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
# import sys


class Element:

    def __init__(self, driver):
        self._driver = driver

    def get_elements(self, base_element, selector_dict, on_exception="continue"):
        try:
            elements = WebDriverWait(base_element, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_dict["selector"]))
            )
        except TimeoutException:
            if on_exception == "continue":
                return DEFAULT_VALUE
            else:
                exit(
                    f"Failed to find {selector_dict['name']} with selector {selector_dict['selector']} "
                    f"after {SEC_TO_WAIT} seconds.\nURL: \n {self._driver.current_url}")
        return elements

    def get_element_by_name(self, base_element, selector_dict, on_exception="continue"):
        try:
            element = WebDriverWait(base_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located((By.NAME, selector_dict["selector"]))
            )
        except TimeoutException:
            if on_exception == "continue":
                return DEFAULT_VALUE
            else:
                exit(
                    f"Failed to find {selector_dict['name']} with selector {selector_dict['selector']} "
                    f"after {SEC_TO_WAIT} seconds.\nURL: \n {self._driver.current_url}")
        return element

    def get_element_by_css(self, base_element, selector_dict, on_exception="continue"):
        try:
            element = WebDriverWait(base_element, SEC_TO_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_dict["selector"]))
            )
        except TimeoutException:
            if on_exception == "continue":
                return DEFAULT_VALUE
            else:
                exit(
                    f"Failed to find {selector_dict['name']} with selector {selector_dict['selector']} "
                    f"after {SEC_TO_WAIT} seconds.\nURL: \n {self._driver.current_url}")
        return element

    def click_button(self, button_dict):
        """
        Finds and clicks button.
        Upon failure to find the button, stops the program.
        """
        try:
            search_button = WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, button_dict["selector"]))
            )
            search_button.click()
        except TimeoutException:
            self._driver.quit()
            exit(f"Failed to find {button_dict['name']} with selector {button_dict['selector']} after {SEC_TO_WAIT}"
                     f"seconds.\nURL: \n {self._driver.current_url}")
