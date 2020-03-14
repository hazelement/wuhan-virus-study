import numpy as np

import requests
import pandas as pd

WHO_LINK = "https://covid.ourworldindata.org/data/full_data.csv"

CACHE_FILE = "data/who_data.csv"


def read_file(filename):
    df = pd.read_csv(filename)
    return df.iloc[:, 1].astype(float).copy().values, df.iloc[:, 0].astype(str).copy().values


def retrieve_who_data():
    r = requests.get(WHO_LINK, allow_redirects=True)
    open(CACHE_FILE, 'wb').write(r.content)


def read_data():
    # todo handle cache and auto update on daily basis
    data = pd.read_csv(CACHE_FILE)
    data.fillna(0, inplace=True)

    return data


class WhoDataSource(object):

    def __init__(self):
        self.df = read_data()

    def get_location_data(self, location):
        return self.df[self.df["location"] == location]


class AbstractData(object):
    x = None
    y = None
    label = None
    date_point = None


class CountryData(AbstractData):

    def __init__(self, country_name):
        who_data_source = WhoDataSource()
        country_data = who_data_source.get_location_data(country_name)

        self.y = country_data["total_cases"].values
        self.date_point = country_data["date"].values
        self.x = np.arange(0, len(self.y), 1)
        self.label = country_name


class FileData(AbstractData):

    def __init__(self, label):
        self.y, self.date_point = read_file(label)
        self.x = np.arange(0, len(self.y), 1)
        self.label = label


if __name__ == '__main__':
    ds = WhoDataSource()
    print(ds.get_location_data("United States"))
