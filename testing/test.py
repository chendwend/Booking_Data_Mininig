from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)
from selenium import webdriver
from utilities.config import USER_AGENT, SEARCH_BAR, SEARCH_BUTTON, \
    CALENDAR, BAR, DEFAULT_VALUE, PAGE_DATA_DICT, REGEX_DATA_DICT, PAGES_BUTTONS, ROOM_FACILITIES, SERVICE_AVAILABILITY
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utilities.config import SEC_TO_WAIT, DEFAULT_VALUE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from time import perf_counter
import re
import pandas as pd
import grequests
from bs4 import BeautifulSoup

url = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaGqIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4Apaw74sGwAIB0gIkYjBiMWNkOTctYWRmMC00Y2U4LTgzNDMtYTMyZDVhYzE1ZDMz2AIG4AIB;sid=96fed286f84b1cadf61d477975932c11;checkin_monthday=08;checkin_year_month=2021-11;checkout_monthday=15;checkout_year_month=2021-11;dest_id=80;dest_type=country;from_history=1;group_adults=2;group_children=0;no_rooms=1;radius=1;si=ad;si=ai;si=ci;si=co;si=di;si=la;si=re;sig=v1mYt_Bn8Y&;sh_position=1'
selector = "._4310f7077._ab6816951._03eb8c30a.e33c6840d8._aa53125bf._c846a17ec"
options = Options()
options.add_argument("--headless")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument(f'user-agent={USER_AGENT}')  # Without this -> doesn't find pages
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(url)


# element_3 = driver.find_elements_by_xpath("//*[contains(text(), '3')]")
def extract_service(element, selector_string):
    """
    Checks if the string selector_string is present in the element.

    :param element: selenium object
    :param selector_string: a string to search for the required service
    :type selector_string: str
    :return: the appropriate SERVICE_AVAILABILITY constant from config.py
    :rtype: int
    """
    condition = selector_string in element.lower()
    return SERVICE_AVAILABILITY["yes"] if condition else SERVICE_AVAILABILITY["no"]


elems = WebDriverWait(driver, SEC_TO_WAIT).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
start = perf_counter()
links = [elem.get_attribute('href') for elem in elems]
rs = (grequests.get(url) for url in links)  # Create a set of unsent Requests
responses = grequests.map(rs, size=10)  # Send them all at the same time bu batches
# for response in responses:
soups = [BeautifulSoup(response.content, "html.parser") for response in responses]
facilities = [soup.find(class_="hotel-facilities") for soup in soups]
facilities_text = [facility.text for facility in facilities]
room_facilities = []
for facility in facilities_text:
    dicti = {}
    dicti.update({service: extract_service(facility, selector_string) for service, selector_string in
                            ROOM_FACILITIES.items()})
    room_facilities.append(dicti)
time = perf_counter() - start
print(f"Execution time: {time / 60:.2f} minutes")

# data = []
# start = perf_counter()
# for data_type, data_selector in PAGE_DATA_DICT.items():
#     try:
#         elements = WebDriverWait(driver, SEC_TO_WAIT).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, data_selector))
#         )
#     except TimeoutException:
#         print(f'selector {data_selector} not found for data type {data_type}')
#     original_data_text_list = [element.text for element in elements]
#     filtered_data_list = clean_data(original_data_text_list, data_type)
#     data.append(filtered_data_list)
#

# for element in elements:
#     print(element.text)
# text = element_3.text
a = 5
