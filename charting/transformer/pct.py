from pandas import Series, DataFrame

from charting.model.transformer import Transformer


class Pct(Transformer):
    """
    A transformer class that calculates the percentage change over a specified number of periods.

    Attributes:
        periods (int): The number of periods to calculate the percentage change over.
    """

    def __init__(self, periods: int):
        """
        Initializes a new instance of the Pct class.

        Args:
            periods (int): The number of periods to calculate the percentage change over.
        """
        super().__init__()
        self.periods = periods

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Applies the percentage change transformation to the input data.

        Args:
            x (Series): The input x-values.
            y (Series): The input y-values.

        Returns:
            Tuple[Series, Series]: The transformed x-values and y-values.
        """
        df = DataFrame({'y': y}, index=x)
        df = df.pct_change(periods=self.periods) * 100
        df = df.dropna()
        x_new = df.index
        y_new = df['y']
        return x_new, y_new

    def label(self) -> str:
        """
        Returns a label describing the transformation.

        Returns:
            str: The label for the transformation.
        """
        return f"pct ~ {self.periods} periods"
