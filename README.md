# Scraping Booking.com website

In this project we scrape the website Booking.com, collect specific data and organize the data in dictionaries.
By selecting the destination country, the check-in and check-out dates by the user, the python program is connecting to the Booking.com website and downloading specific data from any relevant stay which is available by the search on the Booking website.
From each stay we will save the name of the stay, the location, the rating, the number of reviews, the price and the maximum number of persons.

## Installation
After downloading the Data_mininig_project_2021 directory to your computer (or clone the repository from the github) you will need to creat an empty virtual environment.  
Create & activate virtual environment on bare Python installation: \
Create: (inside main project folder):
```bash
python -m venv venv
```
Activate: \
Linux: 
```bash
source venv/bin/activate
```
Windows: 
```bash
venv\Scripts\activate.bat
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.txt file. 
```bash
pip install -r requirements.txt
```
For this project you will need a WebDriver and adding executables to your PATH \
For more information you can check the link below: \
[driver_requirements](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/)
## Usage

For running the program one need to find the main.py file under the sources directory.
runing the main.py file with no input will generate the usage message below:

```bash
usage: main.py [-h] -d DESTINATION -s START_DATE -e END_DATE
main.py: error: the following arguments are required: -d/--destination, -s/--start_date, -e/--end_date
```
Use the command-line interfaces to enter your input, for example:

```bash
main.py -d germany -s 2021-08-15 -e 2021-08-21
```
All you need to do now is wait... \
For this input it might take about 10 minutes so go make yourself a cup of coffee.

## The output
The output is a list of dictionaries, one dictionary for example: \
{'name': 'Wyndham Stuttgart Airport Messe', 'location': 'Stuttgart', 'rating': '8', 'reviewers_amount': '3', 'price': 1616, 'max persons': '2'} \
Each dictionary contain the data about one stay that match the location and available be the dates the user specified.

