from sources.source_page import *
from time import perf_counter
import argparse
from datetime import datetime


def valid_date(s):
    """
    Validates a date to be of type YYYY-MM-DD and is not in the past
    If not given in this formant, exits the program.
    :param s: date
    :type s: str
    :return: datetime object representation of the given date
    :rtype: datetime
    """
    try:
        date = datetime.strptime(s, "%Y-%m-%d")
        today = datetime.today()
        if date < today:
            sys.exit(f"the date {date} is in the past.")
    except ValueError:
        msg = f"Not a valid date: {s}"
        raise argparse.ArgumentTypeError(msg)
    return date


def valid_destination(destination):
    """
    Validates the given string to be alphanumeric.
    If not, exits the program.

    :param destination: desired destination
    :type destination: str
    :return: destination, the input
    :rtype: str
    """
    if not destination.isalpha():
        sys.exit(f"the destination {destination} is not alphanumeric.")
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract data from Booking.com")
    parser.add_argument('-d', "--destination", help="Desired destination", required=True, type=valid_destination, action="store")
    parser.add_argument("-s", "--start_date", help="Start date - format YYYY-MM-DD ", required=True, type=valid_date)
    parser.add_argument("-e", "--end_date", help="End date - format YYYY-MM-DD ", required=True, type=valid_date)
    args = parser.parse_args()

    start = perf_counter()
    website = Website(WEB_SOURCE)
    website.enter_location(args.destination)
    website.click_search_button()
    website.select_date(args.start_date, args.end_date)
    data_list, pages, failures = website.get_all_data()
    website.teardown()
    time = perf_counter() - start
    print(f"Basic statistics for destination= '{args.destination}', between {args.start_date.date()} and {args.end_date.date()}:")
    print(f"Number of total pages = {pages}")
    print(f"Number of failed pages = {failures}")
    print(f"Execution time: {time:.2f} seconds")
    print(f"{BAR}\nResults:\n{BAR}")
    for data in data_list:
        print(data)
