"""########## General constants #############"""
BAR = "-----------------------------------"

"""########## Webdriver constants #############"""
CHROME_DRIVER_PATH = "C:/Program Files (x86)/chromedriver.exe"
SEC_TO_WAIT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/92.0.4515.131 Safari/537.36"

"""########## Website constants #############"""
WEB_SOURCE = "https://www.booking.com"
SEARCH_LOCATION_STRING = "ss"
SEARCH_BUTTON_STRING = ".sb-searchbox__button "
PAGES_LINKS_STRING = ".bui-pagination__pages .bui-pagination__list li a"
CALENDAR_STRING = ".bui-calendar__date"
OFFSET_REGEX = "[0-9]+$"

"""########## Page constants #############"""

# --- REGEX
NAME_REGEX = ".*"
RATING_REGEX = "[0-9.]+"
PRICE_REGEX = "[0-9,]+$"
REVIEWERS_REGEX = "[0-9]+"
LOCATION_REGEX = "(?!Show)\w+"
MAX_PERSONS_REGEX = "[0-9]+$"

# --- Selector strings
MAIN_STRING = "#hotellist_inner"
UPPER_STRING = ".sr_property_block_main_row"
LOWER_STRING = ".roomrow"
PRICE_STRING = ".prco-ltr-right-align-helper"
MAX_PERSONS_STRING = ".roomNameInner .bui-u-sr-only"
NAME_STRING = ".sr-hotel__name"
LOCATION_STRING = ".bui-link"
RATING_STRING = ".bui-review-score__badge"
REVIEWERS_STRING = ".bui-review-score__text"

DATA_TYPES_UPPER = {
    "name": (NAME_STRING, NAME_REGEX),
    "location": (LOCATION_STRING, LOCATION_REGEX),
    "rating": (RATING_STRING, RATING_REGEX),
    "reviewers amount": (REVIEWERS_STRING, REVIEWERS_REGEX)
}
DATA_TYPES_LOWER = {
    "price": PRICE_STRING,
    "max persons": MAX_PERSONS_STRING
}
