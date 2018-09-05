CREATE DATABASE NVR;
use NVR;

CREATE TABLE NVR (
            id INT NOT NULL AUTO_INCREMENT,
            ip VARCHAR(20),
            name VARCHAR(40),
            add_date DATE,
            on_until_date DATETIME,
            off_until_date DATETIME,
            PRIMARY KEY (id));

CREATE TABLE EVENT (
            id INT NOT NULL,
            time DATETIME,
            status TINYINT(1));

CREATE TABLE CONF (
            time DATETIME);

insert into CONF (time) VALUES (NOW());