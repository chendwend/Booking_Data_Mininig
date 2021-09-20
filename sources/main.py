from sources.from_csv_to_db import insert_to_db
from utilities.config import WEB_SOURCE
from sources.source_page import Website
from time import perf_counter
from datetime import datetime
import argparse
import sys
import csv


def validate_date(s):
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

    return destination


def write_to_csv(data_list, filename="data.csv"):
    """
    Writes all data into a csv file
    :param data_list: a list of dictionaries
    :type data_list: list
    :param filename: the name of the csv file to be written to
    :type filename: str
    """
    keys = data_list[0][0].keys()
    with open(filename, 'w', newline='') as csv_file:
        dict_writer = csv.DictWriter(csv_file, keys)
        dict_writer.writeheader()
        for page in data_list:
            dict_writer.writerows(page)


if __name__ == '__main__':
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
    data_list, pages, failed_pages, failed_stays = website.get_all_data()
    website.teardown()
    write_to_csv(data_list)
    insert_to_db(args.start_date, args.end_date, args.destination)
    time = perf_counter() - start
    print(
        f"Basic processing information for destination ='{args.destination}',"
        f" between {args.start_date.date()} and {args.end_date.date()}:")
    print(f"Number of total pages = {pages}")
    print(f"Number of failed pages = {failed_pages}")
    print(f"Number of failed stays = {failed_stays}")
    print(f"Execution time: {time / 60:.2f} minutes")
