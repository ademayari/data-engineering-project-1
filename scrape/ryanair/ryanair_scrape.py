import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import csv


ONE_WAY_URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&IncludeConnectingFlights=true&RoundTrip=false&ToUs=AGREED"



spanje = ["ALC", "IBZ", "AGP", "PMI", "TFS"]
italie = ["BDS", "NAP", "PMO"]
portugal = ["FAO"]
griekenland = ["HER", "RHO","CFU"]
luchthaven = ["BRU", "CRL"]

list_of_destinations = spanje + italie + portugal + griekenland 


# store only the current date in variable datenow
datenow = datetime.now().strftime("%Y-%m-%d")


print("#################################### VANUIT BRUSSEL ####################################")


# change desitination code in URL 
for i in list_of_destinations:
    

    NEW_ONE_WAY_URL = ONE_WAY_URL.replace("AGP", i)
    NEW_ONE_WAY_URL = NEW_ONE_WAY_URL.replace("2023-03-02", "2023-03-21")
    page = requests.get(NEW_ONE_WAY_URL)
    soup = BeautifulSoup(page.content, "lxml")
    result = soup.find("p").text

    # convert string to  object
    json_object = json.loads(result)
    
    # get columns originName, destinationName, dateOut, value, flightDuration, faresLeft and flightKey from the json object and add them to ryanair.csv
    if json_object["trips"][0]["dates"][0]["flights"] != []:
        originName = json_object["trips"][0]["originName"]
        destinationName = json_object["trips"][0]["destinationName"]
        dateOut = json_object["trips"][0]["dates"][0]["dateOut"]
        value = json_object["trips"][0]["dates"][0]["flights"][0]["regularFare"]["fares"][0]["amount"]
        flightDuration = json_object["trips"][0]["dates"][0]["flights"][0]["segments"][0]["duration"]
        faresLeft = json_object["trips"][0]["dates"][0]["flights"][0]["faresLeft"]
        flightKey = json_object["trips"][0]["dates"][0]["flights"][0]["flightKey"]

        # use a csv writer to write the data to a csv file

        with open('ryanair.csv', "a", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # add empty row 
            csv_writer.writerow([])
            csv_writer.writerow([originName, destinationName, dateOut, value, flightDuration, faresLeft, flightKey])      
    

print("#################################### VANUIT CHARLEROI ####################################")

# change the destination code in the URL and the origin code in the URL
for i in list_of_destinations:
        
    NEW_ONE_WAY_URL = ONE_WAY_URL.replace("AGP", i)
    NEW_ONE_WAY_URL = NEW_ONE_WAY_URL.replace("BRU", "CRL")
    NEW_ONE_WAY_URL = NEW_ONE_WAY_URL.replace("2023-03-02", "2023-03-21")
    page = requests.get(NEW_ONE_WAY_URL)
    soup = BeautifulSoup(page.content, "lxml")
    result = soup.find("p").text

    # convert string to  object
    json_object = json.loads(result)
    if json_object["trips"][0]["dates"][0]["flights"] != []:
        originName = json_object["trips"][0]["originName"]
        destinationName = json_object["trips"][0]["destinationName"]
        dateOut = json_object["trips"][0]["dates"][0]["dateOut"]
        value = json_object["trips"][0]["dates"][0]["flights"][0]["regularFare"]["fares"][0]["amount"]
        flightDuration = json_object["trips"][0]["dates"][0]["flights"][0]["segments"][0]["duration"]
        faresLeft = json_object["trips"][0]["dates"][0]["flights"][0]["faresLeft"]
        flightKey = json_object["trips"][0]["dates"][0]["flights"][0]["flightKey"]


        with open('ryanair.csv', "a", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # add empty row 
            csv_writer.writerow([])
            csv_writer.writerow([originName, destinationName, dateOut, value, flightDuration, faresLeft, flightKey])    