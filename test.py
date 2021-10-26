from selenium import webdriver
from utilities.config import USER_AGENT, SEARCH_BAR, SEARCH_BUTTON, \
    CALENDAR, OFFSET_REGEX, BAR, DEFAULT_VALUE, USER_AGENT_LINUX, PAGE_DATA_DICT, REGEX_DATA_DICT, PAGES_BUTTONS
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

url = 'https://www.booking.com/hotel/de/weinhotel-klostermuhle.en-gb.html?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaGqIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4Ap7d3osGwAIB0gIkNjhkYTJlODAtMWViYi00ZjE1LWE5MDktNTViMGY4NGRjZWQ22AIG4AIB;sid=96fed286f84b1cadf61d477975932c11;all_sr_blocks=113551209_202201706_2_1_0;checkin=2021-11-09;checkout=2021-11-16;dest_id=80;dest_type=country;dist=0;group_adults=2;group_children=0;hapos=225;highlighted_blocks=113551209_202201706_2_1_0;hpos=25;matching_block_id=113551209_202201706_2_1_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=113551209_202201706_2_1_0__89400;srepoch=1635260416;srpvid=c5dd34d512140286;type=total;ucfs=1;sig=v1j-Quk3Yd&#hotelTmpl'
selector = ".fde444d7ef._c445487e2"
options = Options()
options.add_argument("--headless")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument(f'user-agent={USER_AGENT}')  # Without this -> doesn't find pages
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(url)


# element_3 = driver.find_elements_by_xpath("//*[contains(text(), '3')]")
def clean_data(data_list, data_type):
    data_list_filtered = data_list
    if data_type == "price":
        data_list_filtered = [int(re.search(REGEX_DATA_DICT["price"], data).group().replace(',', ''))
                              if data else DEFAULT_VALUE
                              for data in data_list]
    elif data_type == "reviewers amount":
        data_list_filtered = [int(re.search(REGEX_DATA_DICT["reviewers amount"], data).group()) \
                                  if data else DEFAULT_VALUE
                              for data in data_list]
    elif data_type == "rating":
        data_list_filtered = [float(data) for data in data_list]
    elif data_type == "sub location":
        data_list_filtered = [data[data.find(',') + 1:data.find('Show')]
                              if data.find(',') != -1 else data[0:data.find('Show')]
                              for data in data_list]
    return data_list_filtered


facilities = WebDriverWait(driver, SEC_TO_WAIT).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".hotel-facilities")))

k = facilities.text


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
# time = perf_counter() - start
# print(f"Execution time: {time / 60:.2f} minutes")

# for element in elements:
#     print(element.text)
# text = element_3.text
a = 5
