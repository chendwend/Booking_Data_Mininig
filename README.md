# Scraping booking.com

In this project we scrape the website booking.com, collect specific data and organize the data in dictionaries.
By selecting the destination country, the check-in and check-out dates by the user, the python program is connecting to the booking.com website and downloading specific data from any relevant stays which is available by the search on the booking website.
From each stay we will save the name, sub-location, rating, number of reviews, etc.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.txt file. One can find it under the utilities folder.

```bash
pip freeze > requirements.txt
```

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
