"""############ website constants ############"""

# ------------------- airbnb ------------------------
#
"""
1. Add CHROME_DRIVER_PATH assumption to README.md
"""

# WEB_SOURCE = "https://www.airbnb.com"

CHROME_DRIVER_PATH = "C:/Program Files (x86)/chromedriver.exe"
SEC_TO_WAIT = 20
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
IDENTIFIER_SEARCH_LOCATION = "c-autocomplete__input sb-searchbox__input sb-destination__input"
IDENTIFIER_SEARCH_BUTTON = "sb-searchbox__button "
IDENTIFIER_PAGE_BUTTONS = "bui-pagination__item sr_pagination_item"
MAX_STAYS_IN_PAGE = 25

OFFSET_REGEX = "=[0-9]+$"

IDENTIFIER_LOCATIONS = ("div", "class", "sr_item  sr_item_new sr_item_default sr_property_block sr_flex_layout         ")
FEATURES_DICT = {
    "name": ("div", "class", "sr-hotel__name"),
    "sub_location": ("a", "class", "bui-link"),
    "price": ("div", "class", "bui-price-display__value prco-inline-block-maker-helper "),
    "rating": ("div", "class", "bui-review-score__badge"),
    "reviewers_amount": ("div", "class", "bui-review-score__text"),
    "guests_amount": ("span", "class", "_3hmsj"),
    "wifi": ("span", "class", "_3hmsj")
}

