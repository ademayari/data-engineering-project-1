import os
import json
from datetime import datetime, timedelta

def generate_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%m-%d")
    end = datetime.strptime(end_date, "%m-%d")
    date_list = []

    while start <= end:
        date_list.append(start.strftime("%m-%d"))
        start += timedelta(days=1)

    return date_list

def generate_files(airlines, start_date, end_date, destinations, output_dir="dates_to_scrape"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    date_list = generate_dates(start_date, end_date)

    for airline in airlines:
        date_dest_dict = {dest: date_list for dest in destinations}
        with open(f"{output_dir}/{airline}.json", "w") as outfile:
            json.dump(date_dest_dict, outfile)

def read_files(input_dir="dates_to_scrape"):
    airline_date_dest_list = {}

    for file in os.listdir(input_dir):
        if file.endswith(".json"):
            airline = file[:-5]  # Remove '.json' from the filename to get the airline name
            with open(f"{input_dir}/{file}", "r") as infile:
                data = json.load(infile)
                airline_date_dest_list[airline] = data

    return airline_date_dest_list

def update_airline_dates(airline, updated_date_dest_list, output_dir="dates_to_scrape"):
    with open(f"{output_dir}/{airline}.json", "w") as outfile:
        json.dump(updated_date_dest_list, outfile)
