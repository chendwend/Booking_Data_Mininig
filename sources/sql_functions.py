from datetime import datetime
import pymysql.cursors
from pymysql.err import OperationalError
import csv
import logging
from utilities.config import DB_NAME, PASSWORD, OUTPUT_DIR

logger = logging.getLogger()


def establish_connection():
    """
    The function connecting to the DB and creating a cursor.
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Kostya',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     database=DB_NAME)
    except OperationalError as err:
        if err.args[0] == 1045:
            logger.error(f"Wrong password was provided to the sql connection")
            print(f"Wrong password was provided to the sql connection")
        elif err.args[0] == 1049:
            logger.error(f"The DB was not created.")
            print(f"The DB was not created")
        else:
            logger.error(f"error: {err}")
            print(f"error: {err}")
        exit()
    cur = connection.cursor()
    logger.info(f"connection to DB established successfully")
    return connection, cur


def close_connection(connection, cursor):
    """
    closes connection to SQL database

    :param connection:  pymysql.connect object
    :param cursor: connection.cursor() object
    """
    cursor.close()
    connection.close()


def query_sql(statement):
    """
    queries the SQL DB with given statement and returns the response

    :param statement: SQL query
    :type statement: str
    :return: dictionary with sql query responses
    :rtype: dict
    """
    connection, cur = establish_connection()
    cur.execute(statement)
    result = cur.fetchall()
    close_connection(connection, cur)
    return result


def insert_to_db(from_date, to_date, location, file_path):
    """
    The function receives dates and location and inserts it with the data from the csv file
    to the different tables in the DB.
    """

    connection, cur = establish_connection()

    # cur.execute('''drop database booking_data''')
    # cur.execute('''CREATE DATABASE IF NOT EXISTS booking_data''')
    # cur.execute('''ALTER DATABASE booking_data CHARACTER SET utf8''')
    # cur.execute('''USE booking_data''')
    #
    # cur.execute('''CREATE TABLE location_dates (
    #                 id INT AUTO_INCREMENT PRIMARY KEY,
    #                 location VARCHAR(100) NOT NULL,
    #                 sub_location VARCHAR(100) NOT NULL,
    #                 sub_location_latitude FLOAT DEFAULT NULL,
    #                 sub_location_longitude FLOAT DEFAULT NULL,
    #                 site_name VARCHAR(100) NOT NULL,
    #                 from_date DATE NOT NULL,
    #                 to_date DATE NOT NULL,
    #                 UNIQUE (location, sub_location, site_name, from_date, to_date)
    #                                             )'''
    #             )
    # cur.execute('''CREATE TABLE site_info (
    #                 site_id INT AUTO_INCREMENT PRIMARY KEY,
    #                 location_dates_id INT NOT NULL,
    #                 rating FLOAT(2) DEFAULT NULL,
    #                 reviewers_amount SMALLINT DEFAULT NULL,
    #                 free_cancellation TINYINT(1) DEFAULT NULL,
    #                 parking TINYINT(1) DEFAULT NULL,
    #                 breakfast TINYINT(1) DEFAULT NULL,
    #                 pets TINYINT(1) DEFAULT NULL,
    #                 price INT NOT NULL,
    #                 date_time DATETIME NOT NULL,
    #                 temperature INT DEFAULT NULL,
    #                 feelslike INT DEFAULT NULL,
    #                 UNIQUE (location_dates_id),
    #                 FOREIGN KEY (location_dates_id) REFERENCES location_dates(id) ON DELETE CASCADE
    #                                         )'''
    #             )
    # cur.execute('''CREATE TABLE facilities (
    #                 site_id INT AUTO_INCREMENT PRIMARY KEY,
    #                 location_dates_id INT NOT NULL,
    #                 kitchen TINYINT(1) DEFAULT NULL,
    #                 wifi TINYINT(1) DEFAULT NULL,
    #                 air_conditioning TINYINT(1) DEFAULT NULL,
    #                 UNIQUE (location_dates_id),
    #                 FOREIGN KEY (location_dates_id) REFERENCES location_dates(id) ON DELETE CASCADE
    #                                         )'''
    #             )
    # path = os.path.join(OUTPUT_DIR, file)
    csv_file = open(file_path, "r", encoding="utf-8")
    reader = csv.DictReader(csv_file)
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    for row in enumerate(reader):
        row = row[1]

        # filling the location_dates table, because we defined that
        # (location, sub_location, site_name, from_date, to_date) are unique key, we check if this combination
        # is already exist, and insert if it isn't.
        insert_query_1 = '''INSERT INTO location_dates (location, sub_location, sub_location_latitude, 
                                                        sub_location_longitude, site_name, from_date, to_date)
                            SELECT * FROM (SELECT %s AS location, %s AS sub_location, %s AS sub_location_latitude, 
                                           %s AS sub_location_longitude, %s AS site_name, %s AS from_date, 
                                           %s AS to_date) AS temp
                            WHERE NOT EXISTS(SELECT location, sub_location, site_name, from_date, to_date 
                                             FROM location_dates 
                                             WHERE location = %s and sub_location = %s and site_name = %s and
                                                   from_date = %s and to_date = %s
                                             )LIMIT 1
                                             '''

        values_1 = (location, row.get('sub_location'), row.get('latitude'),
                    row.get('longitude'), row.get('site_name'), from_date, to_date, location,
                    row.get('sub_location'), row.get('site_name'), from_date, to_date)

        cur.execute(insert_query_1, values_1)

        # getting the id from the location_dates table to use as foreign key in the site_info table.
        query_id = '''SELECT id
                      FROM location_dates
                      WHERE location=%s and sub_location=%s and site_name=%s and from_date=%s and to_date=%s'''
        cur.execute(query_id, (location, row.get('sub_location'), row.get('site_name'), from_date, to_date))
        result_id = cur.fetchone()
        the_id = result_id["id"]

        # filling the site_info table with the option to update existing rows.
        insert_query_2 = '''INSERT INTO site_info (location_dates_id, rating, reviewers_amount,
                                                   free_cancellation, parking, breakfast, pets, price,
                                                   date_time, temperature, feelslike)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                            rating = VALUES(rating),
                            reviewers_amount = VALUES(reviewers_amount),
                            free_cancellation = VALUES(free_cancellation),
                            parking = VALUES(parking),
                            breakfast = VALUES(breakfast),
                            pets = VALUES(pets),
                            price = VALUES(price),
                            date_time = VALUES(date_time),
                            temperature = VALUES(temperature),
                            feelslike = VALUES(feelslike)'''
        values_2 = (the_id, row.get('rating'), row.get('reviewers_amount'),
                    row.get('free_cancellation'), row.get('parking'), row.get('breakfast'), row.get('pets'),
                    row.get('price'), formatted_date, row.get('temperature'), row.get('feelslike'))
        cur.execute(insert_query_2, values_2)

        # filling the facilities table with the option to update existing rows.
        insert_query_3 = '''INSERT INTO facilities (location_dates_id, kitchen, wifi, air_conditioning) 
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                            kitchen = VALUES(kitchen),
                            wifi = VALUES(wifi),
                            air_conditioning = VALUES(air_conditioning)'''
        values_3 = (the_id, row.get('kitchen'), row.get('wifi'), row.get('air conditioning'))
        cur.execute(insert_query_3, values_3)

    connection.commit()
    csv_file.close()
    close_connection(connection, cur)
    logger.info(f"DB connection closed.")
    logger.info(f"The DB was updated successfully.")
# csv_path = os.path.join(OUTPUT_DIR, OUTPUT_DB_CSV)
# insert_to_db("2021-11-26", "2021-12-29", "germany", csv_path)
