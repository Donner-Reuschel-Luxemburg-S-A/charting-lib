"""
Style Guide for D&R Charting Lib.
"""
colors = ["#124877", '#7fbd39', "#018c7d", "#74c0c5", "#6f99ed", "#b2b2b1"]
stacked_colors = ["#1B6CB3", '#96CD58', "#01D1BC", "#8CCBCF", "#88ABF0", "#C1C1C0"]
source_text_style = {'fontsize': 6}
legend_style = {'size': 8}
title_style = {'fontsize': 10, 'fontweight': 'bold'}
color_counter = 0
suggested_alpha = 1


def get_stacked_color(idx: int):
    if idx >= len(stacked_colors):
        idx = idx % len(stacked_colors)
    return stacked_colors[idx]


def get_color(y_axis: int):
    """
    Returns the color for a specific y-axis index.

    If the index is greater than or equal to the number of colors in the list,
    the index wraps around to the beginning of the list.

    Args:
        y_axis (int): The index of the y-axis.

    Returns:
        str: The color corresponding to the index.
    """
    global color_counter, suggested_alpha
    color_counter += 1
    if y_axis >= len(colors):
        suggested_alpha = 1 - int(color_counter/y_axis)*.1
        y_axis = y_axis % len(colors)

    return colors[y_axis], suggested_alpha
