from flask import Flask, render_template, request
import numpy as np
import matplotlib
matplotlib.use('agg')  # Use the 'agg' backend (non-interactive)
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import csv

app = Flask(__name__)

# Loads preprocessed data and results from CSV
def load_data(filename_in):
    data = dict()
    rows = []
    with open(filename_in, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            rows.append(row)

    for i in range(len(rows)):
        name = rows[i][0]
        code = rows[i][1]
        indicator = rows[i][2]
        years = [float(x) for x in rows[i][3:25]]

        if code not in data.keys():
            data[code] = dict()
            data[code]["Name"] = name

        loc = data[code]
        loc[indicator] = years

        if indicator == "CO2 Emissions Per Capita":
            A, B, C, r_sq = rows[i][25:]
            A, B, C, r_sq = float(A), float(B), float(C), float(r_sq)
            loc["A"] = A
            loc["B"] = B
            loc["C"] = C
            loc["Equation"] = (f"{A}x {'+' if B > 0 else '-'} {B if B > 0 else -1 * B}y "
                               f"{'+' if C > 0 else '-'} {C if C > 0 else -1 * C} = z")
            loc["R_sq"] = r_sq
            loc["Years"] = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
                            2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

    return data

# Display function for plotting
def display(code, x1=None, x2=None):
    data = load_data("results.csv")

    if code not in data.keys():
        return "ERROR: Country not found"

    code_data = data[code]
    min_year = 2000
    max_year = 2021
    min_energy = min(code_data["Renewable vs Non-Renewable Energy Generation"])
    max_energy = max(code_data["Renewable vs Non-Renewable Energy Generation"])
    A, B, C = code_data["A"], code_data["B"], code_data["C"]
    prediction = 0.0

    if x1 is not None and x2 is not None:
        x1 = int(x1)
        x2 = float(x2)
        min_year, max_year, min_energy, max_energy = (min(min_year, x1), max(max_year, x1),
                                                      min(min_energy, x2), max(max_energy, x2))
        prediction = A * x1 + B * x2 + C
        prediction_text = f"Prediction for {x1} with an energy generation ratio of {x2}: {prediction}"
    else:
        prediction_text = ""

    X1, X2 = np.meshgrid(np.linspace(min_year, max_year, 100), np.linspace(min_energy, max_energy, 100))
    Y = A * X1 + B * X2 + C
    points_X1 = np.array(code_data["Years"])
    points_X2 = np.array(code_data["Renewable vs Non-Renewable Energy Generation"])
    points_Y = np.array(code_data["CO2 Emissions Per Capita"])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X1, X2, Y)
    ax.scatter(points_X1, points_X2, points_Y, color='blue')
    ax.set_title(f"Multiple Regression Model for {code}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Energy Generation Ratio (r vs non-r)")
    ax.set_zlabel("CO2 Emissions (metric tons / person)")
    text = f"Equation: {code_data['Equation']}, R^2: {code_data['R_sq']}\n{prediction_text}"
    plt.figtext(0.5, 0.01, text, wrap=True, horizontalalignment='center', fontsize=12)

    if x1 is not None and x2 is not None:
        pred_point = np.array([x1, x2, prediction])
        ax.scatter(pred_point[0], pred_point[1], pred_point[2], color='red')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)  # Close the figure to avoid resource leaks

    return plot_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    code = request.form['code']
    x1 = request.form['x1']
    x2 = request.form['x2']
    plot_data = display(code, x1, x2)
    return render_template('plot.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True)
