import pymysql.cursors
import csv
from datetime import datetime
from utilities.config import FILE_NAME


def insert_to_db(from_date, to_date, location):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Kostya',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 database='booking_data')
    cur = connection.cursor()

    # cur.execute('''drop database booking_data''')
    # cur.execute('''CREATE DATABASE IF NOT EXISTS booking_data''')
    # cur.execute('''ALTER DATABASE booking_data CHARACTER SET utf8''')
    # cur.execute('''USE booking_data''')
    #
    # cur.execute('''CREATE TABLE site_location (
    #                location_id INT AUTO_INCREMENT PRIMARY KEY,
    #                location VARCHAR(100) NOT NULL,
    #                sub_location VARCHAR(100) NOT NULL,
    #                UNIQUE (location, sub_location)
    #                                           )'''
    #             )
    # cur.execute('''CREATE TABLE site_info (
    #                site_id INT AUTO_INCREMENT PRIMARY KEY,
    #                location_id INT NOT NULL,
    #                site_name VARCHAR(100) NOT NULL,
    #                max_people SMALLINT DEFAULT NULL,
    #                rating FLOAT(2) DEFAULT NULL,
    #                reviewers_amount SMALLINT DEFAULT NULL,
    #                free_cancellation TINYINT(1) DEFAULT NULL,
    #                parking TINYINT(1) DEFAULT NULL,
    #                breakfast TINYINT(1) DEFAULT NULL,
    #                pets TINYINT(1) DEFAULT NULL,
    #                UNIQUE (location_id, site_name),
    #                FOREIGN KEY (location_id) REFERENCES site_location(location_id) ON DELETE CASCADE
    #                                         )'''
    #             )
    # cur.execute('''CREATE TABLE price_offer (
    #                offer_id INT AUTO_INCREMENT PRIMARY KEY,
    #                location_id INT NOT NULL,
    #                site_id INT NOT NULL,
    #                price INT NOT NULL,
    #                from_date DATE NOT NULL,
    #                to_date DATE NOT NULL,
    #                date_time_update DATETIME NOT NULL,
    #                FOREIGN KEY (location_id) REFERENCES site_location(location_id) ON DELETE CASCADE,
    #                FOREIGN KEY (site_id) REFERENCES site_info(site_id) ON DELETE CASCADE,
    #                UNIQUE (location_id, site_id, from_date, to_date)
    #                                          )'''
    #             )
    # cur.execute('''CREATE TABLE facilities (
    #                site_id INT PRIMARY KEY,
    #                kitchen TINYINT(1) DEFAULT NULL,
    #                wifi TINYINT(1) DEFAULT NULL,
    #                air_conditioning TINYINT(1) DEFAULT NULL,
    #                FOREIGN KEY (site_id) REFERENCES site_info(site_id) ON DELETE CASCADE
    #                                         )'''
    #             )

    csv_file = open(FILE_NAME, "r", encoding="utf-8")
    reader = csv.DictReader(csv_file)
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    for row in enumerate(reader):
        row = row[1]

        insert_query_1 = '''INSERT INTO site_location (location, sub_location)
                            SELECT * FROM (SELECT %s AS location, %s AS sub_location) AS temp
                            WHERE NOT EXISTS(
                            SELECT location, sub_location FROM site_location WHERE location = %s and sub_location = %s
                            )LIMIT 1'''
        values_1 = (location, row.get('sub location'), location, row.get('sub location'))
        cur.execute(insert_query_1, values_1)

        query_location_id = '''SELECT location_id
                               FROM site_location
                               WHERE location = %s and sub_location = %s'''
        cur.execute(query_location_id, (location, row.get('sub location')))
        result_location = cur.fetchone()
        location_id = result_location["location_id"]

        insert_query_2 = '''INSERT INTO site_info (location_id, site_name, max_people, rating, 
                            reviewers_amount, free_cancellation, parking, breakfast, pets)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                            max_people = VALUES(max_people),
                            rating = VALUES(rating),
                            reviewers_amount = VALUES(reviewers_amount),
                            free_cancellation = VALUES(free_cancellation),
                            parking = VALUES(parking),
                            breakfast = VALUES(breakfast),
                            pets = VALUES(pets)'''
        values_2 = (location_id, row.get('name'), row.get('Max people'), row.get('rating'), row.get('reviewers amount'),
                    row.get('Free Cancellations'), row.get('parking'), row.get('Breakfast'), row.get('pets'))
        cur.execute(insert_query_2, values_2)

        query_site_id = '''SELECT site_id
                            FROM site_info
                            WHERE site_name = %s and location_id = %s'''
        cur.execute(query_site_id, (row.get('name'), location_id))
        result_site = cur.fetchone()
        site_id = result_site["site_id"]

        insert_query_3 = '''INSERT INTO price_offer (location_id, site_id, price, from_date, to_date, date_time_update) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                            price = %s'''
        values_3 = (location_id, site_id, row.get('Price'), from_date, to_date, formatted_date, row.get('Price'))
        cur.execute(insert_query_3, values_3)

        insert_query_4 = '''INSERT INTO facilities (site_id, kitchen, wifi, air_conditioning) 
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                            kitchen = VALUES(kitchen),
                            wifi = VALUES(wifi),
                            air_conditioning = VALUES(air_conditioning)'''
        values_4 = (site_id, row.get('kitchen'), row.get('wifi'), row.get('air conditioning'))
        cur.execute(insert_query_4, values_4)

    connection.commit()
    csv_file.close()
    cur.close()
    connection.close()
    print("The DB was updated successfully")
# insert_to_db("2021-10-20","2021-10-29","Germany")