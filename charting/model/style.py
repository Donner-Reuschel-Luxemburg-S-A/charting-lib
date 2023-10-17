"""
Style Guide for D&R Charting Lib.
"""
colors = ["#7EC0C6", "#124877", "#E91457", "#018C7D", "#6F3E2E", "#FD7200"]
stacked_colors = ["#7A7978", "#87CBAC", "#90FFDC", "#8DE4FF", "#8AC4FF"]
source_text_style = {'fontsize': 7}
legend_style = {'size': 8}
title_style = {'size': 10, 'weight': 'bold'}


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
    if y_axis >= len(colors):
        y_axis = y_axis % len(colors)
    return colors[y_axis]
