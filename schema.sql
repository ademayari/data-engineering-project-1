-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE `Airport` (
    `code` string  NOT NULL ,
    `name` string  NOT NULL ,
    `country` string  NOT NULL ,
    PRIMARY KEY (
        `code`
    ),
    CONSTRAINT `uc_Airport_name` UNIQUE (
        `name`
    )
);

CREATE TABLE `Flight` (
    `flight_id` string  NOT NULL ,
    `airline_code` string  NOT NULL ,
    `departure` string  NOT NULL DEFAULT bru,
    `destination` string  NOT NULL ,
    `departure_time` datetime  NOT NULL ,
    `arrival_time` datetime  NOT NULL ,
    `stops` int  NOT NULL ,
    PRIMARY KEY (
        `flight_id`
    )
);

CREATE TABLE `Flight_data` (
    `flight_id` string  NOT NULL ,
    `time_of_data` datetime  NOT NULL ,
    `price` float  NOT NULL ,
    `seats_left` int  NOT NULL ,
    PRIMARY KEY (
        `flight_id`,`time_of_data`
    )
);

CREATE TABLE `Airline` (
    `code` string  NOT NULL ,
    `name` string  NOT NULL ,
    `country` string  NOT NULL ,
    PRIMARY KEY (
        `code`
    )
);

ALTER TABLE `Flight` ADD CONSTRAINT `fk_Flight_airline_code` FOREIGN KEY(`airline_code`)
REFERENCES `Airline` (`code`);

ALTER TABLE `Flight` ADD CONSTRAINT `fk_Flight_departure` FOREIGN KEY(`departure`)
REFERENCES `Airport` (`code`);

ALTER TABLE `Flight` ADD CONSTRAINT `fk_Flight_destination` FOREIGN KEY(`destination`)
REFERENCES `Airport` (`code`);

ALTER TABLE `Flight_data` ADD CONSTRAINT `fk_Flight_data_flight_id` FOREIGN KEY(`flight_id`)
REFERENCES `Flight` (`flight_id`);

