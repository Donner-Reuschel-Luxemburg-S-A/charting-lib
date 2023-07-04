from matplotlib.ticker import MultipleLocator

from charting.model.chart import Chart
from examples import fred
import matplotlib.dates as mdates

if __name__ == '__main__':
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR')

    chart = Chart(title="Demo", num_rows=3, num_y_axis=[1, 2, 1])

    minor_locator = MultipleLocator(1)
    major_locator = MultipleLocator(5)
    chart.configure_y_axis(row_index=1, y_axis_index=1, label="%", y_lim=(0, 35),
                           minor_locator=minor_locator, major_locator=major_locator)

    major_locator = mdates.YearLocator(base=5)
    minor_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.AutoDateFormatter(major_locator)

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator,
                           major_locator=major_locator)

    chart.add_horizontal_line(row_index=2, y_axis_index=0, y=0.5)
    chart.add_vertical_line(x=d2.index, y=d2["y"], row_index=2, label="US Recession")

    chart.legend()
    chart.plot("output/demo.png")
