
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.sdmx_source import Ecb

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata


def main():
    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='QX83X Index', observation_start='20220101')
    df2, t2 = blp.get_series(series_id='QX3A Index', observation_start='20220101')
    df3, t3 = blp.get_series(series_id='QW5A Index', observation_start='20220101')
    df4, t4 = blp.get_series(series_id='LBEATREU Index', observation_start='20220101')

    df1['y'] = (df1['y'] / df1['y'][0]) * 100
    df2['y'] = (df2['y'] / df2['y'][0]) * 100
    df3['y'] = (df3['y'] / df3['y'][0]) * 100
    df4['y'] = (df4['y'] / df4['y'][0]) * 100

    title = "European Interest Rate Markets"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)

    chart = Chart(title=title, metadata=metadata, filename="eu_rates_performance.png")

    chart.configure_y_axis(y_axis_index=0, label="Index")

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=1)
    major_formatter = mdates.DateFormatter("%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1)
    chart.add_series(x=df2.index, y=df2['y'], label=t2)
    chart.add_series(x=df3.index, y=df3['y'], label=t3)
    chart.add_series(x=df4.index, y=df4['y'], label=t4)

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()

