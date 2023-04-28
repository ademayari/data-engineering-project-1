
--Eerst moeten de kolommen start_date en end_date worden toegevoegd aan dimflight
ALTER TABLE DimFlight
ADD COLUMN start_date DATE AFTER flight_id;

ALTER TABLE DimFlight
ADD COLUMN end_date DATE AFTER flight_id;


-- Insert new flights into DimFlight from OLTP
INSERT INTO DimFlight (flight_id, flightnumber, departure_time, arrival_time, duration, stops, start_date, end_date)
SELECT flight_id, flightnumber, departure_time, arrival_time, duration, stops, NOW(), NULL
FROM database_airlines.flight
WHERE flight_id NOT IN (SELECT flight_id FROM DimFlight);

select * from dimflight;

-- Create temporary table to hold updated flights
CREATE TEMPORARY TABLE temp_flights
SELECT DF.flight_key, f.flightnumber, f.departure_time, f.arrival_time, f.duration, f.stops
FROM DimFlight DF
INNER JOIN database_airlines.flight f ON DF.flight_id = f.flight_id
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
SELECT TF.flightnumber, TF.flightnumber, TF.departure_time, TF.arrival_time, TF.duration, TF.stops, NOW(), NULL
FROM temp_flights TF;

select * from dimflight;