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

    def transform(self, x: Series, y: Series, language: str) -> (Series, Series):
        """
        Transforms the time series data by resampling it according to the specified rule.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The resampled x-values and y-values as separate Series.
        """
        self.language = language
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

        resampler = {
            "sum": "Summe",
            "mean": "Durschnitt"
        }

        self.resampler = resampler.get(self.resampler) if self.language == 'de' else self.resampler

        if self.language == 'en':
            if self.rule == 'W':
                return f'weekly {self.resampler}'
            if self.rule == 'M':
                return f'monthly {self.resampler}'
            if self.rule == 'Y':
                return f'yearly {self.resampler}'
            if self.rule == 'Q':
                return f'quarterly {self.resampler}'
            return 'unknown'

        if self.language == 'de':
            if self.rule == 'W':
                return f'wöchentlich {self.resampler}'
            if self.rule == 'M':
                return f'monatlich {self.resampler}'
            if self.rule == 'Y':
                return f'jährlich {self.resampler}'
            if self.rule == 'Q':
                return f'quartalsweise {self.resampler}'
            return 'unbekannt'

        return 'unbekannt'