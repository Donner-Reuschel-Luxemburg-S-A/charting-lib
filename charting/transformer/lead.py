import datetime
from pandas import Series, DateOffset

from charting.transformer import _generate_label
from charting.model.transformer import Transformer


class Lead(Transformer):
    """
    Transformer that performs a forward shift of a time series by a specified timedelta.

    Attributes:
        offset (DateOffset): The offset to shift the time series backward.
    """

    def __init__(self, offset: DateOffset):
        """
        Initializes a Lag transformer.

        Args:
            offset (DateOffset): The offset to shift the time series backward.
        """
        super().__init__()
        self.offset = offset

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Performs a forward shift of the time series by the specified offset.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The shifted x-values and the original y-values of the time series.
        """
        shifted_x = x + self.offset
        return shifted_x, y

    def label(self) -> str:
        """
        Generates a label describing the Lead transformer.

        Returns:
            str: The label describing the Lead transformer.
        """
        return _generate_label(offset=self.offset, action='lead')
