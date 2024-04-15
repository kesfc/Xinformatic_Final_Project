import csv
import numpy as np
from sklearn.linear_model import LinearRegression


# Loads preprocessed data from CSV (includes CO2 emissions in metric tons per person and
# the ratio of renewable to non-renewable energy generated for each country from 2000-2021)
def load_data(filename_in):
    data = dict()
    names_ordered = []
    rows = []
    # Get data from CSV
    with open(filename_in, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        fields = next(csv_reader)
        for row in csv_reader:
            rows.append(row)

    # load data into dictionary, saves data order to names_ordered, saves fields and rows for output
    for item in rows:
        name = item[0]
        code = item[1]
        indicator = item[2]
        years = item[3:]

        if name not in data.keys():
            data[name] = dict()

        names_ordered.append(name)
        loc = data[name]
        loc["Country Code"] = code
        loc[indicator] = years

    return names_ordered, data, fields, rows


# Reformats years and energy generation data into one list for model generation
# [[year, energy], ...], returns reformatted list
def reg_reformat(name_data):
    X = []
    years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
             2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    energy = name_data["Renewable vs Non-Renewable Energy Generation"]
    for i in range(len(energy)):
        X.append([years[i], float(energy[i])])

    return X


# Saves preprocessed data along with results to CSV
def save_data(filename_out, fields, rows, models, r_sqs):
    fields.extend(["A", "B", "C", "R_squared"])
    for i in range(len(rows)):
        rows[i].extend([models[i].coef_[0], models[i].coef_[1], models[i].intercept_, r_sqs[i]])

    # Write data to CSV
    with open(filename_out, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


# Trains a multiple linear regression model for each country
def train(filename_in, filename_out):
    names_ordered, data, fields, rows = load_data(filename_in)
    models = []
    r_sqs = []
    print("Calculating multiple linear regression models...")
    for name in names_ordered:
        name_data = data[name]
        X = np.array(reg_reformat(name_data))
        Y = np.array([float(y) for y in name_data["CO2 Emissions Per Capita"]])
        model = LinearRegression().fit(X, Y)
        models.append(model)
        r_sq = model.score(X, Y)
        r_sqs.append(r_sq)
        A, B = model.coef_
        C = model.intercept_
        print(f"\t{name}:\n\t\tEquation: {A}x {'+' if B > 0 else '-'} {B if B > 0 else -1 * B}y "
              f"{'+' if C > 0 else '-'} {C if C > 0 else -1 * C} = z\n\t\tR_sq: {r_sq}")

    save_data(filename_out, fields, rows, models, r_sqs)
