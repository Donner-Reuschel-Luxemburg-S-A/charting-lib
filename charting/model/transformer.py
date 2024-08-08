from abc import ABC, abstractmethod
from typing import Iterable

from pandas import Series


class Transformer(ABC):
    """
    Abstract base class for transformers that modify time series data.

    Subclasses should implement the `transform` and `label` methods.
    """

    def __init__(self):
        """
        Initializes a Transformer object.
        """
        pass

    @abstractmethod
    def transform(self, x: Series, y: Series, language: str) -> (Series, Series):
        """
        Transforms the time series data.

        This method should be implemented by subclasses to modify the input time series data.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The transformed x-values and y-values of the time series.
        """
        pass

    @abstractmethod
    def label(self) -> str:
        """
        Generates a label for the transformer.

        This method should be implemented by subclasses to generate a label describing the transformer.

        Returns:
            str: The label describing the transformer.
        """
        pass

    def __iter__(self) -> Iterable:
        """
        Makes the transformer iterable.

        This method allows the transformer to be used in a list of transformers.

        Returns:
            Iterable: An iterable containing the transformer.
        """
        yield self

    def __call__(self, x: Series, y: Series) -> (Series, Series):
        """
        Applies the transformer to the time series data.

        This method allows the transformer to be called as a function, applying the transformer to the time series data.

        Args:
            x (Series): The x-values of the time series.
            y (Series): The y-values of the time series.

        Returns:
            (Series, Series): The transformed x-values and y-values of the time series.
        """
        return self.transform(x=x, y=y)
