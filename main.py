from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
from sources.from_csv_to_db import insert_to_db
from utilities.config import WEB_SOURCE, FILE_NAME, OUTPUT_DIR
from sources.weather_api import weather_api
from sources.source_page import Website
from datetime import datetime
from time import perf_counter
import argparse
import sys
import os
import logging
from utilities.log import init_logger


def validate_date(s):
    """
    Validates a date to be of type YYYY-MM-DD and is not in the past.
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


def validate_country(destination):
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

    destination_filtered = destination

    return destination


if __name__ == '__main__':
    logger = init_logger()
    logger.error(f'Hi kostya')
    parser = argparse.ArgumentParser(description="Extract data from Booking.com")
    parser.add_argument('-d', "--destination", help="Desired country", required=True, type=validate_country,
                        action="store")
    parser.add_argument("-s", "--start_date", help="Start date - format YYYY-MM-DD ", required=True, type=validate_date)
    parser.add_argument("-e", "--end_date", help="End date - format YYYY-MM-DD ", required=True, type=validate_date)
    args = parser.parse_args()

    start = perf_counter()
    website = Website(WEB_SOURCE)
    website.insert_location(args.destination)
    website.select_date(args.start_date, args.end_date)
    data, pages = website.get_all_data()
    website.teardown()

    path1 = os.path.join(OUTPUT_DIR, FILE_NAME)
    path2 = os.path.join(OUTPUT_DIR, 'output.csv')
    # os.chdir(OUTPUT_DIR)
    data.to_csv(path1, index=False)
    weather_api(path1)
    insert_to_db(args.start_date, args.end_date, args.destination, path2)
    time = perf_counter() - start
    print(
        f"Basic processing information for destination ='{args.destination}',"
        f" between {args.start_date.date()} and {args.end_date.date()}:")
    print(f"Number of total pages = {pages}")
    print(f"Execution time: {time / 60:.2f} minutes")
