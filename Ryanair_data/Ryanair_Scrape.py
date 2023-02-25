import requests
from bs4 import BeautifulSoup
import json




# backup_one_way = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&promoCode=&IncludeConnectingFlights=false&FlexDaysBeforeOut=2&FlexDaysOut=2&FlexDaysBeforeIn=2&FlexDaysIn=2&RoundTrip=false&ToUs=AGREED"

# alternative_one_way = "https://services-api.ryanair.com/farfnd/3/oneWayFares?&departureAirportIataCode=BCN&language=en&limit=16&market=en-gb&offset=0&outboundDepartureDateFrom=2023-02-28&outboundDepartureDateTo=2023-03-20&priceValueTo=150"

# URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&promoCode=&IncludeConnectingFlights=false&FlexDaysBeforeOut=2&FlexDaysOut=2&FlexDaysBeforeIn=2&FlexDaysIn=2&RoundTrip=true&ToUs=AGREED"

ONE_WAY_URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&IncludeConnectingFlights=true&RoundTrip=false&ToUs=AGREED"



spanje = ["ALC", "IBZ", "AGP", "PMI", "TCI", "TVI"]
italie = ["BDS", "NAP", "PMO"]
portugal = ["FAO"]
griekenland = ["HER", "RHO","CFU"]
luchthaven = ["BRU", "CRL"]

# change desitination code in URL
# def change_destination_code(destination_code):
#     global ONE_WAY_URL
#     ONE_WAY_URL = ONE_WAY_URL.replace("AGP", destination_code)
    




page = requests.get(ONE_WAY_URL)

soup = BeautifulSoup(page.content, "lxml")
print(soup)
result = soup.find("p").text
print(type(result))

#convert string to  object
json_object = json.loads(result)

#check new data type
#print(type(json_object))

#output
#<class 'dict'>


