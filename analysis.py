from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from models import si_model as si_model
from models import si_model_expression as si_expression
from data import CountryData, FileData, AbstractData


# todo add states comparision in US
# todo add province comparision in Canada

class StatisticModel(object):

    def __init__(self, model, expression):
        self.model = model
        self.expression = expression
        self.fitted_formula = None
        self.coeff = None
        self.cov = None
        self.fitted = False

    def fit(self, x, y):
        try:
            coeff, cov = curve_fit(self.model, x, y)
            self.fitted_formula = si_expression(*coeff)
            self.coeff = coeff
            self.cov = cov
            self.fitted = True
        except RuntimeError as e:
            print(e)

    def calculate(self, x):
        return [self.model(t, *self.coeff) for t in x]


class PlotData(object):

    def __init__(self,
                 existing_x,
                 existing_y,
                 existing_date_point,
                 curve_x,
                 curve_y,
                 ):
        self.existing_x = existing_x
        self.existing_y = existing_y
        self.existing_date_point = existing_date_point
        self.curve_x = curve_x
        self.curve_y = curve_y


class DataModel(object):

    def __init__(self, target_data: AbstractData, statistics_model: StatisticModel):
        self.target_data = target_data
        self.statistic_model = statistics_model
        self.statistic_model.fit(self.target_data.x, self.target_data.y)

    def get_plot_data(self):
        x = self.target_data.x
        y = self.target_data.y
        date_point = self.target_data.date_point

        if self.statistic_model.fitted:
            x_1 = np.arange(0, len(x) * 1.2, 1)
            y_1 = self.statistic_model.calculate(x_1)
        else:
            print("Statistical model not fitted")
            x_1 = None
            y_1 = None

        return PlotData(existing_x=x,
                        existing_y=y,
                        existing_date_point=date_point,
                        curve_x=x_1,
                        curve_y=y_1)

    def plot_historical(self):
        # plot fitted curve
        plot_data = self.get_plot_data()
        plt.plot(plot_data.existing_x, plot_data.existing_y, label=self.target_data.label)

    def plot_statistical_model(self):
        # plot fitted curve
        plot_data = self.get_plot_data()
        plt.plot(plot_data.curve_x, plot_data.curve_y, label=self.target_data.label)

    def plot(self):
        """
        Plot existing data and fitted curve, save image to same directory as file_name
        :return:
        """

        plot_data = self.get_plot_data()

        x = plot_data.existing_x
        y = plot_data.existing_y
        date_point = plot_data.existing_date_point
        x_1 = plot_data.curve_x
        y_1 = plot_data.curve_y

        # plot existing
        plt.scatter(x, y)
        plt.annotate(f"{date_point[-1]}: {int(y[-1])}", xy=(x[-1], y[-1]),
                     xytext=(x[-1] / 2, y[-1]), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8))

        if x_1 is not None and y_1 is not None:
            # plot fitted curve
            plt.plot(x_1, y_1, color="red")
            plt.text(1, y[-1] / 9, self.statistic_model.fitted_formula, fontsize=12)

            # plot prediction
            predicted_x = x_1[len(x):][0:2]
            predicted_y = y_1[len(x):][0:2]
            plt.scatter(predicted_x, predicted_y)
            for index, (x, y) in enumerate(zip(predicted_x, predicted_y)):
                plt.annotate(str(int(y)), (x, y))

        plt.title(self.target_data.label)
        plt.savefig(f"plots/{self.target_data.label.split('.')[0]}.png")
        plt.show()


### Get Model ###

def get_file_model(city_name):
    file_name = f"data/{city_name}.csv"

    analysis_model = StatisticModel(si_model, si_expression)
    file_data = FileData(file_name)
    file_model = DataModel(file_data, analysis_model)
    return file_model


def get_country_model(country_name):
    country_data = CountryData(country_name)
    analysis_model = StatisticModel(si_model, si_expression)
    country_model = DataModel(country_data, analysis_model)
    return country_model


### Plotting


def plot_model_lists(models: List[DataModel]):
    """
    Plot alist of Data model to graph
    :param models:
    :return:
    """
    for data_model in models:
        data_model.plot_historical()
        # plot_data = data_model.get_plot_data()
        # # plot fitted curve
        # plt.plot(plot_data.curve_x, plot_data.curve_y, label=data_model.target_data.label)
    plt.legend()
    plt.yscale('log')
    plt.show()


def plot_country(country_name):
    country_model = get_country_model(country_name)
    country_model.plot()


def plot_file(file_name):
    file_model = get_file_model(file_name)
    file_model.plot()


def country_comparision(country_names):
    country_models = []
    for country in country_names:
        country_models.append(get_country_model(country))
    plot_model_lists(country_models)


def file_comparison(city_names):
    file_models = []
    for city in city_names:
        file_name = f"data/{city}.csv"
        analysis_model = StatisticModel(si_model, si_expression)
        file_data = FileData(file_name)
        file_model = DataModel(file_data, analysis_model)
        file_models.append(file_model)
    plot_model_lists(file_models)


if __name__ == '__main__':
    # city_name = "canada"
    # plot_city("canada")
    plot_country("United States")
    plot_country("Canada")
    country_comparision(["Canada", "Spain", "France", "United States", "United Kingdom", "Italy"])
    # group_comparison(["canada", "us"])
    # file_model.plot()

    # plot_file_models([file_model])
