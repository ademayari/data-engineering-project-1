import argparse

from scrape.brussels_airlines.brussels_airlines_scrape import *

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--airline", type=str)
args = parser.parse_args()
airline = args.airline

if not airline:
  print('Missing argument --airline')
  print('Valid airlines: brussels-airlines, transavia, ryanair, tui')
elif airline not in ['brussels-airlines', 'transavia', 'ryanair', 'tui']:
  print('Error: Airline not recognized')
  print('Valid airlines: brussels-airlines, transavia, ryanair, tui')

if (airline == 'brussels-airlines'):
  brussels_airlines_scrape(5, 13, 0, ["ES:TCI:TFS"])
if (airline == 'transavia'):
  pass
if (airline == 'ryanair'):
  pass
if (airline == 'tui'):
  pass