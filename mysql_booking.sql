CREATE DATABASE IF NOT EXISTS booking_data;

USE booking_data;

CREATE TABLE location (
  location_id INT NOT NULL AUTO_INCREMENT,
  location VARCHAR(100) NOT NULL,
  PRIMARY KEY (location_id)
);

CREATE TABLE site_basic_info (
site_id INT NOT NULL AUTO_INCREMENT,
location_id INT NOT NULL,
site_name VARCHAR(100) NOT NULL,
price FLOAT(2),
max_people SMALLINT,
rating FLOAT(2),
reviewers_amount SMALLINT,
PRIMARY KEY (site_id),
FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE CASCADE
);

CREATE TABLE site_more_info (
info_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
site_id INT NOT NULL,
free_cancellation TINYINT(1),
parking TINYINT(1),
breakfast TINYINT(1),
pets TINYINT(1),
FOREIGN KEY (site_id) REFERENCES site_basic_info(site_id) ON DELETE CASCADE
);

CREATE TABLE room_facilities (
facilities_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
site_id INT NOT NULL,
kitchen TINYINT(1),
wifi TINYINT(1),
air_conditioning TINYINT(1),
FOREIGN KEY (site_id) REFERENCES site_basic_info(site_id) ON DELETE CASCADE
);

-- drop database booking_data;


