import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata
from charting.transformer.lag import Lag
from charting import blp

if __name__ == '__main__':
    df1, t1 = blp.get_series(series_id='GEIFSGPE Index', observation_start='20180701')
    df2, t2 = blp.get_series(series_id='GRCP2HYY Index', observation_start='20190101')

    title = "IFO Price Expectations & Inflation"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, num_y_axis=2, metadata=metadata, filename="de_ifo_hicp.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(5), major_locator=MultipleLocator(10))
    chart.configure_y_axis(y_axis_index=1, label="%", minor_locator=MultipleLocator(0.5), major_locator=MultipleLocator(1))

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=3)
    major_formatter = mdates.DateFormatter("%b-%Y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0)
    chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=1, transformer=Lag(offset=DateOffset(months=6)))

    chart.legend(ncol=2)
    chart.plot()

