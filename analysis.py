import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


class AnalysisModel(object):

    def __init__(self, model, expression):
        self.model = model
        self.expression = expression
        self.fitted_formula = None
        self.coeff = None
        self.cov = None

    def fit(self, x, y):
        coeff, cov = curve_fit(self.model, x, y)
        self.fitted_formula = expression(*coeff)
        self.coeff = coeff
        self.cov = cov

    def calculate(self, x):
        return [self.model(t, *self.coeff) for t in x]


class FileData(object):

    def __init__(self, file_name):
        self.y, self.date_point = read_file(file_name)
        self.x = np.arange(0, len(self.y), 1)
        self.filename = file_name


def read_file(filename):
    df = pd.read_csv(filename)
    return df.iloc[:, 1].astype(float).copy().values, df.iloc[:, 0].astype(str).copy().values


def plot_result(file_name, analysis_model, file_data):
    """
    Plot existing data and fitted curve, save image to same directory as file_name
    :return:
    """
    x = file_data.x
    y = file_data.y
    date_point = file_data.date_point

    x_1 = np.arange(0, len(x) * 1.2, 1)
    y_1 = analysis_model.calculate(x_1)

    # plot existing
    plt.scatter(x, y)
    plt.annotate(f"{date_point[-1]}: {int(y[-1])}", xy=(x[-1], y[-1]),
                 xytext=(x[-1] / 2, y[-1]), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8))

    # plot fitted curve
    plt.plot(x_1, y_1, color="red")
    plt.text(1, y[-1] / 9, analysis_model.fitted_formula, fontsize=12)

    # plot prediction
    predicted_x = x_1[len(x):][0:2]
    predicted_y = y_1[len(x):][0:2]
    plt.scatter(predicted_x, predicted_y)
    for index, (x, y) in enumerate(zip(predicted_x, predicted_y)):
        plt.annotate(str(int(y)), (x, y))

    plt.title(file_name)
    plt.savefig(file_name.split(".")[0] + ".png")
    plt.show()


def run_model(file_name, analysis_model):
    file_data = FileData(file_name)
    analysis_model.fit(file_data.x, file_data.y)
    print(analysis_model.fitted_formula)
    plot_result(file_name, analysis_model, file_data)


if __name__ == '__main__':
    city_name = "canada"
    file_name = f"data/{city_name}.csv"
    from models import si_model as model
    from models import si_model_expression as expression

    analysis_model = AnalysisModel(model, expression)

    coeff = run_model(file_name, analysis_model)
