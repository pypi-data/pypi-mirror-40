from bokeh.plotting import show, output_file
from bokeh.layouts import gridplot

class GridLayout:

    # TODO add parameters such as size etc
    def __init__(self, filename="visualization.html", title="Visualization"):
        self.__plots__ = []
        self.__filename__ = filename
        self.__title__ = title

    # TODO create base class for layouts that implements add
    def add(self, plot):
        # TODO generate the plot afterward, first let the user configure their setup
        self.__plots__.append(plot.create_plot())

    def show(self):
        output_file(self.__filename__, title=self.__title__)
        show(gridplot([self.__plots__], plot_width=400, plot_height=400))

