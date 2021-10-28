from selenium import webdriver
from utilities.config import USER_AGENT, SEARCH_BAR, SEARCH_BUTTON, \
    CALENDAR, BAR, DEFAULT_VALUE, USER_AGENT_LINUX, PAGE_DATA_DICT, REGEX_DATA_DICT, PAGES_BUTTONS
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

url = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaGqIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4AonY5osGwAIB0gIkNDZkOGE0ZDUtNjZlMi00YTE3LTg2NjQtOTVjZWJkN2E0MzM32AIG4AIB&lang=en-gb&sid=96fed286f84b1cadf61d477975932c11&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.en-gb.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaGqIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4AonY5osGwAIB0gIkNDZkOGE0ZDUtNjZlMi00YTE3LTg2NjQtOTVjZWJkN2E0MzM32AIG4AIB%3Bsid%3D96fed286f84b1cadf61d477975932c11%3Btmpl%3Dsearchresults%3Bac_click_type%3Db%3Bac_position%3D0%3Bclass_interval%3D1%3Bdest_id%3D80%3Bdest_type%3Dcountry%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcountry%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dindex%3Bsrc_elem%3Dsb%3Bsrpvid%3D4d538ac7bfc3001a%3Bss%3DGermany%3Bss_all%3D0%3Bss_raw%3Dgermany%3Bssb%3Dempty%3Bsshis%3D0%3Btop_ufis%3D1%3Bsig%3Dv163k2XQJc%26%3B&ss=Germany&is_ski_area=0&ssne=Germany&ssne_untouched=Germany&dest_id=80&dest_type=country&checkin_year=2021&checkin_month=11&checkin_monthday=8&checkout_year=2021&checkout_month=11&checkout_monthday=15&group_adults=2&group_children=0&no_rooms=1&sb_changed_dates=1&from_sf=1&track_hp_back_button=1#hotel_60625-back'
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


b_c = WebDriverWait(driver, SEC_TO_WAIT).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._371410fad")))

for element in b_c:
    print(element.text)


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
