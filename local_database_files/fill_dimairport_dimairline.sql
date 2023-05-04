USE AirFaresDWH;

SET SQL_SAFE_UPDATES = 0;

SET FOREIGN_KEY_CHECKS=0;

UPDATE dimairline da SET airline_name = (SELECT airline_name FROM airfares.airline WHERE airfares.airline.code = da.airline_code);

INSERT INTO dimairline (airline_code, airline_name, country)
SELECT code, airline_name, country
FROM airfares.airline
WHERE code NOT IN (SELECT DISTINCT airline_code FROM dimairline)
  AND country IS NOT NULL;

UPDATE dimairport da SET airport_name = (SELECT airport_name FROM airfares.airport WHERE airfares.airport.code = da.airport_code);

INSERT INTO dimairport (airport_code, airport_name, country)
SELECT code, airport_name, country
FROM airfares.airport
WHERE code NOT IN (SELECT DISTINCT airport_code FROM dimairport)
  AND country IS NOT NULL;