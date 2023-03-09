from utils.selenium_helpers import driver
from enum import Enum

class dotdict(dict):
  """dot.notation access to dictionary attributes"""
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__

TITLES = dotdict({
  'ADVANCED_SEARCH': 'Brussels Airlines - Uitgebreide zoekopdracht',
  'RATE_LIMIT': 'Challenge Validation'
})

extra_options_button = "// span[contains(text(),\'Meer reisgegevens')]"
single_flight_button = "// span[contains(text(),\'Enkele reis')]"

PORTAL = dotdict({
  'confirm_button': "// button[contains(text(),\'Akkoord')]",
  'nav_flights_button': "// a[contains(text(),\' Vluchten vinden ')]"
})

EXTRACT_FLIGHTS = dotdict({
  'flight_unavailable': "// span[contains(text(),\' niet beschikbaar ')]",
  'flight_time_class': "time",
  'flight_price_class': "cabinPrice",
  'num_stops_class': "[class='nbStops ng-star-inserted']",
  'by_brussels_airlines': "// div[contains(text(),\'Brussels Airlines')]"
})

def SET_DESTINATION(country, city, airport):
  input_button = "[name='MODIFY_SEARCH_ARRIVAL_LOCATION_1']"
  if driver.title == TITLES.ADVANCED_SEARCH:
    input_button = "[name='ADVANCED_SEARCH_FLIGHTS_ARRIVAL_LOCATION_1']"
    
  return dotdict({
    'input_button': input_button,
    'country_button': f"[id='apd-Country-{country}']",
    'city_button': f"[id='apd-City-{city}']",
    'airport_button': f"[id='apd-Airport-{airport}']",
    'confirm_button': "[class='confirmButton']"
  })

def SET_DATE(month, day):
  if driver.title == TITLES.ADVANCED_SEARCH:
    return dotdict({
      'input_elem': "[id='dp-input-0-outbound']",
      'reset_button': "[class='resetButton']",
      'close_button': "[class='datepickerCloseButton']",
      'next_month_button': "[class='icon-link-navigation-next iconLinkNavigationNext']",
      'month_header': f"// span[contains(text(),'{month} 2023')]",
      'day_button': f"// span[contains(text(),'{day}')]"
    })
  
  return dotdict({
    'input_elem': "[formcontrolname='departureDate1']",
    'reset_button': "[class='resetButton']",
    'close_button': "[class='closeBtn ng-star-inserted']",
    'next_month_button': "[aria-label='Volgende maand']",
    'month_header': f"// h5[contains(text(),'{month} 2023')]",
    'day_button': f"// div[contains(text(),'{day}')]"
  })

def SEARCH_BUTTON():
  if driver.title == TITLES.ADVANCED_SEARCH:
    return "// span[contains(text(),\'Vluchten zoeken')]"
  
  return "// span[contains(text(),\'Start nieuwe zoekopdracht')]"