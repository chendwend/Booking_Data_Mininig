from utilities.config import *
from sources.element import Element
from sources.place_of_stay import PlaceOfStay
from selenium.common.exceptions import ElementNotInteractableException
import re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import pandas as pd


class Page(Element):
    """
    A Class to represent each page in a search result
    """
    sub_location_number = 1
    failed_pages = 0
    lower_upper_mismatches = 0
    failed_stays = 0
    max_num_sub_locations = 25
    tricky_page_count = 0
    number_of_sub_locations = 0
    page_number = 1

    def __init__(self, driver):
        """
        Constructs all the necessary attributes for the Page object.

        :param driver: a webdriver object
        """
        self._driver = driver

    @staticmethod
    def _clean_data(data_list, data_type):
        """
        Clears the data from any unwanted additional strings based on type of service
        :param data_list: a list of all of that type of service value for all stays
        :type data_list: list
        :param data_type: the type of service to be filtered
        :type data_type: str
        :return: filtered list of the type of service
        :rtype: list
        """

        data_list_filtered = data_list
        if data_type == "price":
            data_list_filtered = [int(re.search(REGEX_DATA_DICT["price"], data).group().replace(',', ''))
                                  if data else DEFAULT_VALUE
                                  for data in data_list]
        elif data_type == "reviewers amount":
            data_list_filtered = [int(re.search(REGEX_DATA_DICT["reviewers amount"], data).group())
                                  if data else DEFAULT_VALUE
                                  for data in data_list]
        elif data_type == "rating":
            data_list_filtered = [float(data) for data in data_list]
        elif data_type == "sub location":
            data_list_filtered = [data[data.find(',') + 1:data.find('Show')]
                                  if data.find(',') != -1 else data[0:data.find('Show')]
                                  for data in data_list]
        return data_list_filtered

    def extract_room_facilities(self):
        """
        Extracts room facilities information for each stays in the page
        :return: list of dictionaries corresponding for each stay
        :rtype: list
        """
        room_facilities_elements = [element for element in
                                    self.get_elements(self._driver, SUB_LOCATION_FACILITIES, "continue")]
        if room_facilities_elements == DEFAULT_VALUE:
            room_facilities = [EMPTY_ROOM_FACILITIES.copy()] * Page.number_of_sub_locations
            return room_facilities
        window_before = self._driver.window_handles[0]
        room_facilities = []
        for element in room_facilities_elements:  # click to move to each stays' page
            try:
                element.click()
                window_after = self._driver.window_handles[1]
                self._driver.switch_to_window(window_after)
                place_of_stay_obj = PlaceOfStay(self._driver)
                room_facilities.append(place_of_stay_obj.extract_data())
            except ElementNotInteractableException:  # if not clickable, return dictionary of default values
                room_facilities.append(EMPTY_ROOM_FACILITIES.copy())
            self._driver.close()
            self._driver.switch_to_window(window_before)
        return room_facilities

    @staticmethod
    def _arrange_data(list_of_facilities_dict, page_data_list):
        """
        Accepts the data gathered from the page and its stays and arranges in a pandas dataframe
        :param list_of_facilities_dict: list of dictionaries
        :type list_of_facilities_dict: list
        :param page_data_list:
        :return: dataframe
        """
        df = pd.DataFrame(data=page_data_list, index=PAGE_DATA_DICT.keys())
        df = df.transpose()
        pets, wifi, kitchen, parking, air_conditioning = [], [], [], [], []
        for stay_facilities in list_of_facilities_dict:
            pets.append(stay_facilities["pets"])
            wifi.append(stay_facilities["wifi"])
            kitchen.append(stay_facilities["kitchen"])
            parking.append(stay_facilities["parking"])
            air_conditioning.append(stay_facilities["air conditioning"])
        df_new = pd.DataFrame({"pets": pets, "wifi": wifi, "kitchen": kitchen, "parking": parking, "air conditioning": air_conditioning})
        df = pd.concat([df, df_new], axis=1)
        return df

    def get_data(self):
        """
        Extracts all data from the page, including information in the 'availability' option
        :return: a pandas DataFrame with columns as a stay service, records as stays
        """
        data = []
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        for data_type, data_selector in PAGE_DATA_DICT.items():
            elements = WebDriverWait(self._driver, SEC_TO_WAIT, ignored_exceptions=ignored_exceptions) \
                .until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, data_selector)))
            original_data_text_list = [element.text for element in elements]
            filtered_data_list = self._clean_data(original_data_text_list, data_type)
            data.append(filtered_data_list)
        facilities_list = self.extract_room_facilities()

        return self._arrange_data(facilities_list, data)
