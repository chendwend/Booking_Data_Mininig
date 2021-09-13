import pymysql.cursors


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur = connection.cursor()
cur.execute('CREATE DATABASE IF NOT EXISTS porto')
csv_file = open(FILE_NAME, "r")
reader = csv.DictReader(csv_file)
for i, row in enumerate(tqdm(reader, total=N_ROWS)):
    the_date_time = datetime.utcfromtimestamp(int(row['TIMESTAMP']))
    gps_list = json.loads(row['POLYLINE'])
    number_points = len(gps_list)
    insert_query = '''INSERT INTO trips (trip_id, taxi_id, start_year, start_month, start_day, start_hour, nb_points) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    the_values = (i, row.get('TAXI_ID'), the_date_time.year, the_date_time.month, the_date_time.day, the_date_time.hour, number_points)
    cur.execute(insert_query, the_values)
    if i != 0 and i % 10000 == 0:
        connection.commit()
connection.commit()
csv_file.close()
cur.close()
connection.close()