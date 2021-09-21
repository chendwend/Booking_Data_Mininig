from utilities.config import ROOM_FACILITIES, FACILITY_STRING_LIST, EMPTY_ROOM_FACILITIES, SERVICE_AVAILABILITY
from sources.element import Element


class PlaceOfStay(Element):
    failed_room_facilities = 0

    def __init__(self, driver):
        """
        Constructs all the necessary attributes for the Place_of_stay object.

        :param driver: a webdriver object
        """
        self._driver = driver

    @staticmethod
    def extract_service(element, selector_string):
        """
        Checks if the string selector_string is present in the element.

        :param element: selenium object
        :param selector_string: a string to search for the required service
        :type selector_string: str
        :return: the appropriate SERVICE_AVAILABILITY constant from config.py
        :rtype: int
        """
        condition = selector_string in element.text.lower()
        return SERVICE_AVAILABILITY["yes"] if condition else SERVICE_AVAILABILITY["no"]

    def extract_data(self):
        """
        Extracts all services from place of stay.
        If not selector is detected out of known list, a default dictionary is returned

        :return: a dictionary with service name and availability
        :rtype: dict
        """
        room_facilities = {}
        for index, selector in enumerate(FACILITY_STRING_LIST):
            try:
                element = self.get_elements(self._driver, selector[0], "continue")[selector[1]]
                break
            except TypeError:
                if index == len(FACILITY_STRING_LIST) - 1:  # if no selectors are found, return default dictionary
                    PlaceOfStay.failed_room_facilities += 1
                    return EMPTY_ROOM_FACILITIES.copy()
                continue
        {service: self.extract_service(element, selector_string) for service, selector_string in ROOM_FACILITIES.items()}
        return room_facilities
