import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main():
    fred = FredSource()
    d1, t1 = fred.get_series(series_id='TEMPHELPS', observation_start="1990-01-01")
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR', observation_start="1990-01-01")

    title = "Temporary Employment"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)
    chart = Chart(title=title, metadata=metadata, filename="us_temp_employment.png")

    chart.configure_y_axis(y_axis_index=0, label="Thousand of Persons",
                           minor_locator=MultipleLocator(100), major_locator=MultipleLocator(500))

    major_locator = mdates.YearLocator(base=3)
    minor_locator = mdates.YearLocator(base=1)

    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
