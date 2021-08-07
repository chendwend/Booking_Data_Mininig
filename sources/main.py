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
    return date


def valid_destination(dest):
    if not dest.isalpha():
        sys.exit(f"the destination {dest} is not alphanumeric.")
    return dest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract data from Booking.com")
    parser.add_argument('-d', "--destination", help="Desired destination", required=True, type=valid_destination, action="store")
    parser.add_argument("-s", "--start_date", help="Start date - format YYYY-MM-DD ", required=True, type=valid_date)
    parser.add_argument("-e", "--end_date", help="End date - format YYYY-MM-DD ", required=True, type=valid_date)
    args = parser.parse_args()

    start = perf_counter()
    # destination = input("Enter desired destination: ")
    website = Website(WEB_SOURCE)
    print(args.destination)
    print(args.start_date)
    website.enter_location(args.destination)
    website.click_search_button()
    # start_date, stop_date = datetime.strptime(args.start_date, "%Y-%m-%d"), datetime.strptime(args.stop_date, "%Y-%m-%d")
    website.select_date(args.start_date, args.end_date)
    features_list = website.get_all_features()
    website.teardown()
    time = perf_counter() - start
    print(f"\n-----------------\nExecution time: {time:.2f} seconds")
    for element in features_list:
        print(element)
