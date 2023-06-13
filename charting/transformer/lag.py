import datetime
from pandas import Series

from charting.transformer import _generate_label
from charting.transformer.transformer import Transformer


class Lag(Transformer):
    """
    Transformer that performs a backward shift of a time series by a specified timedelta.

    Attributes:
        window (datetime.timedelta): The timedelta to shift the time series backward.
    """

    def __init__(self, window: datetime.timedelta):
        """
        Initializes a Lag transformer.

        Args:
            window (datetime.timedelta): The timedelta to shift the time series backward.
        """
        super().__init__()
        self.window = window

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Performs a backward shift of the time series by the specified timedelta.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The shifted x-values and the original y-values of the time series.
        """
        shifted_x = x - self.window
        return shifted_x, y

    def label(self) -> str:
        """
        Generates a label describing the Lag transformer.

        Returns:
            str: The label describing the Lag transformer.
        """
        return _generate_label(window=self.window, action='lag')
