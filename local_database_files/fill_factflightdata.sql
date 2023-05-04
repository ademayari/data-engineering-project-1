SET FOREIGN_KEY_CHECKS=0;

INSERT INTO FactFlightData (arrival_date_key, departure_date_key, scrape_date_key, airline_key, arrival_airport_key, departure_airport_key, flight_key, seats_left, price)
SELECT
    CAST(date_format(arrival_date,'%Y%m%d') as unsigned) ,
    CAST(date_format(departure_date,'%Y%m%d') as unsigned),
    CAST(date_format(time_of_data,'%Y%m%d') as unsigned),
	da.airline_key,
    dar_arr.airport_key,
    dar_dep.airport_key,
    df.flight_key,
    fd.seats_left,
    fd.price
FROM
    airfares.flight_data fd
    JOIN airfares.flight f ON fd.flight_id = f.flight_id
    JOIN airfares.airport a_dep ON f.departure = a_dep.code
    JOIN airfares.airport a_arr ON f.destination = a_arr.code
    JOIN airfares.airline al ON al.code = f.airline_code
    JOIN dimairline da ON da.airline_code = al.code
    JOIN dimairport dar_arr ON dar_arr.airport_code = a_arr.code
    JOIN dimairport dar_dep ON dar_dep.airport_code = a_dep.code
    JOIN dimflight df ON df.flight_id = f.flight_id
	
WHERE
    fd.flight_data_id > (SELECT COALESCE(MAX(flight_data_id),0) FROM factflightdata)