import datetime
from pandas import Series
from charting.transformer import _generate_label
from charting.transformer.transformer import Transformer


class Avg(Transformer):
    """
    Transformer to calculate the average of a time series within a given window.

    This transformer applies a rolling mean calculation to the values of the input time series.
    """

    def __init__(self, window: datetime.timedelta):
        """
        Initializes an Avg transformer with the specified window.

        Args:
            window (datetime.timedelta): The window size for calculating the rolling mean.
        """
        self.window = window

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Applies the rolling mean calculation to the time series.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The transformed x-values and y-values.
        """
        window = int(self.window.total_seconds() / (60 * 60 * 24))
        return x, y.rolling(window=window).mean()

    def label(self) -> str:
        """
        Returns a label describing the transformation.

        Returns:
            str: The label for the transformation.
        """
        return _generate_label(window=self.window, action='avg')
