from api import request_flights
from requests.exceptions import JSONDecodeError
from requests import Response
from sys import argv
import json
from datetime import date as Date

from temp import temp_results
from config import DEPARTURE, JSON_HEADER
from utils import json_to_csv

def transavia_scrape(transavia_dates):
    with open(transavia_dates, "r") as dates_file:
        with open(f"./transavia_data{Date.today()}.csv", "w") as outfile:
            data = json.load(dates_file)
            outfile.writelines([JSON_HEADER + "\n"])
            for city, dates in data.items():
                for date in dates:
                    formatted_date = f"2023{date.replace('-','')}"
                    try:
                        res: Response = request_flights(DEPARTURE, city, formatted_date)
                        if res.status_code != 200:
                            print(f"api not responding with 200 on {formatted_date}")
                            continue
                        js = res.json()
                        outfile.write(json_to_csv(js))
                        outfile.write("\n")
                    except JSONDecodeError:
                        print(f"no flight/ already past {date}")
                        continue
                    except KeyError as e:
                        print(f"keyerror: {e.with_traceback}")
                        print(f"obj = {res.json()}")


if __name__ == "__main__":
    if argv[0] is not None and argv[0] == "temp":
        temp_results()
    else:
        transavia_scrape()