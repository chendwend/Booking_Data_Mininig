from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#cortland, NY = 2, penn yan, NY = 3, Etna, NY = 4

#LOCATION = input("Hello, please enter desired location: ")
LOCATION = "italy"
WEB_SOURCE = "https://www.airbnb.com"
PATH = "C:/Program Files (x86)/chromedriver.exe"
SEC_TO_WAIT = 10
IDENTIFIER_SEARCH_LOCATION = "query"
IDENTIFIER_SEARCH_BUTTON = "_m9v25n"
IDENTIFIER_PAGE_BUTTONS = "_1y623pm"
MAX_STAYS_IN_PAGE = 20


def enter_location(location):
    try:
        search_location = WebDriverWait(driver, SEC_TO_WAIT).until(
            EC.presence_of_element_located((By.NAME, IDENTIFIER_SEARCH_LOCATION))
        )
        search_location.send_keys(location)
    except:
        driver.quit()
    return


def clicking_the_search_button():
    try:
        search_button = WebDriverWait(driver, SEC_TO_WAIT).until(
            EC.presence_of_element_located((By.CLASS_NAME, IDENTIFIER_SEARCH_BUTTON))
        )
        search_button.click()
    except:
        driver.quit()
    return


def get_urls():
    list_urls = []
    first_page_url = driver.current_url
    time.sleep(SEC_TO_WAIT)
    list_urls.append(first_page_url)
    try:
        page_buttons = WebDriverWait(driver, SEC_TO_WAIT).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, IDENTIFIER_PAGE_BUTTONS))
        )
        number_of_pages_minus_one = len(page_buttons)
        if number_of_pages_minus_one >= 1:
            page_buttons[number_of_pages_minus_one - 1].click()
            time.sleep(SEC_TO_WAIT)
            url_page = driver.current_url
            time.sleep(SEC_TO_WAIT)
            url_first_part = url_page.split("offset=")[0]
            url_second_part = url_page.split("offset=")[1]
            the_constant_offset = url_page.split("offset=")[2]
            the_last_offset = url_second_part.split("&")[0]
            the_third_part = url_second_part.split("&")[1]
            for j in range(MAX_STAYS_IN_PAGE, int(the_last_offset)+MAX_STAYS_IN_PAGE, MAX_STAYS_IN_PAGE):
                list_urls.append(url_first_part+"offset="+str(j)+"&"+the_third_part+"offset="+the_constant_offset)
    except:
        driver.quit()
    return list_urls


if __name__ == '__main__':
    driver = webdriver.Chrome(PATH)
    driver.get(WEB_SOURCE)
    enter_location(LOCATION)
    clicking_the_search_button()
    urls = get_urls()
    for i in urls:
        print(f"{i}\n")
    driver.quit()

