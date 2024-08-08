from pandas import Series

from charting.model.transformer import Transformer


class Center(Transformer):
    """
    Transformer to modify data based on a threshold.

    Attributes:
        val (float): The threshold value to use as bottom.
    """

    def __init__(self, val: float):
        """
        Initializes a Lag transformer.

        Args:
            val (float): The threshold value to use as bottom.
        """
        super().__init__()
        self.val = val

    def transform(self, x: Series, y: Series, language: str) -> (Series, Series):
        """
        Applies the difference transformation to the time series.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The transformed x-values and y-values.
        """
        self.language = language
        return x, y - self.val

    def label(self) -> str:
        """
        Returns a label describing the transformation.

        Returns:
            str: The label for the transformation.
        """

        if self.language == 'en':
            label = 'centered'
        else:
            label = 'zentriert'

        return f"{label} ~ {self.val}"
