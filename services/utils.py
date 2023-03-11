import csv
import os

class dotdict(dict):
  """dot.notation access to dictionary attributes"""
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__
  
def write_csv_line(file_name, data):
  path = os.path.join(os.path.dirname(__file__), '../csv/' + file_name)
  
  with open(path, "a", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter =';')
    writer.writerow(list(data.values()))
