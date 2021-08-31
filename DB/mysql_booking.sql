CREATE DATABASE IF NOT EXISTS booking_data;
USE booking_data;

CREATE TABLE stays (
  stay_no INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  stay_name varchar(100) NOT NULL
);

CREATE TABLE stays_info (
id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
stay_no INT NOT NULL,
location varchar(100),
price FLOAT(2),
max_person SMALLINT,
FOREIGN KEY (stay_no) REFERENCES stays(stay_no) ON DELETE CASCADE
);

CREATE TABLE stays_rating (
id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
stay_no INT NOT NULL,
rating FLOAT(2),
reviewers_amount SMALLINT,
FOREIGN KEY (stay_no) REFERENCES stays(stay_no) ON DELETE CASCADE
);

-- drop database booking_data;


