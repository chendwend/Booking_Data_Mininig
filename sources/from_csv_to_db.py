import pymysql.cursors
import csv
from utilities.config import *


def insert_to_db():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 database='booking_data')
    cur = connection.cursor()
    #cur.execute('''SET sql_mode = ""''')
    csv_file = open(FILE_NAME, "r")
    reader = csv.DictReader(csv_file)
    cur.execute('USE booking_data')
    sub_location_dict = {}
    j = 0
    for i, row in enumerate(reader):
        location = row.get('location')
        location_lower = location.lower()
        if location_lower not in sub_location_dict:
            sub_location_dict[location_lower] = j + 1
            j += 1
            insert_query_1 = '''INSERT INTO sub_location (location_id, location) VALUES (%s, %s) '''
            values_1 = (sub_location_dict[location_lower], location)
            cur.execute(insert_query_1, values_1)

        insert_query_2 = '''INSERT INTO site_basic_info (site_id, site_name, location_id, 
        price, max_people, rating, reviewers_amount) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        values_2 = (i, row.get('name'), sub_location_dict[location_lower], row.get('Price'), row.get('Max people'), row.get('rating'), row.get('reviewers amount'))
        cur.execute(insert_query_2, values_2)

        insert_query_3 = '''INSERT INTO site_more_info (site_id, free_cancellation, parking, 
        breakfast, pets) VALUES (%s, %s, %s, %s, %s)'''
        values_3 = (i, row.get('Free Cancellations'), row.get('parking'), row.get('Breakfast'), row.get('pets'))
        cur.execute(insert_query_3, values_3)

        insert_query_4 = '''INSERT INTO room_facilities (site_id, kitchen, wifi, 
        air_conditioning) VALUES (%s, %s, %s, %s)'''
        values_4 = (i, row.get('kitchen'), row.get('wifi'), row.get('air conditioning'))
        cur.execute(insert_query_4, values_4)

    connection.commit()
    csv_file.close()
    cur.close()
    connection.close()
    print("The DB was created successfully")


