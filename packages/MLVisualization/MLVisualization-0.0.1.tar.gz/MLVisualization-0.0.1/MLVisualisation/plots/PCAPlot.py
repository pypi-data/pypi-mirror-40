from MLVisualisation.plots.BasicPlot import BasicPlot
from sklearn.decomposition import PCA
from bokeh.palettes import Category20
from bokeh.plotting import figure
import numpy as np


class PCAPlot(BasicPlot):

    def __init__(self, dataset, labels, title="Dataset"):

        if type(dataset) is not np.ndarray:
            raise ValueError(
                "PCAPlot requires dataset to be a numpy array, got {}".format(str(type(dataset)))
            )

        if dataset.ndim != 2:
            raise ValueError(
                "PCAPlot requires dataset to be a 2-D numpy array, got {}".format(str(dataset.shape))
            )

        self.__dataset__ = dataset

        dataset_entries = dataset.shape[0]
        label_entries = labels.shape[0]

        if type(labels) is not np.ndarray:
            raise ValueError(
                "PCAPlot requires labels to be a numpy array, got {}".format(str(type(labels)))
            )

        if dataset_entries != label_entries:
            raise ValueError(
                "PCAPlot requires dataset and labels to have same amount of entries, got dataset: {}, "
                "labels: {}".format(str(dataset_entries), str(label_entries))
            )

        if labels.ndim != 1:
            raise ValueError(
                "PCAPlot requires labels to be an 1-D numpy array, got {}".format(str(labels.shape))
            )

        self.__labels__ = labels

        self.__title__ = title


    def create_plot(self):
        p = figure(title=self.__title__)
        pca = PCA(n_components=2)
        dataset_fit = pca.fit_transform(self.__dataset__)

        for idx, val in enumerate(dataset_fit):
            # TODO limit the color choices somehow, or randomly create a palette
            # TODO use vectorized function to faster add each datapoint on the plot
            fill_color = Category20[10][self.__labels__[idx]]
            p.scatter(val[0], val[1], marker="circle", fill_color=fill_color, size=8)

        return p


