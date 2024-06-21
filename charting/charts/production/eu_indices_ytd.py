import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.ytd import Ytd


def main():
    blp = BloombergSource()

    df2, t2 = blp.get_series(series_id='sxxp Index', observation_start="20230101", field="px_close_1d")
    df3, t3 = blp.get_series(series_id='mcxp Index', observation_start="20230101", field="px_close_1d")
    df4, t4 = blp.get_series(series_id='scxp Index', observation_start="20230101", field="px_close_1d")

    title = "European Indices YTD"

    metadata = Metadata(title=title, category=Category.EQUITY, region=Region.EU)
    chart = Chart(title=title, filename="eu_indices_ytd.png", metadata=metadata)

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(5))

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=2)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Ytd())
    chart.add_series(x=df3.index, y=df3['y'], label=t3, transformer=Ytd())
    chart.add_series(x=df4.index, y=df4['y'], label=t4, transformer=Ytd())
    chart.add_horizontal_line()
    chart.add_last_value_badge()

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
