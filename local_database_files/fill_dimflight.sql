SET SQL_SAFE_UPDATES=0;



-- First, add the columns start_date and end_date to DimFlight
ALTER TABLE DimFlight
ADD COLUMN start_date DATE AFTER flight_id,
ADD COLUMN end_date DATE AFTER start_date;

-- Insert new flights into DimFlight from OLTP
INSERT INTO DimFlight (flight_id, flightnumber, departure_time, arrival_time, duration, stops, start_date, end_date)
SELECT flight_id, flightnumber, departure_time, arrival_time, duration, stops, NOW(), NULL
FROM airlines_database.flight
WHERE flight_id NOT IN (SELECT flight_id FROM DimFlight);

-- Create temporary table to hold updated flights
CREATE TEMPORARY TABLE temp_flights
SELECT DF.flight_key, f.flightnumber, f.departure_time, f.arrival_time, f.duration, f.stops
FROM DimFlight DF
INNER JOIN airlines_database.flight f ON DF.flight_id = f.flight_id
WHERE DF.end_date IS NULL AND (
DF.flightnumber <> f.flightnumber OR
DF.departure_time <> f.departure_time OR
DF.arrival_time <> f.arrival_time OR
DF.duration <> f.duration OR
DF.stops <> f.stops
);

-- Set end_date for updated flights in DimFlight
UPDATE DimFlight DF
INNER JOIN temp_flights TF ON DF.flight_key = TF.flight_key
SET DF.end_date = DATE_SUB(NOW(), INTERVAL 1 DAY)
WHERE DF.end_date IS NULL;

-- Insert new records for updated flights into DimFlight
INSERT INTO DimFlight (flight_id, flightnumber, departure_time, arrival_time, duration, stops, start_date, end_date)
SELECT TF.flight_key, TF.flightnumber, TF.departure_time, TF.arrival_time, TF.duration, TF.stops, NOW(), NULL
FROM temp_flights TF;

-- Update end_date for any flights that have been deleted from OLTP
UPDATE DimFlight DF
LEFT JOIN airlines_database.flight f ON DF.flight_id = f.flight_id
SET DF.end_date = DATE_SUB(NOW(), INTERVAL 1 DAY)
WHERE f.flight_id IS NULL AND DF.end_date IS NULL;

-- Update start_date for any flights that have been added to OLTP
INSERT INTO DimFlight (flight_id, flightnumber, departure_time, arrival_time, duration, stops, start_date, end_date)
SELECT f.flight_id, f.flightnumber, f.departure_time, f.arrival_time, f.duration, f.stops, NOW(), NULL
FROM airlines_database.flight f
WHERE f.flight_id NOT IN (SELECT flight_id FROM DimFlight);

-- Clean up temporary table
DROP TEMPORARY TABLE IF EXISTS temp_flights;
