from matplotlib.ticker import MultipleLocator

from charting.charts.time_series_chart import TimeSeriesChart
import matplotlib.dates as mdates
from examples import fred, blp

if __name__ == '__main__':
    d1, t1 = blp.get_series(series_id='BCOMEUTR Index', observation_start="20170101")

    chart = TimeSeriesChart(title="Rohstoff Index", num_y_axes=1)

    chart.configure_y_axis(axis_index=0, label="EUR", minor_locator=MultipleLocator(20), major_locator=MultipleLocator(40))

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=3)

    major_formatter = mdates.DateFormatter("%Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_data(x=d1.index, y=d1['y'], label=t1, y_axis=0)
    chart.legend(frameon=False, ncol=1)

    chart.plot(path="comdty_index.png")
