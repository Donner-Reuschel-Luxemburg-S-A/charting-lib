import matplotlib.dates as mdates
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.transformer.avg import Avg

if __name__ == '__main__':
    fred = FredSource()
    blp = BloombergSource()

    d1, t1 = blp.get_series(series_id='BNKRINDX Index', observation_start="20060101")
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR', observation_start="2006-01-01")

    chart = Chart(title="Bankruptcy filings moving up in recent weeks", num_y_axis=2, filename="bankruptcy.png")

    chart.configure_y_axis(y_axis_index=0, label="Count")
    chart.configure_y_axis(y_axis_index=1, label="Count")

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=2)
    major_formatter = mdates.DateFormatter("%Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label="Bankruptcy filings", y_axis_index=0,
                     transformer=Avg(offset=DateOffset(months=1)))
    chart.add_series(x=d1.index, y=d1['y'], label="Bankruptcy filings", y_axis_index=1,
                     transformer=Avg(offset=DateOffset(months=3)))
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")

    chart.legend(ncol=2)
    chart.plot()
