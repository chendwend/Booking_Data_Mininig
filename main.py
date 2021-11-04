from gevent import monkey

monkey.patch_all(thread=False, select=False)  # required for grequests to be executed before imports
from sources.sql_functions import insert_to_db, query_sql, establish_connection
from utilities.config import WEB_SOURCE, OUTPUT_DB_CSV, OUTPUT_DIR, BASE_STATEMENT, SERVICE_AVAILABILITY, \
    QUERY_OUTPUT_FILE, LOGGING_FILE, MAX_NUMBER_OF_PAGES
from sources.weather_api import weather_api
from sources.source_page import Website
from time import perf_counter
from argparse import ArgumentParser
from sources.input_validation_functions import validate_date, validate_name, validate_rating, validate_reviewers_amount
import logging
import os
import csv
import pandas as pd

log_path = os.path.join(OUTPUT_DIR, LOGGING_FILE)
logging.basicConfig(filename=log_path,
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO,
                    filemode='w')


def scraper(args):
    """
    scrapes the website and updates the DB

    :param args: arguments from user
    :type args: parser.parse_args object
    """
    establish_connection()

    start = perf_counter()

    website = Website(WEB_SOURCE, args.page_limit)
    website.insert_location(args.destination)
    website.select_date(args.start_date, args.end_date)
    data, pages = website.get_all_data()
    website.teardown()

    csv_path = os.path.join(OUTPUT_DIR, OUTPUT_DB_CSV)
    df_no_weather = pd.DataFrame(data=data)
    df = weather_api(df_no_weather)
    df.to_csv(csv_path, index=False)
    insert_to_db(args.start_date, args.end_date, args.destination, csv_path)
    time = perf_counter() - start
    print(
        f"Basic processing information for destination ='{args.destination}',"
        f" between {args.start_date.date()} and {args.end_date.date()}:")
    logging.debug(f"time of execution: {time / 60:.2f}")
    print(f"Number of total pages = {pages}")
    print(f"Execution time: {time / 60:.2f} minutes")


def query(args):
    """
    Constructs the query for the SQL DB, queries the DB and returns the result in a csv file

    :param args: arguments from user
    :type args: parser.parse_args object
    """
    # This list will hold all the extra conditionals
    establish_connection()
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

    query_response = query_sql(statement)
    logging.info(f"query request: retrieved successfully")
    if not query_response:
        logging.info(f"query request is empty.")

    # Save results to csv file
    path = os.path.join(OUTPUT_DIR, QUERY_OUTPUT_FILE)
    try:
        keys = query_response[0].keys()
        with open(path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(query_response)
            logging.info(f"query response saved to file {path}.")
    except IndexError:
        logging.warning(f"query response is empty.")


if __name__ == '__main__':
    # Verify output directory exists
    if not os.path.exists(OUTPUT_DIR):
        logging.info(f"output directory {OUTPUT_DIR} was created.")
        os.mkdir(OUTPUT_DIR)
    else:
        logging.info(f"output directory {OUTPUT_DIR} exists.")

    parser = ArgumentParser(description="Extract data from Booking.com or Query the DB")
    subparsers = parser.add_subparsers(help='sub-command help')  # dest='subcommand'
    q_parser = subparsers.add_parser("q", help="Query help")  # query parser
    s_parser = subparsers.add_parser("s", help="Scrape help")  # scraper parser

    # scraper parser arguments
    s_parser.add_argument("-s", "--start_date", help="Start date - format YYYY-MM-DD ", required=True,
                          type=validate_date)
    s_parser.add_argument("-e", "--end_date", help="End date - format YYYY-MM-DD ", required=True, type=validate_date)
    s_parser.add_argument('-d', "--destination", help="Desired country", required=True, type=validate_name)
    s_parser.add_argument('-p', '--page_limit', help="maximum number of pages to process", default=1, type=int,
                          choices=range(1, MAX_NUMBER_OF_PAGES + 1))
    s_parser.set_defaults(func=scraper)

    # query parser arguments
    q_parser.add_argument("--city", help="filter by city", type=validate_name)
    q_parser.add_argument("--free_cancellation", help="filter by free_cancellation", choices=['yes', 'no'])

    q_parser.add_argument("--reviewers_amount", help="filter by reviewers amount", type=validate_reviewers_amount)
    q_parser.add_argument("--rating", help="filter by rating", type=validate_rating)
    q_parser.set_defaults(func=query)

    # args = parser.parse_args('q --city Binz --breakfast yes'.split())
    # args = parser.parse_args()
    # args = parser.parse_args('s -d italy -s 2021-11-15 -e 2021-11-21 -p 3'.split())
    args = parser.parse_args()

    try:  # when no arguments are provided
        args.func(args)
    except AttributeError:
        logging.error(f"No arguments provided.")
        exit(1)
