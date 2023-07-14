from pandas import DateOffset

import matplotlib.dates as mdates

from charting.model.chart import Chart
from charting import fred, blp
from charting.model.metadata import Metadata, Category, Country

if __name__ == '__main__':
    df1, t1 = blp.get_series(series_id='USBMMY3M Index', observation_start="20220131")
    df2, t2 = blp.get_series(series_id='USGG10YR Index', observation_start="20220131")

    df2['spread'] = df2['y'] - df1['y']

    title = "10 Year - 3 Month Treasury Yield Spread"
    metadata = Metadata(title=title, country=Country.US, category=Category.CURVES)
    chart = Chart(title=title, metadata=metadata, filename="us_3m10y_curve.png")

    chart.configure_y_axis(y_axis_index=0, label="%")

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=4)
    major_formatter = mdates.DateFormatter("%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df2.index, y=df2['spread'], label=title)
    chart.add_horizontal_line()

    chart.legend()
    chart.plot()
