from api import request_flights
from requests.exceptions import JSONDecodeError
from sys import argv
import json

from temp import temp_results
from config import DEPARTURE

def main():
    with open("../../dates_to_scrape/transavia.json", "r") as dates_file:
        data = json.load(dates_file)
        for city, dates in data.items():
            for date in dates:
                formatted_date = f"2023{date.replace('-','')}"
                try:
                    res = request_flights(DEPARTURE, city, formatted_date)
                    js = res.json()
                    print(js)
                except JSONDecodeError:
                    print(f"no flight/ already past {date}")
                    continue


if __name__ == "__main__":
    if argv[0] is not None and argv[0] == "temp":
        temp_results()
    else:
        main()