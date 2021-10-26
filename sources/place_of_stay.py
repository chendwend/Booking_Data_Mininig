from utilities.config import ROOM_FACILITIES, SERVICE_AVAILABILITY, FACILITY
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
        element = self.get_element_by_css(self._driver, FACILITY, "continue")
        room_facilities.update({service: self.extract_service(element, selector_string) for service, selector_string in ROOM_FACILITIES.items()})
        return room_facilities
