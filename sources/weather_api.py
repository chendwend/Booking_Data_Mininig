import requests
import json
from utilities.config import COLUMNS, DEFAULT_VALUE, ACCESS_KEY, TYPE_OF_REQUEST
import pandas as pd
import logging
logger = logging.getLogger()


def weather_api(origin_df):
    """
    requests additional information using the weather
    API for the cities supplied in the 'sub_location' column.

    :param origin_csv: csv_file with scraped data
    :return: pd.DataFrame with added columns from the weather API
    """

    # Read csv file to pandas and initialize new columns
    df = origin_df.copy()
    df[COLUMNS] = DEFAULT_VALUE
    # go over all unique locations and update columns, thus saving api calls
    unique_sub_locations = df['sub_location'].unique()
    for sub_location in unique_sub_locations:
        # Parameters for api request
        params = {
            'access_key': ACCESS_KEY,
            'query': sub_location,
        }
        api_result = requests.get(f'http://api.weatherstack.com/{TYPE_OF_REQUEST}', params)
        api_result_json = json.loads(api_result.content)
        if "success" in api_result_json.keys():
            if api_result_json["success"] is False:  # error code for usage_limit_reached
                if api_result_json["error"]["code"] == 104:
                    logger.info(f"Monthly API subscription has reached its limit.")
                    break
                continue
        elif api_result.status_code != 200:  # for bad result, skip to next location
            logger.info(f"Weather API bad status code")
            continue
        else:
            api_response = api_result.json()

            lat = api_response['location']['lat']
            lon = api_response['location']['lon']
            temperature = api_response['current']['temperature']
            feelslike = api_response['current']['feelslike']

            df.loc[df['sub_location'] == sub_location, COLUMNS] = lat, lon, temperature, feelslike
    logger.info(f"Weather API finished all requests.")
    return df
