from api import request_flights
from requests.exceptions import JSONDecodeError

from config import DEPARTURE

def main():
    print("START")

def temp_results():
    print("Tijdelijke resultaten:")

    # BRU -> ALC 15/05 -> 20/05
    count = 0
    for date in range(20230515, 20230521):
        try:
            res = request_flights(DEPARTURE, "ALC", str(date))
            j = res.json()
            count += int(j["resultSet"]["count"])
        except JSONDecodeError:
            continue
    print(f"Totaal aantal transavia (BRU->ALC) vluchten van 15/05/2023 tot en met 20/05/2023: {count}")

    # BRU -> FAO average price
    prices = []
    for date in range(20230601, 20230631):
        try:
            res = request_flights(DEPARTURE, "FAO", str(date))
            j = res.json()
            l = [flight["pricingInfoSum"]["totalPriceOnePassenger"] for flight in j["flightOffer"]]
            prices.extend(l)
        except JSONDecodeError:
            continue
    avg = sum(prices)/len(prices)
    print(f"Gemiddelde prijs voor alle transavia vluchten naar Faro in de maand juni: €{avg}")

    # BRU -> IBZ departure time 24/05
    try:
        res = request_flights(DEPARTURE, "IBZ", "20230524")
        j = res.json()
        time = j["flightOffer"][0]["outboundFlight"]["departureDateTime"]
        time = time[time.index("T")+1:]
        print(f"Vertrektijd van BRU -> IBZ op 24 mei: {time}")
    except JSONDecodeError:
        print("no flight found 24/05")
    
    # BRU -> TFS arrival time 29/07
    try:
        res = request_flights(DEPARTURE, "TFS", "20230729")
        j = res.json()
        time = j["flightOffer"][0]["outboundFlight"]["arrivalDateTime"]
        time = time[time.index("T")+1:]
        print(f"Aankomsttijd van BRU -> TFS op 29 juli: {time}")
    except JSONDecodeError:
        print("no flight found 29/07")

    # BRU -> HER
    count = 0
    dates = list(range(20230701,20230732))
    dates.extend(range(20230801, 20230816))
    for date in dates:
        try:
            res = request_flights(DEPARTURE, "HER", str(date))
            j = res.json()
            count += int(j["resultSet"]["count"])
        except JSONDecodeError:
            continue
    print(f"Totaal aantal transavia (BRU->HER)vluchten van 01/07/2023 tot en met 15/08/2023: {count}")


        
if __name__ == "__main__":
    temp_results()