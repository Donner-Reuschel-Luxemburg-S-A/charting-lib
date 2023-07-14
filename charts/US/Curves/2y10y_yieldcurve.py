from pandas import DateOffset

import matplotlib.dates as mdates

from charting.model.chart import Chart
from charting import fred, blp
from charting.model.metadata import Metadata, Country, Category

if __name__ == '__main__':
    d1, t1 = blp.get_series(series_id='USYC2Y10 Index', observation_start="20220131")

    title = "10 Year - 2 Year Treasury Yield Spread"
    metadata = Metadata(title=title, country=Country.US, category=Category.CURVES)
    chart = Chart(title=title, metadata=metadata, filename="us_2y10y_curve.png")

    chart.configure_y_axis(y_axis_index=0, label="BPS")

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=4)
    major_formatter = mdates.DateFormatter("%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=title)
    chart.add_horizontal_line()

    chart.legend()
    chart.plot()
