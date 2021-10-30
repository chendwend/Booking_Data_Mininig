from gevent import monkey

monkey.patch_all(thread=False, select=False)
from sources.sql_functions import insert_to_db, query_sql
from utilities.config import WEB_SOURCE, FILE_NAME, OUTPUT_DIR, BASE_STATEMENT
from sources.weather_api import weather_api
from sources.source_page import Website
from datetime import datetime
from time import perf_counter
from argparse import ArgumentParser, Action, ArgumentTypeError
import sys
import os


class StopAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Do whatever actions you want
        if values:
            print("Exiting")
            exit(0)


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
        raise ArgumentTypeError(msg)
    return date


def validate_name(destination):
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


def scraper(args):
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


def query(args):
    # This list will hold all the extra conditionals
    operators = []
    args = vars(args)
    args = {k: v for k, v in args.items() if v is not None and (k not in ['stop', 'func'])}
    # for k, v in args.items():
    #     print(f"{k}: {v}")
    # # )
    if "city" in args:
        operators.append(f"city={args['city']}")

    if operators:
        statement = BASE_STATEMENT + " WHERE " " and ".join(operators)

    query_response = query_sql(statement)
    print(query_response)


if __name__ == '__main__':
    parser = ArgumentParser(description="Extract data from Booking.com or Query the DB")
    parser.add_argument('stop', nargs='?', action=StopAction, default=False)
    subparsers = parser.add_subparsers(help='sub-command help')  # dest='subcommand'
    q_parser = subparsers.add_parser("q", help="Query help")  # query parser
    s_parser = subparsers.add_parser("s", help="Scrape help")  # scraper parser

    # Scraper parser arguments
    s_parser.add_argument("-s", "--start_date", help="Start date - format YYYY-MM-DD ", required=True,
                          type=validate_date)
    s_parser.add_argument("-e", "--end_date", help="End date - format YYYY-MM-DD ", required=True, type=validate_date)
    s_parser.add_argument('-d', "--destination", help="Desired country", required=True, type=validate_name)
    s_parser.set_defaults(func=scraper)

    # Query parser parser.parse_args()arguments
    q_parser.add_argument("--city", help="the city to filter by", type=validate_name)
    q_parser.add_argument("--breakfast", help="filter by breakfast inclusiveness", choices=['yes', 'no'])
    q_parser.set_defaults(func=query)
    # args = parser.parse_args(input("Enter arguments: ").split())
    args = parser.parse_args('q --city Berlin'.split())
    # args = parser.parse_args('s -d italy -s 2021-11-15 -e 2021-11-21'.split())
    # args = parser.parse_args()
    args.func(args)
    # while True:
    #
    #
