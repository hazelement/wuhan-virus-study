import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def read_file(filename):
    df = pd.read_csv(filename)
    return df.iloc[:, 1].astype(float).copy().values, df.iloc[:, 0].astype(str).copy().values


def run_model(file_name, model, expression):
    y, da = read_file(file_name)
    x = np.arange(0, len(y), 1)

    coeff, cov = curve_fit(model, x, y)
    formula = expression(*coeff)
    print(formula)

    x_1 = np.arange(0, len(x) * 1.2, 1)
    y_1 = [model(t, *coeff) for t in x_1]

    # plot existing
    plt.scatter(x, y)
    plt.annotate(f"{da[-1]}: {int(y[-1])}", xy=(x[-1], y[-1]),
                 xytext=(x[-1]/2, y[-1]), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8))

    # plot fitted curve
    plt.plot(x_1, y_1, color="red")
    plt.text(1, y[-1]/9, formula, fontsize=12)


    # plot prediction
    predicted_x = x_1[len(x):][0:2]
    predicted_y = y_1[len(x):][0:2]
    plt.scatter(predicted_x, predicted_y)
    for index, (x, y) in enumerate(zip(predicted_x, predicted_y)):
        plt.annotate(str(int(y)), (x, y))

    plt.title(file_name)
    plt.savefig(file_name.split(".")[0] + ".png")


if __name__ == '__main__':
    file_name = "wuhan.csv"
    from models import si_model as model
    from models import si_model_expression as expression

    coeff = run_model(file_name, model, expression)
