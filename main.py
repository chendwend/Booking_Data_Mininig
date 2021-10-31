from gevent import monkey

monkey.patch_all(thread=False, select=False)  # required for grequests to be executed before imports
from sources.sql_functions import insert_to_db, query_sql
from utilities.config import WEB_SOURCE, FILE_NAME, OUTPUT_DIR, BASE_STATEMENT, SERVICE_AVAILABILITY, QUERY_OUTPUT_FILE, \
    LOGGING_FILE
from sources.weather_api import weather_api
from sources.source_page import Website
from datetime import datetime
from time import perf_counter
from argparse import ArgumentParser, ArgumentTypeError
import logging
import sys
import os
import csv

log_path = os.path.join(OUTPUT_DIR, LOGGING_FILE)
logging.basicConfig(filename=log_path,
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


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
            logging.critical(f'date provided: {date} - is in the past')
            sys.exit()
    except ValueError:
        msg = f"Not a valid date: {s}"
        logging.critical(f'date provided: {date} - not valid')
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
        logging.critical(f"the string {destination} is not alphanumeric.")
        sys.exit()

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
    weather_api(path1, path2)
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
    args = {k: v for k, v in args.items() if v is not None and (k not in ['func'])}
    statement = BASE_STATEMENT
    if "city" in args:
        operators.append(f"LOWER(sub_location) = LOWER('{args['city']}')")
    if "free_cancellation" in args:
        operators.append(f"free_cancellation = {SERVICE_AVAILABILITY[args['free_cancellation']]}")

    if "rating" in args:
        operators.append(f"rating >= {args['rating']}")
    if "reviewers_amount" in args:
        operators.append(f"reviewers_amount >= {args['reviewers_amount']}")

    if operators:
        statement += " WHERE " + " and ".join(operators)
        print(statement)
    query_response = query_sql(statement)
    logging.info(f"query request: \n {statement} \n - retrieved successfully")
    # for response in query_response[:10]:
    #     print(response)

    # Save results to csv file
    path = os.path.join(OUTPUT_DIR, QUERY_OUTPUT_FILE)
    keys = query_response[0].keys()
    with open(path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(query_response)
        logging.info(f"query response saved to file {path}.")


if __name__ == '__main__':
    parser = ArgumentParser(description="Extract data from Booking.com or Query the DB")
    subparsers = parser.add_subparsers(help='sub-command help')  # dest='subcommand'
    q_parser = subparsers.add_parser("q", help="Query help")  # query parser
    s_parser = subparsers.add_parser("s", help="Scrape help")  # scraper parser

    # scraper parser arguments
    s_parser.add_argument("-s", "--start_date", help="Start date - format YYYY-MM-DD ", required=True,
                          type=validate_date)
    s_parser.add_argument("-e", "--end_date", help="End date - format YYYY-MM-DD ", required=True, type=validate_date)
    s_parser.add_argument('-d', "--destination", help="Desired country", required=True, type=validate_name)
    s_parser.set_defaults(func=scraper)

    # query parser arguments
    q_parser.add_argument("--city", help="filter by city", type=validate_name)
    q_parser.add_argument("--free_cancellation", help="filter by free cancellation", choices=['yes', 'no'])
    q_parser.add_argument("--reviewers_amount", help="filter by reviewers amount", type=int)
    q_parser.add_argument("--rating", help="filter by rating", type=float)
    q_parser.set_defaults(func=query)

    # args = parser.parse_args('q --city Binz --breakfast yes'.split())
    # args = parser.parse_args('q --city Milan'.split())
    # args = parser.parse_args('s -d italy -s 2021-11-15 -e 2021-11-21'.split())
    args = parser.parse_args()
    args.func(args)
