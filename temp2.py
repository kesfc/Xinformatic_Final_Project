import csv
import numpy as np
import matplotlib.pyplot as plt


# Loads preprocessed data and results from CSV (includes CO2 emissions in metric tons per person,
# the ratio of renewable to non-renewable energy generated, planar equation coefficients,
# and R squared for each country from 2000-2021)
def print_as_HTML(filename_in):
    data = dict()
    rows = []
    # Get data from CSV
    with open(filename_in, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            rows.append(row)

    # Load data into dictionary based on country code
    for i in range(len(rows)):
        if(i%2==0):
            print("<option value=\"{}\">{}</option>".format(rows[i][1], rows[i][0]))

print_as_HTML("results.csv")
