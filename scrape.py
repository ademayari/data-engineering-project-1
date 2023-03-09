import argparse

from scrape.brussels_airlines.brussels_airlines_scrape import *

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--airline", type=str)
args = parser.parse_args()
airline = args.airline

if (airline == 'brussels-airlines'):
  brussels_airlines_scrape()
if (airline == 'transavia'):
  pass
if (airline == 'ryanair'):
  pass
if (airline == 'tui'):
  pass
else:
  print('Missing argument --airline')
  print('Valid airlines: brussels-airlines, transavia, ryanair, tui')