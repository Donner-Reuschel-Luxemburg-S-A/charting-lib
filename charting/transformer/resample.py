from pandas import Series, DataFrame

from charting.model.transformer import Transformer


class Resample(Transformer):
    """
    A transformer that resamples time series data.
    """

    def __init__(self, rule: str):
        """
        Initializes a Resample transformer with the specified resampling rule.

        Args:
            rule (str): The resampling rule, such as 'W' for weekly, 'M' for monthly, 'Y' for yearly.
        """
        super().__init__()
        self.rule = rule

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Transforms the time series data by resampling it according to the specified rule.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The resampled x-values and y-values as separate Series.
        """
        df = DataFrame({'y': y}, index=x)
        resampled_df = df.resample(self.rule).mean()
        resampled_x = resampled_df.index
        resampled_y = resampled_df['y']

        return resampled_df.index, resampled_y

    def label(self) -> str:
        """
        Returns a label describing the transformation.

        Returns:
            str: The label for the transformation.
        """
        if self.rule == 'W':
            return 'weekly'
        if self.rule == 'M':
            return 'monthly'
        if self.rule == 'Y':
            return 'yearly'

        return 'unknown'
