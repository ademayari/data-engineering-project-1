import pandas as pd
import os

CSV_PATH = '../clean_data_all'

def load_all_csv():
    all_files = os.listdir(CSV_PATH)
    csv_files = [file for file in all_files if file.endswith('.csv')]
    
    dataframes = []
    column_names = ['flight_id', 'flightnumber', 'departure_date', 'arrival_date', 'departure_time',
                    'arrival_time', 'duration', 'number_of_stops', 'airline_iata_code',
                    'departure_airport_iata_code', 'arrival_airport_iata_code', 'scrape_date',
                    'available_seats', 'price']
    
    for file in csv_files:
        file_path = os.path.join(CSV_PATH, file)
        dataframes.append(pd.read_csv(file_path, header=None, names=column_names))
    
    concatenated_dataframe = pd.concat(dataframes, ignore_index=True)
    
    return concatenated_dataframe.drop_duplicates()
