from matplotlib.ticker import MultipleLocator

from charting.charts.time_series_chart import TimeSeriesChart
import matplotlib.dates as mdates
from examples import fred, blp

if __name__ == '__main__':
    d1, t1 = blp.get_series(series_id='CLA Comdty', observation_start="20200101")
    d2, t2 = blp.get_series(series_id='COA Comdty', observation_start="20200101")

    chart = TimeSeriesChart(title="Rohstoffmärkte", num_y_axes=1)

    chart.configure_y_axis(axis_index=0, label="USD", minor_locator=MultipleLocator(5))

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=1)

    major_formatter = mdates.DateFormatter("%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_data(x=d1.index, y=d1['y'], label="WTI Rohöl", y_axis=0)
    chart.add_data(x=d2.index, y=d2['y'], label="Brent Rohöl", y_axis=0)

    chart.legend(frameon=False, ncol=2)

    chart.plot(path="oil.png")
