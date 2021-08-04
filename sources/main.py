from sources.source_page import *
from time import perf_counter
import argparse
from datetime import datetime


def valid_date(s):
    try:
        date = datetime.strptime(s, "%Y-%m-%d")
        today = datetime.today()
        if date < today:
            sys.exit(f"the date {date} is in the past.")
    except ValueError:
        msg = f"Not a valid date: {s}"
        raise argparse.ArgumentTypeError(msg)


def valid_destination(dest):
    if not dest.isalpha():
        sys.exit(f"the destination {dest} is not alphanumeric.")


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="Extract data from Booking.com")
    # parser.add_argument('-d', "--destination", help="desired destination", required=True, type=valid_destination)
    # parser.add_argument("-s", "--start_date", help="Start date - format YYYY-MM-DD ", required=True, type=valid_date)
    # parser.add_argument("-e", "--end_date", help="end date - format YYYY-MM-DD ", required=True, type=valid_date)
    # args = parser.parse_args()

    start = perf_counter()
    destination = input("Enter desired destination: ")
    website = Website(WEB_SOURCE)
    website.enter_location(destination)
    website.click_search_button()
    website.select_date()
    features_list = website.get_all_features()
    website.teardown()
    time = perf_counter() - start
    print(f"\n-----------------\nExecution time: {time:.2f} seconds")
    for element in features_list[:5]:
        print(element)
