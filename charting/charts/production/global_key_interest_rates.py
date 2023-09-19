from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
import matplotlib.dates as mdates


def main():
    blp = BloombergSource()

    d1, t1 = blp.get_series(series_id='UKBRBASE Index', observation_start="19990101")
    d2, t2 = blp.get_series(series_id='RBATCTR Index', observation_start="19990101")
    d3, t3 = blp.get_series(series_id='NOBRDEPA Index', observation_start="19990101")
    d4, t4 = blp.get_series(series_id='SWRRATEI Index', observation_start="19990101")
    d5, t5 = blp.get_series(series_id='FDTR Index', observation_start="19990101")
    d6, t6 = blp.get_series(series_id='EUORDEPO Index', observation_start="19990101")
    d7, t7 = blp.get_series(series_id='CABROVER Index', observation_start="19990101")

    title = "Central Banks - Key Interest Rates"

    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.RATES)

    chart = Chart(title=title, metadata=metadata, filename="global_key_interest_rates.png")

    chart.configure_y_axis(y_axis_index=0, label="%", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(.25))

    minor_locator = mdates.YearLocator(base=4)
    major_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.DateFormatter("%Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1["y"], label="United Kingdom")
    chart.add_series(x=d2.index, y=d2["y"], label="Australia")
    chart.add_series(x=d3.index, y=d3["y"], label="Norway")
    chart.add_series(x=d4.index, y=d4["y"], label="Sweden")
    chart.add_series(x=d5.index, y=d5["y"], label="United States")
    chart.add_series(x=d6.index, y=d6["y"], label="Eurozone")
    chart.add_series(x=d7.index, y=d7["y"], label="Canada")

    chart.legend(ncol=3)
    chart.plot()


if __name__ == '__main__':
    main()
