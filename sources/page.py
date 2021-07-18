#  accepts a page URL and extracts a list of links of locations
import requests
from bs4 import BeautifulSoup
import utilities.config as conf


class Page:
    def __init__(self, search_page):
        self._search_page = search_page
        self._locations = []

    def get_locations_elements(self):
        page = requests.get(self._search_page)
        soup = BeautifulSoup(page.content, conf.PARSER)
        self._locations = soup.findAll("div", {"class": conf.LOCATIONS_CLASS_ID})

    def extract_features_per_location(self, location_element):
        url = location_element.find('a').get('href')
        name = location_element.find("span", {"id": "title_49517396"}).get_text()
        price = location_element.find("span", {"class": "_155sga30"}).get_text()

        return {"url": url, "name": name, "price": price}

    def get_features(self):
        features = [extract_features_per_location(location_element) for location_element in self._locations]
        return features




a = Page(conf.PAGE_URL)
a.get_locations_elements()
features = a.get_features()
print(features)
b= 5

