import datetime
from pandas import Series

from charting.transformer import _generate_label
from charting.model.transformer import Transformer


class Lead(Transformer):
    """
    Transformer that performs a forward shift of a time series by a specified timedelta.

    Attributes:
        window (datetime.timedelta): The timedelta to shift the time series forward.
    """

    def __init__(self, window: datetime.timedelta):
        """
        Initializes a Lead transformer.

        Args:
            window (datetime.timedelta): The timedelta to shift the time series forward.
        """
        super().__init__()
        self.window = window

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Performs a forward shift of the time series by the specified timedelta.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The shifted x-values and the original y-values of the time series.
        """
        shifted_x = x + self.window
        return shifted_x, y

    def label(self) -> str:
        """
        Generates a label describing the Lead transformer.

        Returns:
            str: The label describing the Lead transformer.
        """
        return _generate_label(window=self.window, action='lead')
