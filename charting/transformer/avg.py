import datetime

from pandas import Series, DateOffset

from charting.model.transformer import Transformer
from charting.transformer import _generate_label


class Avg(Transformer):
    """
    Transformer to calculate the average of a time series within a given offset.

    This transformer applies a rolling mean calculation to the values of the input time series.
    """

    def __init__(self, offset: DateOffset):
        """
        Initializes an Avg transformer with the specified offset.

        Args:
            offset (DateOffset): The offset for calculating the rolling mean.
        """
        super().__init__()
        self.offset = offset

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Applies the rolling mean calculation to the time series.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The transformed x-values and y-values.
        """
        start_date = datetime.datetime.today()
        end_date = start_date + self.offset
        days = (end_date - start_date).days
        return x, y.rolling(window=f'{days}D').mean()

    def label(self) -> str:
        """
        Returns a label describing the transformation.

        Returns:
            str: The label for the transformation.
        """
        return _generate_label(offset=self.offset, action='avg')
