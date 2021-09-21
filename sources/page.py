import re
from utilities.config import *
from sources.element import Element
from sources.place_of_stay import PlaceOfStay
from selenium.common.exceptions import ElementNotInteractableException
from urllib3.exceptions import MaxRetryError


class Page(Element):
    """
    A Class to represent each page in a search result
    """
    sub_location_number = 1
    failed_pages = 0
    lower_upper_mismatches = 0
    failed_stays = 0

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
        for element in upper_elements:  # run on all upper elements
            single_data_dict = empty_dict.copy()
            for data_dict, regex in zip(DATA_TYPES_UPPER, DATA_TYPES_UPPER_REGEX):  # run on all types of data
                singular_data_element = self.get_element_by_css(element, data_dict, on_exception="continue")
                single_data_dict[data_dict["name"]] = re.search(regex, singular_data_element.text).group() if \
                    (singular_data_element != DEFAULT_VALUE) else DEFAULT_VALUE
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
        empty_list = []
        list_of_prices = empty_list.copy()
        max_people_full_string = empty_list.copy()
        policies_original = empty_list.copy()
        lower_data = empty_list.copy()
        #########################################################
        #  First stage parsing - creating lists of unfiltered data
        #########################################################
        for lower_element in lower_elements:
            # locates elements for each category
            try:
                price = lower_element.find_elements_by_css_selector(PRICE_STRING)
                price = price[1].text
            except MaxRetryError:
                price = DEFAULT_VALUE
            try:
                policy = lower_element.find_element_by_css_selector(POLICY_STRING)
                policies_original.append(policy.text)
            except MaxRetryError:
                policies_original.append(DEFAULT_VALUE)
            # parse data (when required) and append to a list
            # non-unique element
            list_of_prices.append(price)
            max_people_element = self.get_element_by_css(lower_element, MAX_PEOPLE, on_exception="continue")
            if max_people_element != DEFAULT_VALUE:
                max_people_full_string.append(max_people_element.text)
            else:
                max_people_full_string.append(DEFAULT_VALUE)
            # each policy.text is a string of all policies for that lower element
        #########################################################
        #  Second stage parsing - Filtering data for each list
        #########################################################
        breakfasts = [1 if (BREAKFAST_STRING in policy.lower()) else 0 for policy in policies_original]
        free_cancellations = \
            [1 if (FREE_CANCELLATION_STRING in policy.lower()) else 0 for policy in policies_original]
        prices = [int(re.search(PRICE_REGEX, price).group().replace(',', ''))
                  if price else DEFAULT_VALUE
                  for price in list_of_prices]
        # max_people_full_string = [element.text for element in max_people_elements_list]

        max_people = [re.search(MAX_PERSONS_REGEX, unfiltered).group()
                      if unfiltered != DEFAULT_VALUE else DEFAULT_VALUE
                      for unfiltered in max_people_full_string]

        if len(prices) != len(max_people):
            return lower_data

        lower_data = [
            {"Price": price, "Max people": people, "Breakfast": breakfast, "Free Cancellations": free_cancellation}
            for
            price, people, breakfast, free_cancellation in zip(prices, max_people, breakfasts, free_cancellations)]
        return lower_data

    def extract_room_facilities(self):
        """
        Extracts room facilities information for each stays in the page
        :return: list of dictionaries corresponding for each stay
        :rtype: list
        """
        room_facilities_elements = [element for element in
                                    self.get_elements(self._driver, SUB_LOCATION_FACILITIES, "continue")]
        window_before = self._driver.window_handles[0]
        room_facilities = []
        for element in room_facilities_elements:  # click to move to each stays' page
            try:
                element.click()
            except ElementNotInteractableException:  # if not clickable, return dictionary of default values
                room_facilities.append(EMPTY_ROOM_FACILITIES.copy())
            window_after = self._driver.window_handles[1]
            self._driver.switch_to_window(window_after)
            place_of_stay_obj = PlaceOfStay(self._driver)
            room_facilities.append(place_of_stay_obj.extract_data())
            self._driver.close()
            self._driver.switch_to_window(window_before)
        return room_facilities

    def get_data(self):
        """
        1. locates main element in the page containing all stays
        2. locates upper & lower elements for each stay
        3. extracts data corresponding for lower & upper elements
        4. extracts room facilities data for each stay
        4. Creates a unified dictionary containing all extracted data for the page

        :return: list of dictionaries for each location
        :rtype: list
        """
        data = []  # This will hold all acquired data for each site in the current page

        main_element = self.get_element_by_css(self._driver, MAIN_PAGE,
                                               on_exception="continue")  # acquires element containing only sites
        if main_element == DEFAULT_VALUE:  #
            Page.failed_pages += 1
            return data
        # lists of upper & lower elements for each stay:
        upper_elements, lower_elements = \
            self.get_elements(main_element, UPPER, on_exception="continue"), \
            self.get_elements(main_element, LOWER, on_exception="continue")

        if len(upper_elements) != len(lower_elements):  # when encountered a mismatch, it's an irregular page
            Page.lower_upper_mismatches += 1
            return data

        upper_data, lower_data = self.extract_upper_data(upper_elements), self.extract_lower_data(lower_elements)
        if not lower_data or not upper_data:  # when either lower or upper failed to acquire data, irregular page
            Page.failed_pages += 1
            return data

        room_facilities = self.extract_room_facilities()
        number_of_sub_locations = len(upper_data)
        for upper, lower, room in zip(upper_data, lower_data, room_facilities):
            # print(f"processing sub location number {Page.sub_location_number}/{number_of_sub_locations}")
            upper.update(lower)
            upper.update(room)
            if upper["name"] != -1 and upper["sub location"] != -1:
                data.append(upper)
            else:
                self.failed_stays += 1
            Page.sub_location_number += 1
        Page.sub_location_number = 1
        return data
