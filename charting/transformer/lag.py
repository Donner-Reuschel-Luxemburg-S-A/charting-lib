from pandas import Series, DateOffset

from charting.model.transformer import Transformer
from charting.transformer import _generate_label


class Lag(Transformer):
    """
    Transformer that performs a backward shift of a time series by a specified timedelta.

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

    def transform(self, x: Series, y: Series, language: str) -> (Series, Series):
        """
        Performs a backward shift of the time series by the specified offset.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The shifted x-values and the original y-values of the time series.
        """
        self.language = language
        shifted_x = x - self.offset
        return shifted_x, y

    def label(self) -> str:
        """
        Generates a label describing the Lag transformer.

        Returns:
            str: The label describing the Lag transformer.
        """
        action = 'lag' if self.language == 'en' else 'verzögert'
        return _generate_label(offset=self.offset, action=action, language=self.language)
