#This is a test python script
import csv
import os

filename = "tract_data.csv"

with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        print(f'\t{row[0]} -- {row[1]}.')
