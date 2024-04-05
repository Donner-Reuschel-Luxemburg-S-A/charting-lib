import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main():
    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='GRCPXEEY Index', observation_start='20180101')
    d2, t2 = blp.get_series(series_id='GRCP20YY Index', observation_start='20180101')

    title = "Germany CPI & CPI excl. Food & Energy"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="de_cpi_corecpi.png")

    chart.configure_y_axis(label="Percentage Points", y_lim=(-1, 9), minor_locator=MultipleLocator(.5),
                           major_locator=MultipleLocator(1))


    minor_locator = mdates.MonthLocator(interval=6)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d2.index, y=d2['y'], label="Germany CPI")
    chart.add_series(x=d1.index, y=d1['y'], label="Germany CPI excl. Food & Energy")

    chart.add_horizontal_line()
    chart.add_last_value_badge()
    chart.legend(ncol=1)
    chart.plot()


if __name__ == '__main__':
    main()
