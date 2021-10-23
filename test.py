
import requests

params = {
  'access_key': 'c97f8ed4ab7a775dd2abe77f28bac6be',
  'query': 'Milan',
  'forecast_days': 3,
  'hourly': 1
 }

type_of_request = 'forecast'
api_result = requests.get(f'http://api.weatherstack.com/{type_of_request}', params)

api_response = api_result.json()

city = api_response['location']['name']
language = api_response['request']['language']
lat = api_response['location']['lat']
lon = api_response['location']['lon']
temperature = api_response['current']['temperature']
wind_speed = api_response['current']['wind_speed']
feelslike = api_response['current']['feelslike']
print(f"Information for {city}:\n"
      f"language = {language}, lat:lon = {lat}/{lon},\n"
      f"temperature = {temperature}, wind speed = {wind_speed},\n"
      f"feels like = {feelslike}")
a = 5