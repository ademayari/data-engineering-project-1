import requests

from config import API_URL, API_KEY

querystring = {"origin":"BRU","destination":"IBZ","originDepartureDate":"20230515"}


def headers():
    return {
        "apikey": API_KEY
    }

def request_flights(origin, destination, date):
    params = {
        "origin": origin,
        "destination": destination,
        "originDepartureDate": date
    }
    req_headers = headers()

    response = requests.get(url=API_URL, headers=req_headers, params=params)
    return response




