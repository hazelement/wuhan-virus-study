import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from statistic_models import si_model_expression as si_expression
from data import AbstractData
import random


# todo add states comparision in US
# todo add province comparision in Canada


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def hashval(str, siz):
    hash = 0
    # Take ordinal number of char in str, and just add
    for x in str: hash += (ord(x))
    return (hash % siz)  # Depending on the range, do a modulo operation.


colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
color_index = -1


def get_label_color(label):
    global color_index
    color_index += 1
    color_index = color_index % len(colors)
    return colors[color_index]


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


class EventData(object):

    def __init__(self):
        pass


class PlotData(object):

    def __init__(self,
                 existing_x,
                 existing_y,
                 existing_date_point,
                 curve_x,
                 curve_y,
                 events=None
                 ):
        self.existing_x = existing_x
        self.existing_y = existing_y
        self.existing_date_point = existing_date_point
        self.curve_x = curve_x
        self.curve_y = curve_y
        self.events = events


class DataModel(object):

    def __init__(self, target_data: AbstractData, statistics_model: StatisticModel):
        self.target_data = target_data
        self.statistic_model = statistics_model
        self.statistic_model.fit(self.target_data.x, self.target_data.y)

    def get_event_data(self, start_date):
        events = self.target_data.events
        valid_events = events[events['date'] >= start_date]
        valid_events['offset'] = valid_events['date'] - start_date
        return valid_events

    def get_plot_data(self, y_threshold=None):

        x = []
        y = []
        date_point = []
        i = -1

        for (x_, y_, date_point_) in zip(self.target_data.x, self.target_data.y, self.target_data.date_point):
            if y_threshold:
                if y_ < y_threshold:
                    continue
            i += 1
            x.append(i)
            y.append(y_)
            date_point.append(date_point_)

        if self.statistic_model.fitted:
            x_1 = np.arange(0, len(x) * 1.2, 1)
            y_1 = self.statistic_model.calculate(x_1)
        else:
            print("Statistical model not fitted")
            x_1 = None
            y_1 = None

        event_data = self.get_event_data(date_point[0])
        plot_event_data = []
        for index, row in event_data.iterrows():
            plot_event_data.append([row['offset'].days, f"{row['location']}: {row['event']}"])

        return PlotData(existing_x=x,
                        existing_y=y,
                        existing_date_point=date_point,
                        curve_x=x_1,
                        curve_y=y_1,
                        events=plot_event_data)

    def plot_historical(self, y_threshold=None):
        # plot fitted curve
        plot_data = self.get_plot_data(y_threshold)
        self.setup_axis(str(y_threshold))
        color = get_label_color(self.target_data.label)

        plt.plot(plot_data.existing_x, plot_data.existing_y, label=self.target_data.label, color=color)
        for event in plot_data.events:
            plt.text(event[0], 100,
                     event[1], rotation=90,
                     color=color)
            plt.axvline(event[0], dashes=(5, 2, 1, 2), color=color)

    def plot_statistical_model(self):
        # plot fitted curve
        plot_data = self.get_plot_data()
        self.setup_axis()

        plt.plot(plot_data.curve_x, plot_data.curve_y, label=self.target_data.label)

    def setup_axis(self, x_start_case="first"):
        plt.xlabel(f"Num days from first {x_start_case} confirmed case")
        plt.ylabel("Accumulative cases")

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

        self.setup_axis()
        plt.title(self.target_data.label)
        plt.savefig(f"plots/{self.target_data.label.split('.')[0]}.png")
        plt.show()
