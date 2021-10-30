"""########## General constants #############"""
BAR = "-----------------------------------"
FILE_NAME = "data.csv"
OUTPUT_DIR = 'output_files'
QUERY_OUTPUT_FILE = 'query.csv'

"""########## Logger constants #############"""
FORMATTER_STRING = '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s'
FILE_NAME_LOG = 'booking.log'

"""########## Webdriver constants #############"""
SEC_TO_WAIT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/93.0.4577.82 Safari/537.36"

"""########## Website constants #############"""
WEB_SOURCE = "https://www.booking.com"
SEARCH_BAR = {"name": "search bar", "selector": "ss"}
SEARCH_BUTTON = {"name": "search button", "selector": ".sb-searchbox__button "}
PAGES_BUTTONS = {"name": "page links", "selector": "._4310f7077._fd15ae127"}
CALENDAR = {"name": "calendar", "selector": ".bui-calendar__date"}

DEFAULT_VALUE = -1

"""########## Page constants #############"""

PAGE_DATA_DICT = \
    {"site_name": ".fde444d7ef._c445487e2",
     "sub_location": "._cff98816f",
     "rating": "._9c5f726ff.bd528f9ea6",
     "reviewers_amount": "._4abc4c3d5._1e6021d2f._fb3ba087b._6e869d6e0",
     "price": ".fde444d7ef._e885fdc12",
     "breakfast": "._371410fad",
     "free_cancellation": "._371410fad"
     }

REGEX_DATA_DICT = \
    {"reviewers_amount": "[0-9]+",
     "price": "[0-9,]+$"
     }

SUB_LOCATION_FACILITIES = {"name": "sub location facilities",
                           "selector": "._4310f7077._ab6816951._03eb8c30a.e33c6840d8._aa53125bf._c846a17ec"}
BATCH_SIZE = 20

"""########## Hotel constants #############"""
PET_STRING = "pets are allowed"
WIFI_STRING = "wifi is available"
KITCHEN_STRING = "kitchen"
PARKING_STRING = "parking is possible"
AIR_CONDITIONING_STRING = "air conditioning"
FREE_CANCELLATION_STRING = "free cancellation"
BREAKFAST_STRING = "breakfast included"

FACILITY_CLASS = "hotel-facilities"
ROOM_FACILITIES_KEYS = ["pets", "wifi", "kitchen", "parking", "air_conditioning"]
ROOM_FACILITIES_VALUES = [PET_STRING, WIFI_STRING, KITCHEN_STRING, PARKING_STRING, AIR_CONDITIONING_STRING]
ROOM_FACILITIES = dict(zip(ROOM_FACILITIES_KEYS, ROOM_FACILITIES_VALUES))
EMPTY_ROOM_FACILITIES = dict(zip(ROOM_FACILITIES_KEYS, [DEFAULT_VALUE] * len(ROOM_FACILITIES_KEYS)))
SERVICE_AVAILABILITY = {"yes": 1, "no": 0}
"""########## SQL constants ###############"""
TABLE_NAMES = ['location_dates', 'site_info', 'facilities']
JOIN_COLUMNS = [('id', 'location_dates_id'), ('location_dates_id', 'location_dates_id')]

BASE_STATEMENT = \
    "SELECT " + ('{}, '*len(PAGE_DATA_DICT)).format(*PAGE_DATA_DICT.keys()) +\
    ', '.join(ROOM_FACILITIES_KEYS) +\
    f" FROM {TABLE_NAMES[0]} " +\
    f"INNER JOIN {TABLE_NAMES[1]} ON {TABLE_NAMES[0]}.{JOIN_COLUMNS[0][0]}={TABLE_NAMES[1]}.{JOIN_COLUMNS[0][1]} " +\
    f"INNER JOIN {TABLE_NAMES[2]} ON {TABLE_NAMES[1]}.{JOIN_COLUMNS[1][0]}={TABLE_NAMES[2]}.{JOIN_COLUMNS[1][1]}"


"""########## API constants ###############"""
COLUMNS = ['latitude', 'longitude', 'temperature', 'feelslike']
ACCESS_KEY = 'c97f8ed4ab7a775dd2abe77f28bac6be'
TYPE_OF_REQUEST = 'current'
