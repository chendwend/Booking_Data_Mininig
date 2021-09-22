"""########## General constants #############"""
BAR = "-----------------------------------"

"""########## Webdriver constants #############"""
SEC_TO_WAIT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/93.0.4577.82 Safari/537.36"

"""########## Website constants #############"""
WEB_SOURCE = "https://www.booking.com"
SEARCH_BAR = {"name": "search bar", "selector": "ss"}
SEARCH_BUTTON = {"name": "search button", "selector": ".sb-searchbox__button "}
PAGE_LINKS = {"name": "page links", "selector": ".bui-pagination__pages .bui-pagination__list li a"}
CALENDAR = {"name": "calendar", "selector": ".bui-calendar__date"}
OFFSET_REGEX = "[0-9]+$"
DEFAULT_VALUE = -1
EMPTY_STRING = ''

"""########## Page constants #############"""

# --- REGEX
NAME_REGEX = ".*"
RATING_REGEX = "[0-9.]+"
PRICE_REGEX = "[0-9,]+$"
REVIEWERS_REGEX = "[0-9]+"
LOCATION_REGEX = "(?!Show)\w+"
MAX_PERSONS_REGEX = "[0-9]+$"

# --- Selector strings
MAIN_PAGE = {"name": "main page", "selector": "#hotellist_inner"}
UPPER = {"name": "upper part", "selector": ".sr_property_block_main_row"}
LOWER = {"name": "lower part", "selector": ".roomrow"}
PRICE_STRING = ".prco-ltr-right-align-helper"
MAX_PEOPLE = {"name": "max people", "selector": ".roomNameInner .bui-u-sr-only"}
POLICY_STRING = ".sr_card_room_policies__container"
SUB_LOCATION_FACILITIES = {"name": "sub location facilities", "selector": ".sr-cta-button-row"}

DATA_TYPES_UPPER = [{"name": "name", "selector": ".sr-hotel__name"},
                    {"name": "sub location", "selector": ".bui-link"},
                    {"name": "rating", "selector": ".bui-review-score__badge"},
                    {"name": "reviewers amount", "selector": ".bui-review-score__text"}]
DATA_TYPES_UPPER_REGEX = [NAME_REGEX, LOCATION_REGEX, RATING_REGEX, REVIEWERS_REGEX]

DATA_TYPES_LOWER = [{"name": "price", "selector": ".prco-ltr-right-align-helper"},
                    {"name": "max people", "selector": ".roomNameInner .bui-u-sr-only"}]

"""########## Hotel constants #############"""
PET_STRING = "pets are allowed"
WIFI_STRING = "wifi is available"
KITCHEN_STRING = "kitchen"
PARKING_STRING = "parking is possible"
AIR_CONDITIONING_STRING = "air conditioning"
FREE_CANCELLATION_STRING = "free cancellation"
BREAKFAST_STRING = "breakfast included"
FACILITY_STRING_LIST = [({"name": "facilities - first selector", "selector": ".hotel-facilities__list"}, 0),
                        ({"name": "facilities - second selector", "selector": ".facilitiesChecklist"}, 1)]

ROOM_FACILITIES_KEYS = ["pets", "wifi", "kitchen", "parking", "air conditioning"]
ROOM_FACILITIES_VALUES = [PET_STRING, WIFI_STRING, KITCHEN_STRING, PARKING_STRING, AIR_CONDITIONING_STRING]
ROOM_FACILITIES = dict(zip(ROOM_FACILITIES_KEYS,ROOM_FACILITIES_VALUES))
EMPTY_ROOM_FACILITIES = dict(zip(ROOM_FACILITIES_KEYS, [DEFAULT_VALUE]*len(ROOM_FACILITIES_KEYS)))
SERVICE_AVAILABILITY = {"yes": 1, "no": 0}
"""########## SQL constants ###############"""
FILE_NAME = "data.csv"
