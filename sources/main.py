from selenium import webdriver  # links up with the brower and perfroms the actions
from selenium.webdriver.common.keys import Keys  # access to enter key etc.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

PATH = "C:\Program Files (x86)\chromedriver.exe"  # location of chromedriver
WEBSITE = "https://www.airbnb.com/"
HTML_ELEMENT_RESULT_PAGE = ''
driver = webdriver.Chrome(PATH)  # choose web browser to work with

driver.get(WEBSITE)
print(driver.title)  # prints title written at the tab

search = driver.find_element_by_id("bigsearch-query-detached-query")
search.send_keys("Milano")  # types Milano
search.send_keys(Keys.RETURN)

# Wait for new page to load:
try:
    main = WebDriverWait(driver, 10).until(  # wait 10 seconds until
        EC.presence_of_element_located((By.ID, HTML_ELEMENT_RESULT_PAGE))
    )
    print(main.text)
finally:
    driver.quit()
# On new page

time.sleep(5)




driver.close()  # closes tab
# driver.quit()  # closes entire window
