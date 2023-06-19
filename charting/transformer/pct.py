from pandas import Series, DateOffset, DataFrame
from charting.model.transformer import Transformer


class Pct(Transformer):

    def __init__(self, periods: int):
        super().__init__()
        self.periods = periods

    def transform(self, x: Series, y: Series) -> (Series, Series):
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
