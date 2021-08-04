"""############ website constants ############"""

# ------------------- airbnb ------------------------
#
"""
1. Add CHROME_DRIVER_PATH assumption to README.md
"""

# WEB_SOURCE = "https://www.airbnb.com"

CHROME_DRIVER_PATH = "C:/Program Files (x86)/chromedriver.exe"
SEC_TO_WAIT = 10
# IDENTIFIER_SEARCH_LOCATION = "query"
"c-autocomplete__input sb-searchbox__input sb-destination__input"
# IDENTIFIER_SEARCH_BUTTON = "_m9v25n"
# IDENTIFIER_SEARCH_BUTTON = "_sxfp92z"
# IDENTIFIER_SEARCH_BUTTON = "_1mzhry13"
# IDENTIFIER_PAGE_BUTTONS = "_1y623pm"
# MAX_STAYS_IN_PAGE = 20

"""########## page constants #############"""
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/92.0.4515.107 Safari/537.36"
PARSER = "html.parser"
IDENTIFIER_LOCATIONS = ("div", "class", "_12oal24")  # _1e541ba5 # ("div", "class", _12oal24
IDENTIFIER_NAME = "_1whrsux9"
IDENTIFIER_SUB_LOCATION = "_1olmjjs6"
IDENTIFIER_PRICE = "_155sga30"
IDENTIFIER_RATING = "_10fy1f8"
IDENTIFIER_REVIEWERS_AMOUNT = "_a7a5sx"
# FEATURES_DICT = {
#     "name": ("span", "class", "_1whrsux9"),
#     "sub_location": ("div", "class", "_1olmjjs6"),
#     "price": ("span", "class", "_155sga30"),
#     "rating": ("span", "class", "_10fy1f8"),
#     "reviewers_amount": ("span", "class", "_a7a5sx"),
#     "guests_amount": ("span", "class", "_3hmsj"),
#     "wifi": ("span", "class", "_3hmsj")
# }
TAG, TYPE, ID = (0, 1, 2)
DEFAULT_NUMBER_OF_ATTEMPTS = 10
RATING_REGEX = "[0-9]+"
PRICE_REGEX = "[0-9]+"
REVIEWERS_REGEX = "[0-9]+"

# -------------- booking -----------------
WEB_SOURCE = "https://www.booking.com"
SEARCH_LOCATION_STRING = "ss"
SEARCH_BUTTON_STRING = "sb-searchbox__button "
PAGES_LINKS_STRING = ".bui-pagination__pages .bui-pagination__list li a"
DATES_STRING = "//div[contains(@data-mode,'checkin')]//span[contains(@class,'sb-date-field__icon sb-date-field__icon-btn bk-svg-wrapper calendar-restructure-sb')]"
MAX_STAYS_IN_PAGE = 25


NUMBERS_REGEX = "[0-9]+$"
OFFSET_REGEX = "[0-9]+$"

MAIN_STRING = "#hotellist_inner"
STAYS_STRING = ".sr_property_block_main_row"
FEATURES_DICT = {
    "name": ".sr-hotel__name",
    "location": ".bui-link",
    "price": "//body[contains(@class, 'prco-wrapper)]",
    "rating": ".bui-review-score__badge",
    "beds": ".bui-u-sr-only",
    "reviewers_amount": ".bui-review-score__text",
}

