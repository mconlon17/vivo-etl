import csv
import json
from sys import stdin
from sys import stdout

csv_file = stdin
json_file = stdout

reader = csv.DictReader(csv_file, delimiter='\t')
json_data = list()
for row in reader:
    new_row = { k.replace(" ", "_"):v for (k,v) in row.items()}
    json_data.append(new_row)
json_file.write(json.dumps(json_data))