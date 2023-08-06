from MLVisualisation.plots.LinePlot import LinePlot
import numpy as np


class LossValidationPlot(LinePlot):

    def __init__(self, loss_history, epochs=None, title="Validation Loss"):

        if type(loss_history) is not np.ndarray:
            raise ValueError(
                "LossValidationPlot requires loss_history to be a numpy array, got {0}"
                .format(str(type(loss_history)))
            )

        if loss_history.ndim != 1:
            raise ValueError(
                "LossValidationPlot requires loss_history to be a 1-D numpy array, got{0}"
                .format(str(loss_history.shape))
            )

        self.__loss_history__ = loss_history

        if epochs is not None:

            if loss_history.shape != epochs.shape:
                raise ValueError(
                    "LossValidationPlot requires loss_history and x_values to have same shape, got x_values: {}, "
                    "loss_history: {}".format(str(epochs.shape), str(loss_history.shape))
                )

            if type(loss_history) is not np.ndarray:
                raise ValueError(
                    "LossValidationPlot requires x_values to be a numpy array, got {0}".format(str(type(loss_history))))

            self.__epochs__ = epochs
        else:
            # Automatically construct labels for the epochs if they're not explicitly stated
            self.__epochs__ = np.arange(loss_history.shape[0])

        self.__title__ = title

        super().__init__((self.__epochs__, self.__loss_history__, ""), title=self.__title__)

    def create_plot(self):
        plot = super().create_plot()
        plot.xaxis.axis_label = 'Epoch'
        plot.yaxis.axis_label = 'Val Loss'
        return plot
