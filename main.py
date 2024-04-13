import sys
from preprocess import preprocess
from train import train
from display import display

if __name__ == '__main__':
    argc = len(sys.argv)

    if argc < 2:
        print("ERROR: No arguments provided")
        exit(-1)

    mode = sys.argv[1]

    # Preprocess multiple data CSVs into one feature CSV for training
    # Accepts arguments: emissions data CSV filename, populations data CSV filename,
    # energy generation data CSV filename, output CSV filename
    if mode == "preprocess":
        if argc < 6:
            print("ERROR: Insufficient additional arguments for preprocessing (4 required)")
            exit(-1)

        preprocess(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    # Fit multiple linear regression models in 3 dimensions for each country
    # Accepts arguments: preprocessed data CSV filename, output CSV filename
    elif mode == "train":
        if argc < 4:
            print("ERROR: Insufficient additional arguments for training (2 required)")
            exit(-1)

        train(sys.argv[2], sys.argv[3])
    # Display 3-dimensional plot for a given country
    # Accepts arguments: complete data with results CSV filename, country code
    elif mode == "display":
        if argc < 4:
            print("ERROR: Insufficient additional arguments for display (2 required)")
            exit(-1)

        display("display", sys.argv[2], sys.argv[3])
    # Display 3-dimensional plot with a predicted CO2 emission per capita prediction
    # for a given country, year, and renewable vs non-renewable energy generation ratio
    # Accepts arguments: complete data with results CSV filename, country code, year, energy generation ratio
    elif mode == "predict":
        if argc < 6:
            print("ERROR: Insufficient additional arguments for predicting (4 required)")
            exit(-1)

        display("predict", sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
