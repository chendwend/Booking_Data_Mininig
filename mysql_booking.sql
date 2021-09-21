CREATE DATABASE IF NOT EXISTS booking_data;
ALTER DATABASE booking_data CHARACTER SET utf8;
USE booking_data;

CREATE TABLE site_location (
	location_id INT AUTO_INCREMENT PRIMARY KEY,
	location VARCHAR(100) NOT NULL,
	sub_location VARCHAR(100) NOT NULL,
	UNIQUE (location, sub_location) 
);

CREATE TABLE site_info (
	site_id INT AUTO_INCREMENT PRIMARY KEY,
	location_id INT NOT NULL,
	site_name VARCHAR(100) NOT NULL,
	max_people SMALLINT DEFAULT NULL,
	rating FLOAT(2) DEFAULT NULL,
	reviewers_amount SMALLINT DEFAULT NULL,
	free_cancellation TINYINT(1) DEFAULT NULL,
	parking TINYINT(1) DEFAULT NULL,
	breakfast TINYINT(1) DEFAULT NULL,
	pets TINYINT(1) DEFAULT NULL,
	UNIQUE (location_id, site_name),
	FOREIGN KEY (location_id) REFERENCES site_location(location_id) ON DELETE CASCADE
);

CREATE TABLE price_offer (
   offer_id INT AUTO_INCREMENT PRIMARY KEY,
   location_id INT NOT NULL,
   site_id INT NOT NULL,
   price INT NOT NULL,
   from_date DATE NOT NULL,
   to_date DATE NOT NULL,
   date_time_update DATETIME NOT NULL,
   FOREIGN KEY (location_id) REFERENCES site_location(location_id) ON DELETE CASCADE,
   FOREIGN KEY (site_id) REFERENCES site_info(site_id) ON DELETE CASCADE,
   UNIQUE (location_id, site_id, from_date, to_date)
);

CREATE TABLE facilities (
	site_id INT PRIMARY KEY,
	kitchen TINYINT(1) DEFAULT NULL,
	wifi TINYINT(1) DEFAULT NULL,
	air_conditioning TINYINT(1) DEFAULT NULL,
	FOREIGN KEY (site_id) REFERENCES site_info(site_id) ON DELETE CASCADE
);
