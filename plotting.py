import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from display import load_data
from bokeh.embed import components
from bokeh.plotting import figure

# Displays 3-dimensional plot of data points and corresponding planar model for a given country code
# (to avoid spaces in command line arguments)
# Additionally calculates and displays predicted CO2 emission prediction for a given year
# and energy generation ratio if mode is set to 'predict'
def planar_model_3d(code, x1=None, x2=None):
    data = load_data("data/results.csv")

    if code not in data.keys():
        return "ERROR: Country not found"

    # Initialize plot variables
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

    # Initialize plot variables
    X1, X2 = np.meshgrid(np.linspace(min_year, max_year, 100), np.linspace(min_energy, max_energy, 100))
    Y = A * X1 + B * X2 + C
    points_X1 = np.array(code_data["Years"])
    points_X2 = np.array(code_data["Renewable vs Non-Renewable Energy Generation"])
    points_Y = np.array(code_data["CO2 Emissions Per Capita"])

    # Create plot
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

    # Add prediction point onto plot
    if x1 is not None and x2 is not None:
        pred_point = np.array([x1, x2, prediction])
        ax.scatter(pred_point[0], pred_point[1], pred_point[2], color='red')

    # Generate png image of plot
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)  # Close the figure to avoid resource leaks

    return plot_data

# Generate 2d graph displaying year vs emission with prediction for a given renewable ratio
def prediction_plot(code, x1=None, x2=None):
    data = load_data("data/results.csv")

    # Initialize plot variables
    code_data = data[code]
    min_year = 2000
    max_year = 2021
    min_energy = min(code_data["Renewable vs Non-Renewable Energy Generation"])
    max_energy = max(code_data["Renewable vs Non-Renewable Energy Generation"])
    A, B, C = code_data["A"], code_data["B"], code_data["C"]
    prediction = 0.0

    # create the plot figure
    p = figure(height=350, sizing_mode="stretch_width")
    p.circle(
        code_data["Years"],
        code_data["CO2 Emissions Per Capita"],
        size=20,
        color="navy",
        alpha=0.5
    )
    script, div = components(p)

    # return chart components
    return f'''
    <html lang="en">
        <head>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-3.0.1.min.js"></script>
            <title>Bokeh Charts</title>
        </head>
        <body>
            <h1>Add Graphs to Flask apps using Python library - Bokeh</h1>
            { div }
            { script }
        </body>
    </html>
    '''

if __name__=="__main__":
    script, div = prediction_plot("AFG", x1="2025", x2="0.75")
    