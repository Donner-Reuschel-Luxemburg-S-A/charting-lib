import datetime
from abc import ABC, abstractmethod
from typing import Tuple, List

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.pyplot import xlim
from matplotlib.ticker import Formatter, Locator, AutoLocator

from charting.model.style import title_style, source_text_style


class Chart(ABC):
    """
    Abstract base class representing a chart.
    """

    def __init__(self, title: str = "", num_y_axes: int = 1, figsize: Tuple[int, int] = (12, 8)):
        """
        Initializes a Chart object.

        Args:
            title (str): The title of the chart (default: "").
            num_y_axes (int): The number of y-axes for the chart (default: 1).
            figsize (tuple): The figure size of the chart (default: (12, 8)).
        """
        self.title = title
        self.num_y_axes = num_y_axes
        self.figsize = figsize
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.spines['top'].set_visible(False)
        self.handles = []
        self.y_labels = [None] * num_y_axes
        self.y_lims = [None] * num_y_axes
        self.y_axes = self.__init_y_axes()
        self.x_min = []
        self.x_max = []
        self.legend_y = 0

    def __init_y_axes(self) -> List[Axes]:
        """
        Initializes and returns the y-axes for the chart.

        Returns:
            List (Axes): The list of y-axes for the chart.
        """

        y_axes = [self.ax]

        for i in range(1, self.num_y_axes):
            twin_ax = self.ax.twinx()
            twin_ax.spines.right.set_position(("axes", 1 + (i - 1) * 0.1))
            twin_ax.spines['top'].set_visible(False)
            y_axes.append(twin_ax)

        return y_axes

    def configure_x_axis(self, x_lim: Tuple[int, int] = None, label: str = None,
                         minor_formatter: Formatter = None,
                         major_formatter: Formatter = None,
                         minor_locator: Locator = None,
                         major_locator: Locator = None):
        """
        Configures the x-axis with limits, label, and color.

        Args:
            x_lim (tuple): The limits for the x-axis (default: None).
            label (str): The label for the x-axis (default: None).
            minor_formatter (Formatter): The minor formatter for the x-axis (default: None)
            major_formatter (Formatter): The major formatter for the x-axis (default: None)
            minor_locator (Locator): The minor locator for the x-axis (default: None)
            major_locator (Locator): The major locator for the x-axis (default: None)
        """
        if x_lim is not None:
            self.ax.set_xlim(*x_lim)

        self.ax.set_xlabel(label)

        if minor_formatter is not None:
            self.ax.xaxis.set_minor_formatter(minor_formatter)

        if major_formatter is not None:
            self.ax.xaxis.set_major_formatter(major_formatter)

        if minor_locator is not None:
            self.ax.xaxis.set_minor_locator(minor_locator)

        if major_locator is not None:
            self.ax.xaxis.set_major_locator(major_locator)

    def configure_x_ticks(self, which: str = 'both', length: float = 1, width: float = 0.5,
                          rotation: float = 0, pad: float = 0):
        """
        Configures the x-axis ticks.

        Args:
            which (str): The ticks to configure. Possible values: 'major', 'minor', or 'both' (default: 'both').
            length (float): The length of the ticks in points (default: 1).
            width (float): The width of the ticks in points (default: 0.5).
            rotation (float): The rotation angle of the tick labels in degrees (default: 0).
            pad (float): The padding between the ticks and the tick labels in points (default: 0).
            pad (float): The padding between the ticks and the tick labels in points (default: 0).
        """
        self.ax.tick_params(axis='x', which=which, length=length, width=width, rotation=rotation, pad=pad)

    def configure_y_axis(self, axis_index: int, label: str = None, y_lim: Tuple[int, int] = None,
                         minor_formatter: Formatter = None,
                         major_formatter: Formatter = None,
                         minor_locator: Locator = None,
                         major_locator: Locator = None,
                         invert_axis: bool = False
                         ):
        """
        Configures a y-axis with a label and color.

        Args:
            axis_index (int): The index of the y-axis to configure.
            label (str): The label for the y-axis.
            y_lim (tuple): The limits for the axis.
            minor_formatter (Formatter): The minor formatter for the y-axis (default: None)
            major_formatter (Formatter): The major formatter for the y-axis (default: None)
            minor_locator (Locator): The minor locator for the y-axis (default: AutoLocator)
            major_locator (Locator): The major locator for the y-axis (default: AutoLocator)
            invert_axis (bool): Whether to invert the y-axis (default: False)

        Raises:
            IndexError: If the axis index is out of range.
        """
        if axis_index >= self.num_y_axes:
            raise IndexError("Axis index out of range")

        if label is not None:
            self.y_labels[axis_index] = label

        if y_lim is not None:
            self.y_lims[axis_index] = y_lim

        ax = self.y_axes[axis_index]

        if invert_axis:
            ax.invert_yaxis()
            self.y_labels[axis_index] = f'{label} (reversed axis)'

        if minor_formatter is not None:
            ax.yaxis.set_minor_formatter(minor_formatter)

        if major_formatter is not None:
            ax.yaxis.set_major_formatter(major_formatter)

        if minor_locator is not None:
            ax.yaxis.set_minor_locator(minor_locator)

        if major_locator is not None:
            ax.yaxis.set_major_locator(major_locator)

    def configure_y_ticks(self, axis_index: int, which: str = 'both', length: float = 1,
                          width: float = 0.5, rotation: float = 0, pad: float = 0):
        """
        Configures the y-axis ticks.

        Args:
            axis_index (int): The index of the y-axis to configure.
            which (str): The ticks to configure. Possible values: 'major', 'minor', or 'both' (default: 'both').
            length (float): The length of the ticks in points (default: 1).
            width (float): The width of the ticks in points (default: 0.5).
            rotation (float): The rotation angle of the tick labels in degrees (default: 0).
            pad (float): The padding between the ticks and the tick labels in points (default: 0).

        Raises:
            IndexError: If the axis index is out of range.
        """
        if axis_index == 0:
            self.ax.tick_params(axis='y', which=which, length=length,
                                width=width, rotation=rotation, pad=pad)
        else:
            if axis_index >= self.num_y_axes:
                raise IndexError("Axis index out of range")
            ax = self.y_axes[axis_index]
            ax.tick_params(axis='y', which=which, length=length,
                                width=width, rotation=rotation, pad=pad)

    def add_horizontal_line(self, axis_index: int = 0, y: float = 0):
        """
        Adds a dotted zero line to the chart.

        Args:
            axis_index (int): The index of the y-axis on which to add the zero line (default: 0).
            y (float): The value for y-axis (default: 0).

        Raises:
            IndexError: If the axis index is out of range.
        """
        if axis_index == 0:
            self.ax.axhline(y, linestyle='dotted', color='black', linewidth=1)
        else:
            if axis_index >= self.num_y_axes:
                raise IndexError("Axis index out of range")
            ax = self.y_axes[axis_index]
            ax.axhline(y, linestyle='dotted', color='black', linewidth=1)

    def add_vertical_line(self, x, y, beat: float = 1, label: str = None):
        """
        Adds a vertical line to the chart for specific values in the y-axis.

        Args:
            x: The x-values of the data.
            y: The y-values of the data.
            beat (float): The specific value in the y-axis to mark with a vertical line (default: 1).
            label (str): The title for the vertical line in the legend (default: None).
        """
        if label is not None:
            self.handles.append(plt.Rectangle((0, 0), 1, 1, fc='grey', alpha=0.3, label=label))

        for i, value in enumerate(y):
            if value == beat:
                self.ax.axvspan(x[i], x[i + 1], facecolor='grey', alpha=0.3)

    def legend(self, loc: str = 'upper center', bbox_to_anchor: Tuple[float, float] = (0.5, -0.1), ncol: int = 1,
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
        legend = self.ax.legend(handles=self.handles, loc=loc, bbox_to_anchor=bbox_to_anchor, ncol=ncol,
                                frameon=frameon, **kwargs)
        self.legend_y = self.ax.transAxes.inverted().transform([(0, legend.get_window_extent().y0)])[0][1]

    def __apply_configuration(self):
        """
        Applies the y-axis configuration and styling to the chart.
        """
        self.ax.set_ylabel(self.y_labels[0])

        if self.y_lims[0] is not None:
            self.ax.set_ylim(self.y_lims[0])

        for i in range(1, self.num_y_axes):
            twin_ax = self.y_axes[i]

            if self.y_lims[i] is not None:
                twin_ax.set_ylim(self.y_lims[i])

            twin_ax.set_ylabel(self.y_labels[i])

        x_min = min(self.x_min)
        x_max = max(self.x_max)

        self.ax.set_xlim(x_min, x_max)

    @abstractmethod
    def add_data(self, *args, **kwargs):
        """
        Abstract method to add data to the chart.
        Implement this method in each child class to define how data and handles are added to the chart.
        """
        pass

    def __add_bottom_label(self):
        """
        Adds a centered label at the bottom of the chart.
        """

        self.ax.text(0, self.legend_y - 0.08, f'Source: Bloomberg & Federal Reserve Economic Data (FRED) '
                                              f'as of {datetime.datetime.today().strftime("%d.%m.%Y")}',
                     transform=self.ax.transAxes, ha='left', va='bottom', **source_text_style)

    def plot(self, path: str) -> None:
        """
        Plots the chart and saves it as png.3

        Args:
            path (str): the path to save the file to.
        """
        self.__apply_configuration()
        plt.title(self.title, fontdict=title_style)
        self.__add_bottom_label()
        plt.tight_layout()
        plt.savefig(path, dpi=600)
        plt.close()
