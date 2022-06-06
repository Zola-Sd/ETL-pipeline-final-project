import csv
from pathlib import Path


def fetch_filepath(filename):
    return Path(__file__).parent/filename

def extract_data():
    with open(fetch_filepath('test.csv'), 'r') as f:
        contents = csv.DictReader(f)

        sales_data = [row for row in contents]
    
    return sales_data

print(extract_data())
