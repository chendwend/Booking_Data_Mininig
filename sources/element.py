from utilities.config import SEC_TO_WAIT
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class Element:

    def __init__(self, driver):
        self._driver = driver

    def get_elements(self, base_element, selector_string):
        try:
            elements = WebDriverWait(base_element, SEC_TO_WAIT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_string))
            )
        except TimeoutException:
s            sys.exit(
                f"Failed to find {selector_string} in url {self._driver.current_url} "
                f"after {SEC_TO_WAIT} seconds.")
        return elements

    def get_element(self, base_element, selector_string, selector_type="class"):
        if selector_type == "class":
            try:
                element = WebDriverWait(base_element, SEC_TO_WAIT).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector_string))
                )
            except TimeoutException:
                sys.exit(
                    f"Failed to find {selector_string} in url {self._driver.current_url} "
                    f"after {SEC_TO_WAIT} seconds.")
        else:
            try:
                element = WebDriverWait(base_element, SEC_TO_WAIT).until(
                    EC.presence_of_element_located((By.NAME, selector_string))
                )
            except TimeoutException:
                sys.exit(
                    f"Failed to find {selector_string} in url {self._driver.current_url} "
                    f"after {SEC_TO_WAIT} seconds.")
        return element

    def click_button(self, button_string):
        """
        Finds and clicks button.
        Upon failure to find the button, stops the program.
        """
        try:
            search_button = WebDriverWait(self._driver, SEC_TO_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, button_string))
            )
            search_button.click()
        except TimeoutException:
            self._driver.quit()
            sys.exit(f"Failed to find the button {button_string} in url {self._driver.current_url} "
                     f"or Timeout= {SEC_TO_WAIT} seconds passed.")
