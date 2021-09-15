CREATE DATABASE IF NOT EXISTS booking_data;

USE booking_data;

CREATE TABLE sub_location (
  location_id INT NOT NULL PRIMARY KEY,
  location VARCHAR(100) NOT NULL 
);

CREATE TABLE site_basic_info (
site_id INT NOT NULL PRIMARY KEY,
site_name VARCHAR(100) NOT NULL,
location_id INT NOT NULL,
price INT DEFAULT NULL,
max_people SMALLINT DEFAULT NULL,
rating FLOAT(2) DEFAULT NULL,
reviewers_amount SMALLINT DEFAULT NULL,
FOREIGN KEY (location_id) REFERENCES sub_location(location_id) ON DELETE CASCADE
);

CREATE TABLE site_more_info (
site_id INT NOT NULL PRIMARY KEY,
free_cancellation TINYINT(1) DEFAULT NULL,
parking TINYINT(1) DEFAULT NULL,
breakfast TINYINT(1) DEFAULT NULL,
pets TINYINT(1) DEFAULT NULL,
FOREIGN KEY (site_id) REFERENCES site_basic_info(site_id) ON DELETE CASCADE
);

CREATE TABLE room_facilities (
site_id INT NOT NULL PRIMARY KEY,
kitchen TINYINT(1) DEFAULT NULL,
wifi TINYINT(1) DEFAULT NULL,
air_conditioning TINYINT(1) DEFAULT NULL,
FOREIGN KEY (site_id) REFERENCES site_basic_info(site_id) ON DELETE CASCADE
);

-- drop database booking_data;


