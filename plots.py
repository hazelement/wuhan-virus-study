from typing import List

from matplotlib import pyplot as plt

from analysis import DataModel, StatisticModel
from data import FileData, CountryData
from statistic_models import si_model as si_model, si_model_expression as si_expression


def plot_model_lists(models: List[DataModel], savefig=None, y_threshold=None):
    """
    Plot alist of Data model to graph
    :param models:
    :return:
    """
    for data_model in models:
        data_model.plot_historical(y_threshold)
    plt.legend()
    plt.yscale('log')
    if savefig is not None:
        plt.savefig(savefig)
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
    plot_model_lists(country_models, "plots/countries.png", 50)


def file_comparison(city_names):
    file_models = []
    for city in city_names:
        file_name = f"data/{city}.csv"
        analysis_model = StatisticModel(si_model, si_expression)
        file_data = FileData(file_name)
        file_model = DataModel(file_data, analysis_model)
        file_models.append(file_model)
    plot_model_lists(file_models)


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