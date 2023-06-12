from pandas import Series

from charting.transformer.transformer import Transformer


class Invert(Transformer):

    def transform(self, x: Series, y: Series) -> (Series, Series):
        return x, -y

    def label(self) -> str:
        return "inverted"
