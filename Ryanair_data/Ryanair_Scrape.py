import requests
from bs4 import BeautifulSoup
import json




# backup_one_way = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&promoCode=&IncludeConnectingFlights=false&FlexDaysBeforeOut=2&FlexDaysOut=2&FlexDaysBeforeIn=2&FlexDaysIn=2&RoundTrip=false&ToUs=AGREED"

# alternative_one_way = "https://services-api.ryanair.com/farfnd/3/oneWayFares?&departureAirportIataCode=BCN&language=en&limit=16&market=en-gb&offset=0&outboundDepartureDateFrom=2023-02-28&outboundDepartureDateTo=2023-03-20&priceValueTo=150"

# URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&promoCode=&IncludeConnectingFlights=false&FlexDaysBeforeOut=2&FlexDaysOut=2&FlexDaysBeforeIn=2&FlexDaysIn=2&RoundTrip=true&ToUs=AGREED"

ONE_WAY_URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&IncludeConnectingFlights=true&RoundTrip=false&ToUs=AGREED"



spanje = ["ALC", "IBZ", "AGP", "PMI"]
italie = ["BDS", "NAP", "PMO"]
portugal = ["FAO"]
griekenland = ["HER", "RHO","CFU"]
luchthaven = ["BRU", "CRL"]

list_of_destinations = spanje + italie + portugal + griekenland 


number = 0


# change desitination code in URL 
for i in list_of_destinations:
    number += 1

    NEW_ONE_WAY_URL = ONE_WAY_URL.replace("AGP", i)
    # print new empty line
    #print("--------------------------------------------------------------")
    #print(NEW_ONE_WAY_URL, number)
    page = requests.get(NEW_ONE_WAY_URL)
    soup = BeautifulSoup(page.content, "lxml")
    #print(soup)
    result = soup.find("p").text
    #print(type(result))
    #convert string to  object
    json_object = json.loads(result)
    #print(json_object)
    # get columns originName, destinationName, dateOut, amount from the json object by using the json object 
    print("Destination: ", json_object["trips"][0]["destinationName"])
    print("Date Out: ",  json_object["trips"][0]["dates"][0]["dateOut"])

    #if there is no flight available, the json object will not have the key "flights"
    # check if the key "flights" is in the json object and check if the list is not empty


    if json_object["trips"][0]["dates"][0]["flights"] != []:
        print("Flight: ",  json_object["trips"][0]["dates"][0]["flights"][0]["flightNumber"])
        print("Value: ",  json_object["trips"][0]["dates"][0]["flights"][0]["regularFare"]["fares"][0]["amount"])
    else:
        print("No flight available")

    #print("Value: ",  json_object["trips"][0]["dates"][0]["flights"][0]["regularFare"]["fares"][0]["amount"])




# page = requests.get(ONE_WAY_URL)

# soup = BeautifulSoup(page.content, "lxml")
# print(soup)
# result = soup.find("p").text
# print(type(result))

# #convert string to  object
# json_object = json.loads(result)

#check new data type
#print(type(json_object))

#output
# get the price of the flight from the soup object as well as destination and date and time 
# print(json_object["outbound"]["fares"][0]["price"]["value"])


# get originName, destinationName, dateOut, amount from the json object 
