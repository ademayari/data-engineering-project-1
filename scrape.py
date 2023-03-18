import argparse
from datetime import datetime
from date_generator import generate_files, read_files
from scrape.brussels_airlines.brussels_airlines_scrape import *
# from scrape.tui.tui_scrape import *

# Generate files containing dates and destinations
start_date = datetime.now().strftime("%m-%d")
end_date = "10-01"
destinations = ["ALC", "IBZ", "AGP", "PMI", "TCI", "BDS", "NAP", "PMO", "FAO", "HER", "RHO", "CFU"]
airlines = ['brussels-airlines', 'transavia', 'ryanair', 'tui']

generate_files(airlines, start_date, end_date, destinations)
date_dest_list = read_files()

# Parse script arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--airline", type=str)
args = parser.parse_args()
airline = args.airline
valid_airlines = ', '.join(airlines)

if not airline:
    print(f'Missing argument --airline\nValid airlines: {valid_airlines}')
elif airline not in airlines:
    print(f'Error: Airline not recognized\nValid airlines: {valid_airlines}')

if airline == 'brussels-airlines':
    brussels_airlines_scrape(date_dest_list['brussels-airlines'])
elif airline == 'transavia':
    pass
elif airline == 'ryanair':
    pass
elif airline == 'tui':
    pass