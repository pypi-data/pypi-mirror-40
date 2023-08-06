from MLVisualisation.plots.BasicPlot import BasicPlot
import numpy as np
import pandas as pd
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import transform


class ConfusionMatrixPlot(BasicPlot):

    def __init__(self, y_test, y_train, normalize=False, title="Confusion Matrix", labels=None,
                 color_palette="Magma256"):
        self.__title__ = title
        self.__normalize__ = normalize
        self.__color_palette__ = color_palette

        if (type(y_test) and type(y_train)) is not np.ndarray:
            raise ValueError(
                "ConfusionMatrixPlot requires dataset to be a numpy array, got y_test: {} and y_train {}"
                    .format(str(type(y_test)), str(type(y_train)))
            )

        if y_test.ndim != 1 and y_train.ndim != 1:
            raise ValueError(
                "PCAPlot requires dataset to be a 1-D numpy array, got y_test: {} and y_train {}"
                    .format(str(y_test.shape), str(y_train.shape))
            )

        # check if both have the same length and if they're the same time

        self.__y_train__ = y_train.astype(str)
        self.__y_test__ = y_test.astype(str)

        if labels is None:
            self.__labels__ = np.unique(y_train)
        else:
            self.__labels__ = np.asarray(labels)

        pass

    def __normalized__(a, axis=-1, order=2):
        l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
        l2[l2 == 0] = 1
        return a / np.expand_dims(l2, axis)

    def create_plot(self):
        factors = self.__labels__.astype(str).tolist()

        y_actu = pd.Series(self.__y_train__, name='Actual')
        y_pred = pd.Series(self.__y_test__, name='Predicted')
        df = pd.crosstab(y_actu, y_pred)

        # Prepare data.frame in the right format
        df = df.stack().rename("value").reset_index()

        # Had a specific mapper to map color with value
        mapper = LinearColorMapper(palette='Magma256', low=df.value.min(), high=df.value.max())

        plot = figure(
            title=self.__title__,
            x_range=factors,
            y_range=factors,
            toolbar_location=None
        )

        # Create rectangle for heatmap
        plot.rect(
            x="Actual",
            y="Predicted",
            width=1,
            height=1,
            source=ColumnDataSource(df),
            line_color=None,
            fill_color=transform('value', mapper))
        # Add legend
        color_bar = ColorBar(
            color_mapper=mapper,
            location=(0, 0),
            ticker=BasicTicker(desired_num_ticks=5))

        plot.add_layout(color_bar, 'right')

        return plot
