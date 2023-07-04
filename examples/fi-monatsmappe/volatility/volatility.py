
import matplotlib.dates as mdates

from charting.model.chart import Chart
from examples import fred, blp

if __name__ == '__main__':
    d1, t1 = fred.get_series(series_id='VIXCLS', observation_start="2022-01-01")
    d2, t2 = blp.get_series(series_id='V2X Index', observation_start="20220101")

    chart = Chart(title="Volatilitätsmärkte")

    chart.configure_y_axis(y_axis_index=0, label="%", y_lim=(10, 50))

    major_locator = mdates.MonthLocator(interval=3)
    minor_locator = mdates.MonthLocator(interval=1)

    major_formatter = mdates.DateFormatter("%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label="Implizite Volatilität S&P 500")
    chart.add_series(x=d2.index, y=d2['y'], label="Implizite Volatilität Eurostoxx 50")

    chart.legend(ncol=2)

    chart.plot(path="vix_v2x.png")

    ###

    d1, t1 = blp.get_series(series_id='MOVE Index', observation_start="20220101")

    chart = Chart(title="Implizite Volatilität US Staatsanleihen")

    chart.configure_y_axis(y_axis_index=0, label="%", y_lim=(50, 210))

    major_locator = mdates.MonthLocator(interval=3)
    minor_locator = mdates.MonthLocator(interval=1)

    major_formatter = mdates.DateFormatter("%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1)

    chart.legend(ncol=2)

    chart.plot(path="move.png")
