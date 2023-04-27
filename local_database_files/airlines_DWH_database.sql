CREATE DATABASE AirFaresDWH;

USE AirFaresDWH;

CREATE TABLE DimDate (
    date_key INT PRIMARY KEY NOT NULL,   -- primay key.
    date_current DATETIME ,     -- date: 2008-08-18 00:00:00
    date_num INT(8),    -- numeric value, in YYYYMMDD, 20080818
    day_num INT (2),    -- numeric value, 18
    day_of_year INT(4), -- the day of the year 
    day_of_week INT(2), -- the day of the week
    day_of_week_name VARCHAR(20), -- day of week name (Monday, Tuesday,etc)
    week_num INT (2), --  week of the year 
    week_begin_date DATETIME,  -- week begin date
    week_end_date DATETIME, -- week end date
    last_week_begin_date DATETIME,  -- priore week begin date
    last_week_end_date DATETIME,   -- priore week end date
    last_2_week_begin_date  DATETIME,   -- priore two week begin date
    last_2_week_end_date DATETIME,  -- priore two ween end date
    month_num INT (2) ,  -- month in number, ie. 12
    month_name varchar(20),  -- month in name, ie. December
    YEARMONTH_NUM INT(6),  -- year and month in number, ie. 201212
    last_month_num INT (2), -- priore month in number, ie. 11
    last_month_name varchar(20), -- priore month in name, November
    last_month_year INT(4),  -- priore month in year, 2012
    last_yearmonth_num INT(6), -- priore year and month in  number, ie, 2o1211
    quarter_num INT (2),  -- quarter in number, ie 4
    year_num INT (4), -- year in number, ie, 2012
    created_date TIMESTAMP NOT NULL  ,  -- date record was created
    updated_date TIMESTAMP NOT NULL  -- date record was updated
);



CREATE TABLE DimFlight (
    flight_key INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    flight_id INT NOT NULL,
    flightnumber VARCHAR(10),
    departure_time TIME,
    arrival_time TIME,
    duration INT,
    stops INT
);


CREATE TABLE DimAirline (
    airline_key INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    airline_code VARCHAR(2),
    airline_name VARCHAR(255),
    country VARCHAR(255)
);


CREATE TABLE DimAirport (
    airport_key INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    airport_code VARCHAR(10) NOT NULL,
    airport_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);

CREATE TABLE FactFlightData (
  fact_flight_key INT AUTO_INCREMENT NOT NULL,
  arrival_date_key INT NOT NULL,
  departure_date_key INT NOT NULL,
  scrape_date_key INT NOT NULL,
  airline_key INT NOT NULL,
  arrival_airport_key INT NOT NULL,
  departure_airport_key INT NOT NULL,
  flight_key INT NOT NULL,
  seats_left INT,
  price DECIMAL(10,2),
  PRIMARY KEY (fact_flight_key),
  FOREIGN KEY (arrival_date_key) REFERENCES DimDate(date_key),
  FOREIGN KEY (departure_date_key) REFERENCES DimDate(date_key),
  FOREIGN KEY (scrape_date_key) REFERENCES DimDate(date_key),
  FOREIGN KEY (airline_key) REFERENCES DimAirline(airline_key),
  FOREIGN KEY (arrival_airport_key) REFERENCES DimAirport(airport_key),
  FOREIGN KEY (departure_airport_key) REFERENCES DimAirport(airport_key),
  FOREIGN KEY (flight_key) REFERENCES DimFlight(flight_key)
);






