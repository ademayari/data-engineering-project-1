import pandas as pd

# Load the CSV file into a pandas dataframe
df = pd.read_csv('PATH_TO_FILE.csv')

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Save the cleaned dataframe to a new CSV file
df.to_csv('cleaned_file.csv', index=False)
