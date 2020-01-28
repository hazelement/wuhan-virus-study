import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def read_file(filename):
    df = pd.read_csv(filename)
    return df.iloc[:, 1].astype(float).copy()


def run_model(file_name, model):
    y = read_file(file_name)
    x = np.arange(0, len(y), 1)

    coeff, cov = curve_fit(model, x, y)

    print(cov)

    x_1 = np.arange(0, len(x) * 1.2, 1)
    y_1 = [model(t, *coeff) for t in x_1]

    plt.scatter(x, y)
    plt.plot(x_1, y_1, color="red")
    plt.title(file_name)
    plt.savefig(file_name.split(".")[0] + ".png")


if __name__ == '__main__':
    file_name = "sars.csv"
    from models import si_model as model

    run_model(file_name, model)
