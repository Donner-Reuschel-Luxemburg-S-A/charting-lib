import pandas as pd
from pandas import Series, DataFrame

from charting.model.transformer import Transformer


class Ytd(Transformer):
    """
    A transformer class that calculates the yield to date.
    """

    def __init__(self):
        """
        Initializes a new instance of the Ytd class.
        """
        super().__init__()

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Applies the yield to date transformation to the input data.

        Args:
            x (Series): The input x-values.
            y (Series): The input y-values.

        Returns:
            Tuple[Series, Series]: The transformed x-values and y-values.
        """
        df = DataFrame({'y': y}, index=x)
        start_value = df.iloc[0]['y']
        ytd = (df['y'] - start_value) / start_value * 100
        x_new = df.index
        y_new = ytd
        return x_new, y_new

    def label(self) -> str:
        """
        Returns a label describing the transformation.

        Returns:
            str: The label for the transformation.
        """
        return f"ytd"
