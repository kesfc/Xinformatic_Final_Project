from flask import Flask, render_template, request
import matplotlib
matplotlib.use('agg')  # Use the 'agg' backend (non-interactive)
from plotting import prediction_plot, planar_model_3d
from display import load_data
import csv
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    code = request.form['code']
    x1 = request.form['x1']
    x2 = request.form['x2']
    plot_data1 = planar_model_3d(code, x1, x2)
    return render_template('plot.html', plot_data1=plot_data1)

@app.route('/results.html')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
