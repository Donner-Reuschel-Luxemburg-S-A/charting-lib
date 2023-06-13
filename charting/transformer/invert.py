from pandas import Series

from charting.model.transformer import Transformer


class Invert(Transformer):
    """
    Transformer to invert a time series.

    This transformer applies a negation to the values of the input time series.
    """

    def transform(self, x: Series, y: Series) -> (Series, Series):
        """
        Applies the inversion transformation to the time series.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The transformed x-values and y-values.
        """

        return x, -y

    def label(self) -> str:
        """
        Returns a label describing the transformation.

        Returns:
            str: The label for the transformation.
        """

        return "inverted"
