from MLVisualisation.plots.BasicPlot import BasicPlot
from bokeh.plotting import figure
import numpy as np


class LinePlot(BasicPlot):

    def __init__(self, *argv, title="Dataset"):
        """
        :param argv: Triple which is (np.array([x_values]), np.array([y_values]), label)
        :param title: Titel for the plot
        """

        self.__title__ = title

        # need to check if x and y are the correct shape
        for arg in argv:
            if len(arg) != 3:
                raise ValueError(
                    "LinePlot needs tuple (np.array([x_values]), np.array([y_values]), label)"
                )

            x, y, title = arg

            if type(x) is not np.ndarray or type(y) is not np.ndarray:
                raise ValueError(
                    "LinePlot requires x,y values to be a numpy array"
                )

            if x.ndim != 1 or y.ndim != 1:
                raise ValueError(
                    "LinePlot requires x and y values to be an 1D numpy array"
                )

            if x.shape[0] != y.shape[0]:
                raise ValueError(
                    "LinePlot requires x and y datapoints to have the same length got length x: {} length y: {}"
                    .format(str(x.shape[0]), str(y.shape[0]))
                )

        self.__argv__ = argv

    def create_plot(self):
        """
        Creates the plot with the provided arguments that were passed when the class was
        initialized. It returns a plot that is used by the layout to print everything
        :return: bokeh plot
        """
        plot = figure(title=self.__title__)

        for arg in self.__argv__:
            # todo add auto colors
            if arg[2] == "":
                plot.line(arg[0], arg[1])
            else:
                plot.line(arg[0], arg[1], legend=arg[2])

        return plot
