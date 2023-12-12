from pandas import Series, DataFrame

from charting.model.transformer import Transformer


class Resample(Transformer):
    """
    A transformer that resamples time series data.
    """

    def __init__(self, rule: str, resampler: str = 'mean'):
        """
        Initializes a Resample transformer with the specified resampling rule.

        Args:
            rule (str): The resampling rule, such as 'W' for weekly, 'M' for monthly, 'Y' for yearly.
            resampler (str): the resample algorithm (default: mean)
        """
        super().__init__()
        self.rule = rule
        self.resampler = resampler

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
        resampled_df = getattr(df.resample(self.rule), self.resampler)()
        resampled_df.index = resampled_df.index.to_period(self.rule).to_timestamp(how='start')
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
            return f'weekly {self.resampler}'
        if self.rule == 'M':
            return f'monthly {self.resampler}'
        if self.rule == 'Y':
            return f'yearly {self.resampler}'
        if self.rule == 'Q':
            return f'quarterly {self.resampler}'

        return 'unknown'
