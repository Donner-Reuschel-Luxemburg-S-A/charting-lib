from typing import Tuple, List, Union
from charting.model.chart import Chart
from charting.model.transformer import Transformer
from functools import reduce


class TimeSeriesChart(Chart):
    """
    A Time Series Chart.
    """

    def __init__(self, title: str = "", num_y_axes: int = 1, figsize: Tuple[int, int] = (12, 8)):
        """
        Initializes a TimeSeriesChart object.

        Args:
            title (str): The title of the chart (default: "").
            num_y_axes (int): The number of y-axes for the chart (default: 1).
            figsize (tuple): The figure size of the chart (default: (12, 8)).
        """
        super().__init__(title=title, num_y_axes=num_y_axes, figsize=figsize)

    def add_data(self, x, y, label: str, y_axis: int, color: str = 'black', linestyle: str = '-',
                 transformer: Union[Transformer, List[Transformer]] = None, *args, **kwargs):
        """
        Adds a line series to the chart.

        Args:
            x: The x-values of the series.
            y: The y-values of the series.
            label (str): The label for the series.
            y_axis (int): The index of the y-axis to plot the series on.
            color (str): The color of the line series (default: 'black').
            linestyle (str): The line style of the series (default: '-').
            transformer (Union[Transformer, List[Transformer]]): Optional transformer(s) to apply to the series
                (default: None). If a single transformer is provided, it will be applied to the series.
                If a list of transformers is provided, they will be applied sequentially to the series.
                Each transformer should implement the `transform` method to modify the series.
                The label of the series will be updated to reflect the applied transformers.
        """
        if y_axis >= self.num_y_axes:
            raise IndexError("Axis index out of range")

        if transformer is not None:
            if isinstance(transformer, list):
                x, y = reduce(lambda xy, trans: trans.transform(*xy), transformer, (x, y))
                label = f"{label} ({', '.join(trans.label() for trans in transformer)})"
            elif isinstance(transformer, Transformer):
                x, y = transformer.transform(x, y)
                label = f"{label} ({transformer.label()})"

        line, = self.y_axes[y_axis].plot(x, y, color=color, linestyle=linestyle, label=label)
        self.handles.append(line)
