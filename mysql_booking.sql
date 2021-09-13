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
price FLOAT(2),
max_people SMALLINT,
rating FLOAT(2),
reviewers_amount SMALLINT,
FOREIGN KEY (location_id) REFERENCES sub_location(location_id) ON DELETE CASCADE
);

CREATE TABLE site_more_info (
site_id INT NOT NULL PRIMARY KEY,
free_cancellation TINYINT(1),
parking TINYINT(1),
breakfast TINYINT(1),
pets TINYINT(1),
FOREIGN KEY (site_id) REFERENCES site_basic_info(site_id) ON DELETE CASCADE
);

CREATE TABLE room_facilities (
site_id INT NOT NULL PRIMARY KEY,
kitchen TINYINT(1),
wifi TINYINT(1),
air_conditioning TINYINT(1),
FOREIGN KEY (site_id) REFERENCES site_basic_info(site_id) ON DELETE CASCADE
);

-- drop database booking_data;


