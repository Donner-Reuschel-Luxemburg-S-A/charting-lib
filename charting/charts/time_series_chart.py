from typing import Tuple, Callable, List, Union

import matplotlib.pyplot as plt
from matplotlib.ticker import Formatter

from charting.transformer.transformer import Transformer
from functools import reduce


class TimeSeriesChart:

    def __init__(self, title: str = "", num_y_axes: int = 1, figsize: Tuple[int, int] = (12, 8)):
        """
        Initializes a TimeSeriesChart object.

        Args:
            title (str): The title of the chart (default: "").
            num_y_axes (int): The number of y-axes for the chart (default: 1).
            figsize (tuple): The figure size of the chart (default: (12, 8)).
        """
        super().__init__()
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.title = title
        self.num_y_axes = num_y_axes
        self.y_axes = [self.ax]

        for i in range(1, self.num_y_axes):
            twin_ax = self.ax.twinx()
            twin_ax.spines.right.set_position(("axes", 1 + (i-1) * 0.1))
            self.y_axes.append(twin_ax)

        self.y_labels = [None] * num_y_axes
        self.y_colors = [None] * num_y_axes
        self.y_lims = [None] * num_y_axes
        self.handles = []

    def configure_y_axis(self, axis_index: int, label: str = None, color: str = "black", y_lim: Tuple[int, int] = None):
        """
        Configures a y-axis with a label and color.

        Args:
            axis_index (int): The index of the y-axis to configure.
            label (str): The label for the y-axis.
            color (str): The color for the y-axis.
            y_lim (tuple): The limits for the axis.

        Raises:
            IndexError: If the axis index is out of range.
        """
        if axis_index >= self.num_y_axes:
            raise IndexError("Axis index out of range")

        if label is not None:
            self.y_labels[axis_index] = label

        self.y_colors[axis_index] = color

        if y_lim is not None:
            self.y_lims[axis_index] = y_lim

    def configure_x_axis(self, x_lim: Tuple[int, int] = None, label: str = None, color: str = "black",
                         formatter: Formatter = None, rotation: int = 0):
        """
        Configures the x-axis with limits, label, and color.

        Args:
            x_lim (tuple): The limits for the x-axis (default: None).
            label (str): The label for the x-axis (default: None).
            color (str): The color for the x-axis (default: None).
            formatter (Formatter): The formatter for the x-axis (default: None)
            rotation (int): The rotation for the x-axis labels (default: 0).
        """
        if x_lim is not None:
            self.ax.set_xlim(*x_lim)

        self.ax.set_xlabel(label)
        self.ax.xaxis.label.set_color(color)
        self.ax.tick_params(axis='x', colors=color, rotation=rotation)

        if formatter is not None:
            self.ax.xaxis.set_major_formatter(formatter)

    def add_line_series(self, x, y, label: str, y_axis: int, color: str = 'black', linestyle: str = '-',
                        transformer: Union[Transformer, List[Transformer]] = None):
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

    def legend(self, loc: str = 'upper center', bbox_to_anchor: Tuple[int, int] = (0.5, -0.1), ncol: int = 4,
                         frameon: bool = True, **kwargs):
        """
        Configures the legend for the chart.

        Args:
            loc (str): The location of the legend (default: 'upper center').
            bbox_to_anchor (tuple): The anchor point of the legend box (default: (0.5, -0.1)).
            ncol (int): The number of columns in the legend (default: 4).
            frameon (bool): Whether to draw a frame around the legend (default: True).
            **kwargs: Additional keyword arguments to pass to the legend function.
        """
        self.ax.legend(handles=self.handles, loc=loc, bbox_to_anchor=bbox_to_anchor, ncol=ncol,
                       frameon=frameon, **kwargs)

    def __apply_formatting(self):
        """
        Applies the y-axis configuration and styling to the chart.
        """
        self.ax.set_ylabel(self.y_labels[0])
        self.ax.yaxis.label.set_color(self.y_colors[0])
        self.ax.tick_params(axis='y', colors=self.y_colors[0])

        if self.y_lims[0] is not None:
            self.ax.set_ylim(self.y_lims[0])

        for i in range(1, self.num_y_axes):
            twin_ax = self.y_axes[i]

            if self.y_lims[i] is not None:
                twin_ax.set_ylim(self.y_lims[i])

            twin_ax.set_ylabel(self.y_labels[i])
            color = self.y_colors[i] if self.y_colors[i] is not None else 'b'
            twin_ax.yaxis.label.set_color(color)
            twin_ax.tick_params(axis='y', colors=color)

    def plot(self, path: str):
        """
        Plots the chart and saves it as png.

        Args:
            path (str): the path to save the file to.
        """
        self.__apply_formatting()
        plt.title(self.title)

        plt.tight_layout()

        plt.savefig(path)
        plt.close()
