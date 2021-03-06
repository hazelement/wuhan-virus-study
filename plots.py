from typing import List

import matplotlib
from analysis import DataModel, StatisticModel, datetime64_to_datetime
from data import CountryData, FileData
from matplotlib import pyplot as plt
from statistic_models import si_model as si_model
from statistic_models import si_model_expression as si_expression

font = {'size': 12}
matplotlib.rc('font', **font)


def save_plot(filename):
    plt.savefig(filename, format="png")


def plot_model_lists(models: List[DataModel], y_threshold=None, label_vertical=True,
                     plot_accumulative=True):
    """
    Plot alist of Data model to graph
    :param models:
    :return:
    """
    plt.figure(figsize=(16, 9))
    plt.grid(b=True)
    for data_model in models:
        data_model.plot_data(y_threshold, label_vertical, plot_accumulative)
    plt.legend()
    plt.yscale('log')
    last_date = datetime64_to_datetime(
        models[0].data_last_date).strftime("%Y-%m-%d")
    plt.title(f"Data updated on {last_date}")


def plot_country(country_name):
    country_model = get_country_total_model(country_name)
    country_model.plot()


def plot_file(file_name):
    file_model = get_file_model(file_name)
    file_model.plot()


def country_total_comparison(country_names):
    country_models = []
    for country in country_names:
        country_models.append(get_country_total_model(country))
    plot_model_lists(country_models, 100, False)


def country_incremental_comparison(country_names):
    country_models = []
    for country in country_names:
        country_models.append(get_country_total_model(country))

    plot_model_lists(
        country_models, "plots/country_incrementals.png", 50, False, False)


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


def get_country_total_model(country_name):
    country_total_data = CountryData(country_name)
    analysis_model = StatisticModel(si_model, si_expression)
    country_total_model = DataModel(country_total_data, analysis_model)
    return country_total_model
