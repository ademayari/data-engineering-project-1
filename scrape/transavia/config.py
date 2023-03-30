
URL = "https://www.transavia.com/nl-BE/boek-een-vlucht/uitgebreid-zoeken/zoeken/"
API_URL = "https://api.transavia.com/v1/flightoffers/"
API_KEY = "17c5625ff4424000b95a0ae6f3a23586"

JSON_HEADER = ';'.join([
    "flight_id",
    "from_airport",
    "to_airport",
    "departure_date_time",
    "arrival_date_time",
    "marketing_airline_name",
    "flight_number",
    "price",
    "link"
])

DEPARTURE = "BRU"

DEPARTURE_INPUT_ID = "countryStationSelection_Origin-input"
DESTINATION_INPUT_ID = "countryStationSelection_Destination-input"

DIMENSIONS = [
    (1920, 1080),
    (1366, 768),
    (1536, 864)
]

TOGGLE_IDS = [
    "AS-search-panel-budget-section",
    "AS-search-panel-budget-section_next-section",
    "AS-search-panel-when-section_next-section"
]