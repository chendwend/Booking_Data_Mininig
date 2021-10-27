-- drop database booking_data;
  
CREATE DATABASE IF NOT EXISTS booking_data;
ALTER DATABASE booking_data CHARACTER SET utf8;
USE booking_data;

CREATE TABLE location_dates (
	id INT AUTO_INCREMENT PRIMARY KEY,
	location VARCHAR(100) NOT NULL,
	sub_location VARCHAR(100) NOT NULL,
    	sub_location_latitude FLOAT DEFAULT NULL,
    	sub_location_longitude FLOAT DEFAULT NULL,
    	site_name VARCHAR(100) NOT NULL,
	from_date DATE NOT NULL,
    	to_date DATE NOT NULL,
	UNIQUE (location, sub_location, site_name, from_date, to_date) 
);

CREATE TABLE site_info (
	site_id INT AUTO_INCREMENT PRIMARY KEY,	
  	location_dates_id INT NOT NULL,
	rating FLOAT(2) DEFAULT NULL,
	reviewers_amount SMALLINT DEFAULT NULL,
	free_cancellation TINYINT(1) DEFAULT NULL,
	parking TINYINT(1) DEFAULT NULL,
	breakfast TINYINT(1) DEFAULT NULL,
	pets TINYINT(1) DEFAULT NULL,
	price INT NOT NULL,
    	date_time DATETIME NOT NULL,
    	temperature INT DEFAULT NULL,
    	feelslike INT DEFAULT NULL, 
	UNIQUE (location_dates_id),
	FOREIGN KEY (location_dates_id) REFERENCES location_dates(id) ON DELETE CASCADE
);

CREATE TABLE facilities (
	site_id INT AUTO_INCREMENT PRIMARY KEY,
    	location_dates_id INT NOT NULL,
	kitchen TINYINT(1) DEFAULT NULL,
	wifi TINYINT(1) DEFAULT NULL,
	air_conditioning TINYINT(1) DEFAULT NULL,
	UNIQUE (location_dates_id),
    	FOREIGN KEY (location_dates_id) REFERENCES location_dates(id) ON DELETE CASCADE
);
