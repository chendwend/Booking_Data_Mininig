from datetime import datetime
import logging
from argparse import ArgumentTypeError
logger = logging.getLogger()


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
            exit()
    except ValueError:
        msg = f"Not a valid date: {s}"
        logging.critical(f'date provided: {date} - not valid')
        raise ArgumentTypeError(msg)
    return date


def validate_name(name):
    """
    Validates the given string to be alphanumeric.
    If not, exits the program.

    :param name: the string to validate
    :type name: str
    :return: the input
    :rtype: str
    """
    if not name.isalpha():
        logging.critical(f"the string {name} is not alphanumeric.")
        exit()

    return name


def validate_rating(rating):
    """
    Validates if rating is not string and is between [0,10].
    :param rating: rating
    :return: rating
    :rtype: float
    """
    if not isinstance(rating, float) and not isinstance(rating, int):
        logging.error(f"the given rating {rating} is not a number.")
        exit()
    rating = float(rating)
    if rating > 10 or rating < 0:
        logging.error(f"the given rating {rating} in a legal range [0,10].")
        exit()

    return rating


def validate_reviewers_amount(reviewers_amount):
    """
    Validates if reviewers_amount is integer and is not less than 0.

    :param reviewers_amount:
    :return: reviewers_amount
    :rtype: int
    """
    if not isinstance(reviewers_amount, int):
        logging.error(f"the given reviewers amount {reviewers_amount} is not an integer.")
        exit()
    reviewers_amount = int(reviewers_amount)
    if reviewers_amount < 0:
        logging.error(f"the given reviewers amount {reviewers_amount}< 0.")
        exit()

    return reviewers_amount
