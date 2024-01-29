import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

def main():
    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='LECPOAS Index', observation_start="20140101")

    title = "EUR Investment Grade Corporate Bond Spreads"

    metadata = Metadata(title=title, region=Region.EU, category=Category.FI)
    chart = Chart(title=title, filename="eu_ig_credit_spread.png", metadata=metadata)

    chart.configure_y_axis(y_axis_index=0, label="Spread (BPS)", minor_locator=MultipleLocator(10),
                           major_locator=MultipleLocator(50))

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=2)
    major_formatter = mdates.DateFormatter("%y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1)
    chart.add_series(x=df1.index, y=df1['y'].mean(), label="Avg", linestyle="--")

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
