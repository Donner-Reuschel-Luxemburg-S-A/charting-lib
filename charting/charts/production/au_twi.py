import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()
    df, t = blp.get_series(series_id='TWI ADSP Index', observation_start='20170101')

    title = "AUD Trade Weighted Index Spot"

    metadata = Metadata(title=title, region=Region.AU, category=Category.FX)

    chart = Chart(title=title, metadata=metadata, filename="au_twi.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(4))

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df.index, y=df['y'], label=t)

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
