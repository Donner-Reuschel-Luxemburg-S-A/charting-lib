class InvalidAxisConfigurationException(Exception):
    def __init__(self, num_rows: int, num_y_axis: int):
        message = f"Number of y-axis with length '{num_y_axis}' for rows does not match number " \
                  f"of rows with length '{num_rows}' in the plot."
        super().__init__(message)


class YAxisIndexException(Exception):
    def __init__(self, row_index: int, y_axis_index: int):
        message = f"Either row {row_index} does not exists or does not have {y_axis_index} y-axes!"
        super().__init__(message)
