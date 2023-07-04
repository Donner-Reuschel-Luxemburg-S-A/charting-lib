from matplotlib.ticker import MultipleLocator

import matplotlib.dates as mdates

from charting.model.chart import Chart
from examples import fred, blp

if __name__ == '__main__':
    d1, t1 = blp.get_series(series_id='CLA Comdty', observation_start="20200101")
    d2, t2 = blp.get_series(series_id='COA Comdty', observation_start="20200101")

    chart = Chart(title="Rohstoffmärkte")

    chart.configure_y_axis(y_axis_index=0, label="USD", minor_locator=MultipleLocator(5))

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=3)

    major_formatter = mdates.DateFormatter("%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label="WTI Rohöl")
    chart.add_series(x=d2.index, y=d2['y'], label="Brent Rohöl")

    chart.legend(ncol=2)
    chart.plot(path="oil.png")
