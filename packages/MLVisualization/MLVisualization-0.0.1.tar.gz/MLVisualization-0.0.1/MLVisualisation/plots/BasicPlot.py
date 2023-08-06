class BasicPlot(object):
    """
    This is just the base class that defines an interface for the rest, enduser shouldn't be
    concerned with it
    """

    def create_plot(self):
        raise NotImplementedError("create_plot is not implemented")
