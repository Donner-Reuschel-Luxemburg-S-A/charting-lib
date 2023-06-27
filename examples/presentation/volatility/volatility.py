from charting.charts.time_series_chart import TimeSeriesChart
import matplotlib.dates as mdates
from examples import fred, blp

if __name__ == '__main__':
    d1, t1 = fred.get_series(series_id='VIXCLS', observation_start="2022-06-01")

    chart = TimeSeriesChart(title="Volatilitätsmärkte", num_y_axes=1)

    chart.configure_y_axis(axis_index=0, label="%", y_lim=(10, 50))

    major_locator = mdates.MonthLocator(interval=3)
    minor_locator = mdates.MonthLocator(interval=1)

    major_formatter = mdates.DateFormatter("%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_data(x=d1.index, y=d1['y'], label=t1, y_axis=0)

    chart.legend(frameon=False, ncol=1)

    chart.plot(path="vix_v2x.png")
