"""############ website constants ############"""

"""
1. Add CHROME_DRIVER_PATH assumption to README.md
"""

CHROME_DRIVER_PATH = "C:/Program Files (x86)/chromedriver.exe"
SEC_TO_WAIT = 10

"""########## page constants #############"""
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/92.0.4515.107 Safari/537.36"



# -------------- booking -----------------
WEB_SOURCE = "https://www.booking.com"
SEARCH_LOCATION_STRING = "ss"
SEARCH_BUTTON_STRING = "sb-searchbox__button "
PAGES_LINKS_STRING = ".bui-pagination__pages .bui-pagination__list li a"


# --- page constants

PRICE_REGEX = "[0-9,]+$"
NUMBERS_REGEX = "[0-9]+$"
OFFSET_REGEX = "[0-9]+$"


MAIN_STRING = "#hotellist_inner"

# --- REGEX
NAME_REGEX = ".*"
RATING_REGEX = "[0-9]+"
PRICE_REGEX = "[0-9,]+$"
REVIEWERS_REGEX = "[0-9]+"
LOCATION_REGEX = "(?!Show)\w+"
MAX_PERSONS_REGEX = "[0-9]+$"

UPPER_STRING = ".sr_property_block_main_row"
LOWER_STRING = ".roomrow"
PRICE_STRING = ".prco-ltr-right-align-helper"
MAX_PERSONS_STRING = ".roomNameInner .bui-u-sr-only"


DATA_TYPES_UPPER = {
    "name": (".sr-hotel__name", NAME_REGEX),
    "location": (".bui-link", LOCATION_REGEX),
    "rating": (".bui-review-score__badge", RATING_REGEX),
    "reviewers_amount": (".bui-review-score__text", REVIEWERS_REGEX)
}
DATA_TYPES_LOWER = {
    "price": PRICE_STRING,
    "max persons": MAX_PERSONS_STRING
}


