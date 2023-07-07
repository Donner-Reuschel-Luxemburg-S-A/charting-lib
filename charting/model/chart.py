import base64
import getpass
import io
import os
from datetime import datetime, timedelta
from enum import Enum
from functools import reduce
from typing import Tuple, Union, List, Dict

import numpy as np
import pandas as pd
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.dates import num2date
from matplotlib.ticker import Formatter, Locator

from charting.exception import InvalidAxisConfigurationException, YAxisIndexException
from charting.model.metadata import Metadata
from charting.model.style import title_style, source_text_style, get_color, get_stacked_color
import matplotlib.offsetbox as offsetbox

from charting.model.transformer import Transformer


class Chart:

    def __init__(self,
                 path: str,
                 title: str = "",
                 num_rows: int = 1,
                 num_y_axis: Union[int, List[int]] = 1,
                 figsize: Tuple[float, float] = (8.06, 5.05),
                 metadata: Union[Metadata, None] = None,
                 ):
        """
        Initializes a Chart object.

        Args:
            path (str): the path to save the file to.
            title (str): The title of the chart (default: "").
            num_y_axis (int, List[int]): The number of y-axes for the chart. If num_rows is > 1, you also can
                define a list of int, defining the number of y-axis per row. If num_rows > 1 and num_y_axis a
                single int, each row will get specified number of y-axis. (default: 1).
            figsize (tuple): The figure size of the chart (default: (12, 8)).
            metadata (Metadata, None): the metadata to add to the image (default: None).
        """
        self.path = path
        self.title = title
        self.num_rows = num_rows
        self.num_y_axis = num_y_axis
        self.figsize = figsize
        self.metadata = metadata

        self.fig, self.axis = plt.subplots(self.num_rows, 1, figsize=figsize, constrained_layout=True, sharex=True)

        if isinstance(self.axis, Axes):
            self.axis = [self.axis]

        self.__remove_top_spines()
        self.axis_dict = self.__init_y_axis()
        self.handles = []
        self.x_min = []
        self.x_max = []

    def __remove_top_spines(self) -> None:
        """
        Sets the visibility of the top spines of each axis to False.
        """
        for ax in self.axis:
            ax.spines.top.set_visible(False)

    def __init_y_axis(self) -> Dict[int, List[Axes]]:
        """
        Initializes the y-axes configuration based on the provided parameters and returns a dictionary
        mapping each axis index to a list of corresponding y-axes.

        Raises:
            InvalidAxisConfigurationException: If the number of y-axes specified for each row is not
            compatible with the number of rows.

        Returns:
            dict[int, List[Axes]]: A dictionary mapping each axis index to a list of corresponding y-axes.
        """
        if isinstance(self.num_y_axis, List) and len(self.num_y_axis) != self.num_rows:
            raise InvalidAxisConfigurationException(num_rows=self.num_rows, num_y_axis=len(self.num_y_axis))

        axis_dict = {}

        for i, ax in enumerate(self.axis):
            num = self.num_y_axis[i] if isinstance(self.num_y_axis, List) else self.num_y_axis

            axis_list = [ax] + [ax.twinx() for _ in range(1, num)]
            positions = [(1 + (j - 1) * 0.1) for j in range(1, num)]

            for twin_ax, position in zip(axis_list[1:], positions):
                twin_ax.spines.right.set_position(("axes", position))
                twin_ax.spines.top.set_visible(False)

            axis_dict[i] = axis_list

        return axis_dict

    def configure_x_axis(self, label: str = None,
                         minor_formatter: Formatter = None,
                         major_formatter: Formatter = None,
                         minor_locator: Locator = None,
                         major_locator: Locator = None):
        """
        Configures the x-axis with label, formatter and locator.

        Args:
            label (str): The label for the x-axis (default: None).
            minor_formatter (Formatter): The minor formatter for the x-axis (default: None)
            major_formatter (Formatter): The major formatter for the x-axis (default: None)
            minor_locator (Locator): The minor locator for the x-axis (default: None)
            major_locator (Locator): The major locator for the x-axis (default: None)
        """
        ax = self.axis_dict[next(reversed(self.axis_dict))][0]

        ax.set_xlabel(label)

        if minor_formatter is not None:
            ax.xaxis.set_minor_formatter(minor_formatter)

        if major_formatter is not None:
            ax.xaxis.set_major_formatter(major_formatter)

        if minor_locator is not None:
            ax.xaxis.set_minor_locator(minor_locator)

        if major_locator is not None:
            ax.xaxis.set_major_locator(major_locator)

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
        ax = self.axis_dict[next(reversed(self.axis_dict))][0]
        ax.tick_params(axis='x', which=which, length=length, width=width, rotation=rotation, pad=pad)

    def configure_y_axis(self, row_index: int = 0, y_axis_index: int = 0, label: str = None,
                         y_lim: Tuple[float, float] = None,
                         minor_formatter: Formatter = None,
                         major_formatter: Formatter = None,
                         minor_locator: Locator = None,
                         major_locator: Locator = None,
                         invert_axis: bool = False):
        """
        Configures a y-axis with a label and color.

        Args:
            row_index (int): The index of the row to plot the line (default: 0).
            y_axis_index (int): The index of the y-axis to configure (default: 0).
            label (str): The label for the y-axis.
            y_lim (tuple): The limits for the axis.
            minor_formatter (Formatter): The minor formatter for the y-axis (default: None)
            major_formatter (Formatter): The major formatter for the y-axis (default: None)
            minor_locator (Locator): The minor locator for the y-axis (default: AutoLocator)
            major_locator (Locator): The major locator for the y-axis (default: AutoLocator)
            invert_axis (bool): Whether to invert the y-axis (default: False)

        Raises:
            YAxisIndexException: If the provided row or y-axis index is invalid.
        """

        try:
            ax = self.axis_dict[row_index][y_axis_index]
            ax.set_ylabel(label)

            if invert_axis:
                ax.invert_yaxis()
                ax.set_ylabel(f'{label} (reversed axis)')

            if y_lim is not None:
                ax.set_ylim(*y_lim)

            if minor_formatter is not None:
                ax.yaxis.set_minor_formatter(minor_formatter)

            if major_formatter is not None:
                ax.yaxis.set_major_formatter(major_formatter)

            if minor_locator is not None:
                ax.yaxis.set_minor_locator(minor_locator)

            if major_locator is not None:
                ax.yaxis.set_major_locator(major_locator)

        except IndexError:
            raise YAxisIndexException(row_index=row_index, y_axis_index=y_axis_index)

    def add_series(self, x, y, label: str, row_index: int = 0, y_axis_index: int = 0, chart_type: str = 'line',
                   linestyle: str = '-', linewidth: float = 1, fill: bool = False, fill_threshold: float = None,
                   bar_bottom: float = 0, stacked: bool = False, alpha: float = 1,
                   transformer: Union[Transformer, List[Transformer]] = None):
        """
        Adds a series to the chart.

        Args:
            x: The x-values of the series.
            y: The y-values of the series.
            label (str): The label for the series.
            row_index (int): The index of the row to plot the data (default: 0).
            y_axis_index (int): The index of the y-axis to plot the series on (default: 0).
            chart_type (str): The type of chart to plot ('line' or 'bar', default: 'line').
            linestyle (str): The line style of the series (default: '-').
            linewidth (float): The width of the line (default: 1)
            fill (bool): True if area between x and y should be filled (default: False).
            fill_threshold (float): The threshold value to fill the area below (default: None).
                               If not specified, the area will be filled from the line to the bottom axis.
            bar_bottom (float): The bottom for bar charts to plot (default: 0).
            stacked (bool): Indicates if the bar should be stacked (default: False).
            alpha (float): The alpha value for the data plot (default: 1).
            transformer (Union[Transformer, List[Transformer]]): Optional transformer(s) to apply to the series
                (default: None). If a single transformer is provided, it will be applied to the series.
                If a list of transformers is provided, they will be applied sequentially to the series.
                Each transformer should implement the `transform` method to modify the series.
                The label of the series will be updated to reflect the applied transformers.
        """
        color = get_color(y_axis=len(self.handles))
        axis_label = 'L1' if y_axis_index == 0 else f'R{y_axis_index}'

        try:
            ax = self.axis_dict[row_index][y_axis_index]
        except IndexError:
            raise YAxisIndexException(row_index=row_index, y_axis_index=y_axis_index)

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
            handle, = ax.plot(x, y, color=color, linestyle=linestyle, linewidth=linewidth, label=label, alpha=alpha)

            if fill:
                if fill_threshold is None:
                    fill_threshold = ax.get_ylim()[0]
                ax.fill_between(x, y, fill_threshold, color=color, alpha=0.1)

        elif chart_type == 'bar':
            get_bar_width = lambda idx: (x[idx + 1] - x[idx]).days * 0.8 if idx < len(x) - 1 else None
            bar_widths = [get_bar_width(i) for i in range(len(x) - 1)]
            mean_bar_width = np.mean(bar_widths)

            if stacked:
                if len(ax.patches) == len(x):
                    bar_bottom = [0 if (y_val > 0 > patch.get_height()) or (y_val < 0 < patch.get_height())
                                  else patch.get_height() for y_val, patch in zip(y, ax.patches)]
                    color = get_stacked_color(1)
                elif len(ax.patches) > len(x):
                    bar_bottom = []
                    n = len(ax.patches) // len(x)
                    color = get_stacked_color(n+1)
                    all_patches = []
                    for i in range(n):
                        start = i * len(x)
                        end = (i + 1) * len(x)
                        p = ax.patches[start:end]
                        all_patches.append(p)

                    for idx, patches in enumerate(zip(*all_patches)):
                        bottom = 0
                        if y[idx] > 0:
                            bottom = sum([patch.get_height() for patch in patches if np.sign(patch.get_height()) == 1])
                        if y[idx] < 0:
                            bottom = sum([patch.get_height() for patch in patches if np.sign(patch.get_height()) == -1])

                        bar_bottom.append(bottom)
                else:
                    bar_bottom = np.zeros(len(x))
                    color = get_stacked_color(0)

            handle = ax.bar(x, y, align='center', width=mean_bar_width, bottom=bar_bottom,
                            label=label, color=color, alpha=alpha)
        else:
            raise NotImplemented(f"Chart type '{chart_type} is not implemented yet!")

        x_min = min(x)
        x_max = max(x)

        if chart_type == 'bar':
            x_min = x_min - timedelta(days=mean_bar_width / 2)
            x_max = x_max + timedelta(days=mean_bar_width / 2)

        self.handles.append(handle)
        self.x_min.append(x_min)
        self.x_max.append(x_max)

    def add_horizontal_line(self, row_index: int = 0, y_axis_index: int = 0, y: float = 0) -> None:
        """
        Adds a dotted zero line to the chart.

        Args:
            row_index (int): The index of the row to plot the line (default: 0).
            y_axis_index (int): The index of the y-axis on which to add the zero line (default: 0).
            y (float): The y-coordinate value for the zero line (default: 0).

        Raises:
            YAxisIndexException: If the provided row or y-axis index is invalid.
        """
        try:
            self.axis_dict[row_index][y_axis_index].axhline(y, linestyle='dotted', color='black', linewidth=1)
        except IndexError:
            raise YAxisIndexException(row_index=row_index, y_axis_index=y_axis_index)

    def add_vertical_line(self, x, y, row_index: Union[int, List[int]] = 0, beat: float = 1, label: str = None):
        """
        Adds a vertical line to the chart for specific values in the y-axis.

        Args:
            x: The x-values of the data.
            y: The y-values of the data.
            row_index (int, List[int): The index of the row to plot the line (default: 0).
            beat (float): The specific value in the y-axis to mark with a vertical line (default: 1).
            label (str): The title for the vertical line in the legend (default: None).
        """
        if isinstance(row_index, int):
            row_index = [row_index]

        for row in row_index:
            try:
                ax = self.axis_dict[row][0]
            except IndexError:
                raise YAxisIndexException(row_index=row, y_axis_index=0)

            for i, value in enumerate(y):
                if value == beat:
                    ax.axvspan(x[i], x[i + 1], facecolor='grey', alpha=0.3)

        if label is not None:
            handle = plt.Rectangle((0, 0), 1, 1, fc='grey', alpha=0.3, label=label)
            self.handles.append(handle)

    def __add_bottom_label(self):
        """
        Adds a centered label at the bottom of the chart.
        """
        ax = self.axis_dict[next(reversed(self.axis_dict))][0]
        x_min = min(self.x_min)
        x_max = max(self.x_max)
        ax.set_xlim(x_min, x_max)

        label = f'Source: Bloomberg & Federal Reserve Economic Data (FRED) as of ' \
                f'{datetime.today().strftime("%d.%m.%Y")}, Time Series from ' \
                f'{x_min.strftime("%m/%Y")} - {x_max.strftime("%m/%Y")}.'

        txt = offsetbox.TextArea(label, textprops=source_text_style)

        if ax.get_legend() is not None:
            box = ax.get_legend()._legend_box
            box.get_children().append(txt)
            box.set_figure(box.figure)
        else:
            ax.annotate(label, xy=(0.5, -0.4), xycoords='axes fraction', ha='center', va='center', **source_text_style)

    def legend(self, ncol: int = 1):
        """
        Configures the legend for the chart.

        Args:
            ncol (int): The number of columns in the legend (default: 1).
        """
        ax = self.axis_dict[next(reversed(self.axis_dict))][0]
        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, 0),
            borderaxespad=3,
            handles=self.handles,
            frameon=False,
            ncol=ncol
        )

    def add_sup_y_label(self, label: str):
        """
        Adds a super ylabel to the figure.

        Args:
            label (str): The label text to be added as the super ylabel.
        """
        self.fig.supylabel(label, fontsize=8)

    def __tag_image(self) -> None:
        """
        Tags the image with metadata.
        """
        target_image = Image.open("temp.png")

        data = PngInfo()

        if self.metadata is not None:
            for key, value in self.metadata:
                data.add_text(key, value.value if isinstance(value, Enum) else value)

        target_image.save(self.path, pnginfo=data)
        os.remove("temp.png")

    def base64(self) -> str:
        image = Image.open(self.path)
        byte_stream = io.BytesIO()
        image.save(byte_stream, format="PNG")
        byte_stream.seek(0)
        byte_stream_value = byte_stream.getvalue()
        return base64.b64encode(byte_stream_value).decode("utf-8")

    def plot(self) -> None:
        """
        Plots the chart and saves it as png.
        """
        plt.suptitle(self.title, fontdict=title_style)
        self.__add_bottom_label()
        plt.savefig("temp.png", transparent=True)
        plt.close()
        self.__tag_image()


