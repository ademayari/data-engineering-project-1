import pandas as pd
import os

path = os.path.join(os.path.dirname(__file__), '../../csv/brussels_airlines.csv')
# df = pd.read_csv(path, sep=':')

# print(df)

# test = (
# df.groupby('country')['price'].mean()
#   .rename(columns={"Result": "Average"})
#   .reset_index()
#   .to_csv("agg.csv", index=False)
# )

# print(test)

file1 = open(path, 'r')
lines = file1.readlines()

sum = 0
for line in lines:
  sum += float(line.rstrip().replace(',', '.'))
  
print(sum/len(lines))