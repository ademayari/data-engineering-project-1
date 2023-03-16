from services.selenium_helpers import driver
from enum import Enum
from services.utils import dotdict

TITLES = dotdict({
  'ADVANCED_SEARCH': 'Brussels Airlines - Uitgebreide zoekopdracht',
  'RATE_LIMIT': 'Challenge Validation'
})

extra_options_button = "// span[contains(text(),\'Meer reisgegevens')]"
single_flight_button = "// span[contains(text(),\'Enkele reis')]"

PORTAL = dotdict({
  'confirm_button': "// button[contains(text(),\'Akkoord')]",
})

EXTRACT_FLIGHTS = dotdict({
  'flight_tag': "cont-avail",
  'flight_unavailable': "// span[contains(text(),\' niet beschikbaar ')]",
  'flight_time_class': "time",
  'flight_price_class': "cabinPrice",
  'flight_stops_class': "segments",
  'seats_available_class': 'seats',
  'by_brussels_airlines': "// div[contains(text(),\'Brussels Airlines')]",
  'flight_number_class': 'flightNumber'
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
      'day_button': f"// span[contains(text(),'{day}')]",
    })
  
  return dotdict({
    'input_elem': "[formcontrolname='departureDate1']",
    'reset_button': "[class='resetButton']",
    'close_button': "[class='closeBtn ng-star-inserted']",
    'next_month_button': "[aria-label='Volgende maand']",
    'day_button': f"// div[contains(text(),'{day}')]",
  })

def SEARCH_BUTTON():
  if driver.title == TITLES.ADVANCED_SEARCH:
    return "// span[contains(text(),\'Vluchten zoeken')]"
  
  return "// span[contains(text(),\'Start nieuwe zoekopdracht')]"