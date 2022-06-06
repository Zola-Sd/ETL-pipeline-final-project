import csv

def extract_data():
    with open('test.csv', 'r') as f:
        contents = csv.DictReader(f)

        sales_data = [row for row in contents]
    
    return sales_data

sales_data = extract_data()
