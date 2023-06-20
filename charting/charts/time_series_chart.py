from typing import Tuple, List, Union
from charting.model.chart import Chart
from charting.model.style import get_color
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

    def add_data(self, x, y, label: str, y_axis: int, chart_type: str = 'line', linestyle: str = '-',
                 linewidth: float = 1, fill: bool = False, fill_threshold: float = None, bar_bottom: float = 0,
                 alpha: float = 1, transformer: Union[Transformer, List[Transformer]] = None, *args, **kwargs):
        """
        Adds a line series to the chart.

        Args:
            x: The x-values of the series.
            y: The y-values of the series.
            label (str): The label for the series.
            y_axis (int): The index of the y-axis to plot the series on.
            chart_type (str): The type of chart to plot ('line' or 'bar', default: 'line').
            linestyle (str): The line style of the series (default: '-').
            linewidth (float): The width of the line (default: 1)
            fill (bool): True if area between x and y should be filled (default: False).
            fill_threshold (float): The threshold value to fill the area below (default: None).
                               If not specified, the area will be filled from the line to the bottom axis.
            bar_bottom (float): The bottom for bar charts to plot (default: 0).
            alpha (float): The alpha value for the data plot (default: 1).
            transformer (Union[Transformer, List[Transformer]]): Optional transformer(s) to apply to the series
                (default: None). If a single transformer is provided, it will be applied to the series.
                If a list of transformers is provided, they will be applied sequentially to the series.
                Each transformer should implement the `transform` method to modify the series.
                The label of the series will be updated to reflect the applied transformers.

        """
        if y_axis >= self.num_y_axes:
            raise IndexError("Axis index out of range")

        color = get_color(y_axis=y_axis)
        axis_label = 'L1' if y_axis == 0 else f'R{y_axis}'

        if transformer is not None:
            if isinstance(transformer, list):
                x, y = reduce(lambda xy, trans: trans.transform(*xy), transformer, (x, y))
                label = f"{label}, {axis_label} ({', '.join(trans.label() for trans in transformer)})"
            elif isinstance(transformer, Transformer):
                x, y = transformer.transform(x, y)
                label = f"{label}, {axis_label} ({transformer.label()})"
        else:
            label = f"{label}, {axis_label}"

        if chart_type == 'line':
            handle, = self.y_axes[y_axis].plot(x, y, color=color,
                                               linestyle=linestyle, linewidth=linewidth, label=label, alpha=alpha)

            if fill:
                if fill_threshold is None:
                    fill_threshold = self.ax.get_ylim()[0]
                self.y_axes[y_axis].fill_between(x, y, fill_threshold, color=color, alpha=0.1)
        elif chart_type == 'bar':
            get_bar_width = lambda idx: (x[idx + 1] - x[idx]).days * 0.8 if idx < len(x) - 1 else None

            for i, (idx, diff) in enumerate(zip(x, y)):
                bar_width = get_bar_width(i)
                handle = self.y_axes[y_axis].bar(x[i], diff, align='edge', width=bar_width, bottom=bar_bottom, label=label,
                                                 color=color, alpha=alpha)
        else:
            raise NotImplemented(f"Chart type '{chart_type} is not implemented yet!")

        self.x_min.append(min(x))
        self.x_max.append(max(x))

        self.handles.append(handle)
