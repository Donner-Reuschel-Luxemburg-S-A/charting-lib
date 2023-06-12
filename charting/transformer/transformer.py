from abc import abstractmethod, ABC
from typing import Iterable

from pandas import Series


class Transformer(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def transform(self, x: Series, y: Series) -> (Series, Series):
        pass

    @abstractmethod
    def label(self) -> str:
        pass

    def __iter__(self) -> Iterable:
        yield self

    def __call__(self, x: Series, y: Series) -> Series:
        return self.transform(x=x, y=y)
