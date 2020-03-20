import numpy as np

import requests
import pandas as pd
import os
import time

WHO_LINK = "https://covid.ourworldindata.org/data/full_data.csv"

CACHE_FILE = "data/who_data.csv"
EVENTS_FILE = "data/events.csv"


def read_file(filename):
    df = pd.read_csv(filename)
    return df.iloc[:, 1].astype(float).copy().values, df.iloc[:, 0].astype(str).copy().values


def retrieve_who_data():
    r = requests.get(WHO_LINK, allow_redirects=True)
    open(CACHE_FILE, 'wb').write(r.content)


def read_data(filename):
    # todo handle cache and auto update on daily basis
    data = pd.read_csv(filename)
    data.fillna(0, inplace=True)
    data['date'] = data['date'].astype('datetime64[ns]')

    return data


class WhoDataSource(object):

    def __init__(self):
        if (int(time.time()) - os.path.getmtime(CACHE_FILE)) > 24 * 60 * 60:
            retrieve_who_data()

        self.df = read_data(CACHE_FILE)

    def get_location_data(self, location):
        return self.df[self.df["location"] == location]


class EventData(WhoDataSource):

    def __init__(self):
        self.df = read_data(EVENTS_FILE)


class AbstractData(object):
    x = None
    total_cases = None
    new_cases = None
    label = None
    date_point = None
    events = None


class CountryData(AbstractData):

    def __init__(self, country_name):
        who_data_source = WhoDataSource()
        event_data_source = EventData()
        country_data = who_data_source.get_location_data(country_name)

        self.total_cases = country_data["total_cases"].values
        self.new_cases = country_data["new_cases"].values
        self.date_point = country_data["date"].values
        self.x = np.arange(0, len(self.total_cases), 1)
        self.label = country_name
        self.events = event_data_source.get_location_data(country_name)



class FileData(AbstractData):

    def __init__(self, label):
        self.y, self.date_point = read_file(label)
        self.x = np.arange(0, len(self.y), 1)
        self.label = label


if __name__ == '__main__':
    ds = WhoDataSource()
    print(ds.get_location_data("United States"))
