
import matplotlib.dates as mdates

from charting.model.chart import Chart
from examples import blp

if __name__ == '__main__':
    d1, t1 = blp.get_series(series_id='XAG Curncy', observation_start="20170101")

    chart = Chart(title="Silber")

    chart.configure_y_axis(y_axis_index=0, label="USD")

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=3)

    major_formatter = mdates.DateFormatter("%Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.legend()

    chart.plot(path="silver.png")
