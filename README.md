Data Mining Project - Booking.com Webscraper
============================  
A booking.com webscraper project 
## General Information
- In this project we scrape the website Booking.com using Selenium.
- The user inputs a desired country, check-in and check-out dates
- based on that input, specific data is collected from all page results and stored in a local SQL Database

## Installation
1. Install MySQL server from [MySQL server Download](https://dev.mysql.com/downloads/mysql/).
2. Install Python 3.7 or above 
3. Create a new project directory in your local machine and clone the repository into it.
4. Inside the project directory create a virtual environment and activate it:    
  Creating the environment (Windows & Linux):
  ```bash
  python -m venv venv
  ```
  <ins> Activating the environment: </ins>  
  For Linux  
  ```bash
  source venv/bin/activate
  ```
  For Windows   
  ```bash
  venv\Scripts\activate.bat
  ```
5. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.txt file. 
```bash
pip install -r requirements.txt
```

## Project Structure
    .
    ├── sources                 # Source files
    ├── test                    # Automated tests 
    ├── utilities               # Config & Logfiles
    ├── mysql_booking.sql       # SQL script for DB creation
    ├── requirements.txt        # package requirements 
    └── ERD.png                 # Entity Relationship Diagram 
### Source files
    .
    ├── ...
    ├── sources                 # Source files
    │   ├── main                # main file from which to run the program 
    │   ├── source_page.py      # A class to represent a booking.com website element
    │   ├── page.py             # A Class to represent each page in a search result
    │   ├── element.py          # A base class from which other classes inherit
    │   ├── from_csv_to_db.py   # A function to update DB with scraped data
    │   └── place_of_stay.py    # A Class to represent each place of stay
    └── ...
## Usage
When running for the first time, create the DB by running the  mysql_booking.sql script in your local MySQL server.
To run the program, Use the command-line interfaces to enter your input:
```bash
main.py [-h] -d DESTINATION -s START_DATE -e END_DATE
```
**DESTINATION** - Desired country   
**START_DATE**  - Check-in date in format %Y-%m-%d, where Y = year (4 digits), m = month (up to 2 digits), d = day (up to 2 digits)  
**END_DATE**    - Check-out date in format %Y-%m-%d, where Y = year (4 digits), m = month (up to 2 digits), d = day (up to 2 digits)

example run:
```bash
main.py -d germany -s 2021-08-15 -e 2021-08-21
```
All you need to do now is wait... \
For this input it might take about 10 minutes so go make yourself a cup of coffee.

## Output
The output is stored in a local SQL Database which was created previously.

### SQL DB Design  
![This is an image](/ERD.png)

```
    site_location
    └── Website                 
        ├── Page                
        │   ├── Place_of_stay                
        │   ├── Place_of_stay      
        │   └── ...    
        ├── Page
        └── ...
```     

## Implementation
### Special Libraries
- We utilized Selenium library to scrap information from Booking website.
- We also use the argparse module to make a user-friendly command-line interface.
- The SQL Database is updated via PyMySQL library.

### Code Structure
From the code structure perspective, Our project is implemented in a hierarchial manner with 4 classes:
- The Website class: Represents the booking website main page. Instantiates Page objects.  
- The Page class: Represents a page from the search result.  Instantiates Place_of_stay objects  
- The Place_of_stay Clas: Represents the availability page (when pressing "availability" button for each place of stay). 
- The Elemet Class: A custom defined base class with recurring methods to be used by all other classes. All classes mentioned above inherit from it.  
Here is a diagram depicting the relations:

```
    Element
    └── Website                 
        ├── Page                
        │   ├── Place_of_stay                
        │   ├── Place_of_stay      
        │   └── ...    
        ├── Page
        └── ...
```     
### Scrapable Information Structure
- Presently "Booking.com" limits search results to 40 pages. 
- Each page result contains up to 25 sub locations. 
- Each sub location result is divided into 2 parts: lower & upper element. These elements hold different information which we would like to scrape.  
  Each can be found using appropriate selector.
- Each sub location has also "availability" button that opens up a new page containing "Facilities" - more elaborate information, which we also scrape. Here we use one selector and filter with appropriate string.

### The Algorithmic Steps
1. Accept country, check-in & check-out dates from user.
2. Instantiate a Webdriver element with booking URL.
3. Find the searchbar and insert country. Press search button.
4. Find the calenader and insert corresponding dates. Press search button.
5. Get URLs of all page results.
6. For each page URL:
   - click the link. 
   - Find all upper and lower elements and extract relevant information
   - for each sub location inside the page, press the "availability" button and extract more information.
8. All results are stored in an intermediary data.csv file.
9. Update the Database using the data.csv file.
