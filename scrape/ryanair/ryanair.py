import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import csv
import time
from termcolor import colored


ONE_WAY_URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn=2023-03-14&DateOut=2023-03-02&Destination=AGP&Disc=0&INF=0&Origin=BRU&TEEN=0&IncludeConnectingFlights=true&RoundTrip=false&ToUs=AGREED"
luchthaven = ["BRU", "CRL"]
datenow = datetime.now().strftime("%Y-%m-%d")

def ryanair_scrape(date):

#    session = requests.Session()
#    session.headers['User-Agent'] = USER_AGENT
    
    for destination, dates in date.items():
        for i in dates:
            print("SCRAPING DESTINATION " + colored(destination, 'green') + " FOR DATE " + colored(i, 'green'))
            for j in luchthaven:
                
                NEW_ONE_WAY_URL = ONE_WAY_URL.replace("AGP", destination)
                NEW_ONE_WAY_URL = NEW_ONE_WAY_URL.replace("03-02", str(i))
                for l in range(3):
                    try:
                        page = requests.get(NEW_ONE_WAY_URL)
                        
                        soup = BeautifulSoup(page.content, "lxml")
                        result = soup.find("p").text
                        json_object = json.loads(result)
                        break
                    except requests.exceptions.RequestException as e:
                        print(f"Error connecting to {NEW_ONE_WAY_URL}: {e}")

                        if l == 2:
                            print(f"Could not connect to {NEW_ONE_WAY_URL} after 3 attempts. Skipping.") 
                try:
                    aantal_vluchten = len(json_object["trips"][0]["dates"][0]["flights"])
                except KeyError:
                    aantal_vluchten = 0
                
                # get columns originName, destinationName, dateOut, value, flightDuration, faresLeft and flightKey from the json object and add them to ryanair.csv
                print("NUM FLIGHTS: " + aantal_vluchten)
                if aantal_vluchten != 0:
                    if json_object["trips"][0]["dates"][0]["flights"] != []:

                        for j in range(aantal_vluchten):
                            originName = json_object["trips"][0]["originName"]
                            destinationName = json_object["trips"][0]["destinationName"]
                            dateOut = json_object["trips"][0]["dates"][0]["dateOut"]
                            try:
                                prijs = json_object["trips"][0]["dates"][0]["flights"][j]["regularFare"]["fares"][0]["amount"]
                            except KeyError:
                                prijs = "None"
                            try:
                                timeOut = json_object["trips"][0]["dates"][0]["flights"][j]["segments"][0]["time"][0]
                            except KeyError:
                                timeOut = "None"
                            try:
                                timeArrival = json_object["trips"][0]["dates"][0]["flights"][j]["segments"][0]["time"][1]
                            except KeyError:
                                timeArrival = "None"
                            try:    
                                flightDuration = json_object["trips"][0]["dates"][0]["flights"][j]["segments"][0]["duration"]
                            except KeyError:
                                flightDuration = "None"
                            try:    
                                plaatsenOver = json_object["trips"][0]["dates"][0]["flights"][j]["faresLeft"]
                            except KeyError:
                                plaatsenOver = "None"
                            try:    
                                flightKey = json_object["trips"][0]["dates"][0]["flights"][j]["flightKey"]
                            except KeyError:
                                flightKey = "None"
                            try:
                                flightNumber = json_object['trips'][0]['dates'][0]['flights'][j]['flightNumber']
                            except KeyError:
                                flightNumber = "None"


                            with open('ryanair.csv', "a", newline='') as csv_file:
                                csv_writer = csv.writer(csv_file)
                                csv_writer.writerow([originName, destinationName, dateOut, prijs, flightDuration, plaatsenOver, flightKey, flightNumber, timeOut, timeArrival])      


#ryanair_scrape(date)