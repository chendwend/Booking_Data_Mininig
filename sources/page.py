#  accepts a page URL and extracts a list of links of locations
import requests
from bs4 import BeautifulSoup
import utilities.config as conf

PARSER = "html.parser"
PAGE_URL = "https://www.airbnb.com/s/Germany/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&query=Germany&place_id=ChIJa76xwh5ymkcRW-WRjmtd6HU"
# LOCATIONS_CLASS_ID = "_8s3ctt"
LOCATIONS = ("div", "class", "_12oal24")
FEATURES_DICT = {
    "name": ("span", "id", "title_42065955"),
    "sub_location": ("div", "class", "_1olmjjs6"),
    "price": ("span", "class", "_155sga30"),
    "rating": ("span", "class", "_10fy1f8"),
    "reviewers_amount": ("span", "class", "_a7a5sx"),
    "guests_amount": ("span", "class", "_3c0zz1"),
    "wifi": ("span", "class", "_3hmsj")

}
TAG, TYPE, ID = (0, 1, 2)


class Page:
    def __init__(self, search_page):
        self._search_page = search_page
        self._locations = []
        self._features = []

    def get_locations_elements(self):
        page = requests.get(self._search_page)
        soup = BeautifulSoup(page.content, PARSER)
        self._locations = soup.findAll(LOCATIONS[TAG], {LOCATIONS[TYPE]: LOCATIONS[ID]})
        a = 5

    @staticmethod
    def extract_features_per_location(location_element):
        # url = location_element.find('a').get('href')
        name = location_element.find(FEATURES_DICT["name"][TAG], {FEATURES_DICT["name"][TYPE]: FEATURES_DICT["name"][ID]}).get_text()
        sub_location = location_element.find(FEATURES_DICT["sub_location"][TAG], {FEATURES_DICT["sub_location"][TYPE]: FEATURES_DICT["sub_location"][ID]}).get_text()
        price = location_element.find(FEATURES_DICT["price"][TAG], {FEATURES_DICT["price"][TYPE]: FEATURES_DICT["price"][ID]}).get_text()
        rating = location_element.find(FEATURES_DICT["rating"][TAG], {FEATURES_DICT["rating"][TYPE]: FEATURES_DICT["rating"][ID]}).get_text()
        reviewers_amount = location_element.find(FEATURES_DICT["reviewers_amount"][TAG], {FEATURES_DICT["reviewers_amount"][TYPE]: FEATURES_DICT["reviewers_amount"][ID]}).get_text()
        guests_amount = location_element.find(FEATURES_DICT["guests_amount"][TAG], {FEATURES_DICT["guests_amount"][TYPE]: FEATURES_DICT["guests_amount"][ID]}).get_text()
        wifi = location_element.find(FEATURES_DICT["wifi"][TAG], {FEATURES_DICT["wifi"][TYPE]: FEATURES_DICT["wifi"][ID]}).get_text()
        features = {
            # "url": url,
            "name": name,
            "sub_location": sub_location,
            "price": price,
            "rating": rating,
            "reviewers_amount": reviewers_amount,
            "guests_amount": guests_amount,
            "wifi": wifi
        }
        return features

    def get_features(self):
        self._features = [Page.extract_features_per_location(location_element) for location_element in self._locations]
        return self._features


a = Page(conf.PAGE_URL)
a.get_locations_elements()
features = a.get_features()
print(features)


