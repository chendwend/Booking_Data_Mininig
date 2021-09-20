"""########## General constants #############"""
BAR = "-----------------------------------"

"""########## Webdriver constants #############"""
SEC_TO_WAIT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/93.0.4577.82 Safari/537.36"

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
MAIN_PAGE_STRING = "#hotellist_inner"
UPPER_STRING = ".sr_property_block_main_row"
LOWER_STRING = ".roomrow"
PRICE_STRING = ".prco-ltr-right-align-helper"
MAX_PEOPLE_STRING = ".roomNameInner .bui-u-sr-only"
NAME_STRING = ".sr-hotel__name"
SUB_LOCATION_STRING = ".bui-link"
RATING_STRING = ".bui-review-score__badge"
REVIEWERS_STRING = ".bui-review-score__text"
POLICY_STRING = ".sr_card_room_policies__container"
STAY_FACILITIES_STRING = ".sr-cta-button-row"

DATA_TYPES_UPPER = {
    "name": (NAME_STRING, NAME_REGEX),
    "sub location": (SUB_LOCATION_STRING, LOCATION_REGEX),
    "rating": (RATING_STRING, RATING_REGEX),
    "reviewers amount": (REVIEWERS_STRING, REVIEWERS_REGEX)
}
DATA_TYPES_LOWER = {
    "price": PRICE_STRING,
    "max people": MAX_PEOPLE_STRING
}

"""########## Hotel constants #############"""
FACILITY_STRING = ".facilitiesChecklist"
FACILITY_STRING2 = ".hotel-facilities__list"
PET_STRING = "pets are allowed"
WIFI_STRING = "wifi is available"
KITCHEN_STRING = "kitchen"
PARKING_STRING = "parking is possible"
AIR_CONDITIONING_STRING = "air conditioning"
FREE_CANCELLATION_STRING = "free cancellation"
BREAKFAST_STRING = "breakfast included"

ROOM_FACILITIES = {
    "pets": PET_STRING,
    "wifi": WIFI_STRING,
    "kitchen": KITCHEN_STRING,
    "parking": PARKING_STRING,
    "air conditioning": AIR_CONDITIONING_STRING
}

"""########## SQL constants ###############"""
DEFAULT_VALUE = -1
FILE_NAME = "data.csv"
