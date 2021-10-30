# from gevent import monkey as curious_george
#
# curious_george.patch_all(thread=False, select=False)
# from selenium import webdriver
# from utilities.config import USER_AGENT, SEARCH_BAR, SEARCH_BUTTON, \
#     CALENDAR, BAR, DEFAULT_VALUE, PAGE_DATA_DICT, REGEX_DATA_DICT, PAGES_BUTTONS, ROOM_FACILITIES, SERVICE_AVAILABILITY
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from time import perf_counter
# import re
# import pandas as pd
# import grequests
# from bs4 import BeautifulSoup
from utilities.config import *
import argparse
# url = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaGqIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4Apaw74sGwAIB0gIkYjBiMWNkOTctYWRmMC00Y2U4LTgzNDMtYTMyZDVhYzE1ZDMz2AIG4AIB;sid=96fed286f84b1cadf61d477975932c11;checkin_monthday=08;checkin_year_month=2021-11;checkout_monthday=15;checkout_year_month=2021-11;dest_id=80;dest_type=country;from_history=1;group_adults=2;group_children=0;no_rooms=1;radius=1;si=ad;si=ai;si=ci;si=co;si=di;si=la;si=re;sig=v1mYt_Bn8Y&;sh_position=1'
# selector = "._4310f7077._ab6816951._03eb8c30a.e33c6840d8._aa53125bf._c846a17ec"
# options = Options()
# options.add_argument("--headless")
# options.add_argument("--blink-settings=imagesEnabled=false")
# options.add_argument(f'user-agent={USER_AGENT}')  # Without this -> doesn't find pages
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver.get(url)
#
#
# # element_3 = driver.find_elements_by_xpath("//*[contains(text(), '3')]")
# def extract_service(element, selector_string):
#     """
#     Checks if the string selector_string is present in the element.
#
#     :param element: selenium object
#     :param selector_string: a string to search for the required service
#     :type selector_string: str
#     :return: the appropriate SERVICE_AVAILABILITY constant from config.py
#     :rtype: int
#     """
#     condition = selector_string in element.lower()
#     return SERVICE_AVAILABILITY["yes"] if condition else SERVICE_AVAILABILITY["no"]
#
#
# elems = WebDriverWait(driver, SEC_TO_WAIT).until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
# start = perf_counter()
# links = [elem.get_attribute('href') for elem in elems]
# rs = (grequests.get(url) for url in links)  # Create a set of unsent Requests
# responses = grequests.map(rs, size=10)  # Send them all at the same time bu batches
# # for response in responses:
# soups = [BeautifulSoup(response.content, "html.parser") for response in responses]
# facilities = [soup.find(class_="hotel-facilities") for soup in soups]
# facilities_text = [facility.text for facility in facilities]
# room_facilities = []
# for facility in facilities_text:
#     dicti = {}
#     dicti.update({service: extract_service(facility, selector_string) for service, selector_string in
#                             ROOM_FACILITIES.items()})
#     room_facilities.append(dicti)
# time = perf_counter() - start
# print(f"Execution time: {time / 60:.2f} minutes")

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
import sys
from datetime import datetime


def validate_date(s):
    """
    Validates a date to be of type YYYY-MM-DD and is not in the past.
    If not given in this formant, exits the program.
    :param s: date
    :type s: str
    :return: datetime object representation of the given date
    :rtype: datetime
    """
    try:
        date = datetime.strptime(s, "%Y-%m-%d")
        today = datetime.today()
        if date < today:
            sys.exit(f"the date {date} is in the past.")
    except ValueError:
        msg = f"Not a valid date: {s}"
        raise argparse.ArgumentTypeError(msg)
    return date


def validate_name(destination):
    """
    Validates the given string to be alphanumeric.
    If not, exits the program.

    :param destination: desired destination
    :type destination: str
    :return: destination, the input
    :rtype: str
    """
    if not destination.isalpha():
        sys.exit(f"the destination {destination} is not alphanumeric.")

    destination_filtered = destination

    return destination


parser = argparse.ArgumentParser(description="Extract data from Booking.com")
subparsers = parser.add_subparsers(help='sub-command help')  # dest='subcommand'
Q_parser = subparsers.add_parser("Q", help="Query help")
S_parser = subparsers.add_parser("S", help="Scrape help")
# a_parser.add_argument("something", choices=['a1', 'a2'])

# Scraper parser arguments
S_parser.add_argument("-s", "--start_date", help="Start date - format YYYY-MM-DD ", required=True, type=validate_date)
S_parser.add_argument("-e", "--end_date", help="End date - format YYYY-MM-DD ", required=True, type=validate_date)
S_parser.add_argument('-d', "--destination", help="Desired country", required=True, type=validate_name)
# Query parser arguments
Q_parser.add_argument("--city", help="the city to filter by", type=validate_name)
Q_parser.add_argument("--breakfast", help="filter by breakfast inclusiveness", choices=['yes', 'no'])

args = parser.parse_args('Q --breakfast yes'.split())
args.func(args)

args = parser.parse_args()

# Base select statement
base_statement = \
    f"SELECT * " \
    f"FROM {TABLE_NAMES[0]} " \
    f"INNER JOIN {TABLE_NAMES[1]} ON {TABLE_NAMES[0]}.{JOIN_COLUMNS[0][0]}={TABLE_NAMES[1]}.{JOIN_COLUMNS[0][1]}" \
    f"INNER JOIN {TABLE_NAMES[2]} ON {TABLE_NAMES[1]}.{JOIN_COLUMNS[1][0]}={TABLE_NAMES[2]}.{JOIN_COLUMNS[1][1]}"




# This list will hold all the extra conditionals
operators = []

if "city" in args:
    operators.append("sub location BETWEEN {} AND {}".format(*args["date"]))

a = 5

