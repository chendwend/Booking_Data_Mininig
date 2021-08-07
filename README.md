# Scraping Booking.com website

In this project we scrape the website Booking.com, collect specific data and organize the data in dictionaries.
By selecting the destination country, the check-in and check-out dates by the user, the python program is connecting to the Booking.com website and downloading specific data from any relevant stay which is available by the search on the Booking website.
From each stay we will save the name of the stay, the location, the rating, the number of reviews, the price and the maximum number of persons.

## Installation

Create & activate virtual environment on bare Python installation: \
Create: (inside main project folder):
```bash
python -m venv venv
```
Activate:
```bash
source venv/bin/activate
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.txt file. 
```bash
pip install -r requirements.txt
```
For this project you will need a WebDriver and adding executables to your PATH \
For more information you can check the link below: \
[driver_requirements](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/)
## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
