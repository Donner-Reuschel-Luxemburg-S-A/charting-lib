
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.sdmx_source import Ecb

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata


def main():
    blp = BloombergSource()

    fed, _ = blp.get_series(series_id='CERBTTAL Index', observation_start='20000101')
    ecb, _ = blp.get_series(series_id='EBBSTOTA Index', observation_start='20000101')
    boj, _ = blp.get_series(series_id='BJACTOTL Index', observation_start='20000101')

    fed['y'] = (fed['y']/fed['y'][0]) * 100
    ecb['y'] = (ecb['y'] / ecb['y'][0]) * 100
    boj['y'] = (boj['y'] / boj['y'][0]) * 100

    title = "Total Assets - Central Banks"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.CB)

    chart = Chart(title=title, metadata=metadata, filename="global_central_banks.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", major_locator=MultipleLocator(200),
                           minor_locator=MultipleLocator(100))

    major_locator = mdates.YearLocator(base=2)
    minor_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.AutoDateFormatter(major_locator)
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=fed.index, y=fed['y'], label="FED")
    chart.add_series(x=ecb.index, y=ecb['y'], label="ECB")
    chart.add_series(x=boj.index, y=boj['y'], label="BOJ")

    chart.legend(ncol=3)
    chart.plot()


if __name__ == '__main__':
    main()

