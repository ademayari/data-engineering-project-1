CREATE DATABASE AirFaresDWH;

USE AirFaresDWH;

CREATE TABLE DimDate (
  date_key INT PRIMARY KEY AUTO_INCREMENT,
  date_current DATE NOT NULL,
  date_full VARCHAR(30) NOT NULL,
  day_Of_month INT NOT NULL,
  day_suffix VARCHAR(2) NOT NULL,
  day_name VARCHAR(10) NOT NULL,
  day_of_week INT NOT NULL,
  day_of_week_in_month INT NOT NULL,
  day_of_week_in_year INT NOT NULL,
  day_of_quarter INT NOT NULL,
  day_of_year INT NOT NULL,
  week_of_month INT NOT NULL,
  week_of_quarter INT NOT NULL,
  week_of_Year INT NOT NULL,
  month_current INT NOT NULL,
  month_name VARCHAR(10) NOT NULL,
  month_of_quarter INT NOT NULL,
  quarter_current INT NOT NULL,
  quarter_name VARCHAR(10) NOT NULL,
  year_current INT NOT NULL,
  year_name VARCHAR(4) NOT NULL,
  month_year VARCHAR(6) NOT NULL,
  mmyyyyy VARCHAR(6) NOT NULL
);


CREATE TABLE DimFlight (
    flight_key INT PRIMARY KEY,
    flight_id INT NOT NULL,
    flightnumber VARCHAR(10),
    departure_time TIME,
    arrival_time TIME,
    duration INT,
    stops INT
);


CREATE TABLE DimAirline (
    airline_key INT PRIMARY KEY NOT NULL,
    airline_code VARCHAR(2),
    airline_name VARCHAR(255),
    country VARCHAR(255)
);


CREATE TABLE DimAirport (
    airport_key INT PRIMARY KEY NOT NULL,
    airport_code VARCHAR(10) NOT NULL,
    airport_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);

CREATE TABLE FactFlightData (
  fact_flight_key INT NOT NULL,
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