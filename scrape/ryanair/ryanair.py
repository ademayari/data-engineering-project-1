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


# huidige datum
datenow = datetime.now().strftime("%Y-%m-%d")



def ryanair_scrape(date):
    for i in list_of_destinations:
        for j in luchthaven:
            
            NEW_ONE_WAY_URL = ONE_WAY_URL.replace("AGP", i)
            NEW_ONE_WAY_URL = NEW_ONE_WAY_URL.replace("2023-03-02", date)
            page = requests.get(NEW_ONE_WAY_URL)
            soup = BeautifulSoup(page.content, "lxml")
            result = soup.find("p").text
            json_object = json.loads(result)
            aantal_vluchten = len(json_object["trips"][0]["dates"][0]["flights"])
            
            # get columns originName, destinationName, dateOut, value, flightDuration, faresLeft and flightKey from the json object and add them to ryanair.csv
            if json_object["trips"][0]["dates"][0]["flights"] != []:

                for j in range(aantal_vluchten):
                    originName = json_object["trips"][0]["originName"]
                    destinationName = json_object["trips"][0]["destinationName"]
                    dateOut = json_object["trips"][0]["dates"][0]["dateOut"]
                    prijs = json_object["trips"][0]["dates"][0]["flights"][j]["regularFare"]["fares"][0]["amount"]
                    timeOut = json_object["trips"][0]["dates"][0]["flights"][j]["segments"][0]["time"][0]
                    timeArrival = json_object["trips"][0]["dates"][0]["flights"][j]["segments"][0]["time"][1]
                    flightDuration = json_object["trips"][0]["dates"][0]["flights"][j]["segments"][0]["duration"]
                    plaatsenOver = json_object["trips"][0]["dates"][0]["flights"][j]["faresLeft"]
                    flightKey = json_object["trips"][0]["dates"][0]["flights"][j]["flightKey"]
                    flightNumber = json_object['trips'][0]['dates'][0]['flights'][j]['flightNumber']


                    with open('ryanair.csv', "a", newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([])
                        csv_writer.writerow([originName, destinationName, dateOut, prijs, flightDuration, plaatsenOver, flightKey, flightNumber, timeOut, timeArrival])      

