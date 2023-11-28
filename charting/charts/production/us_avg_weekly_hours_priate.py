import matplotlib.dates as mdates
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main():
    fred = FredSource()
    d1, t1 = fred.get_series(series_id='AWHAETP', observation_start="2006-01-01")
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR', observation_start="2006-01-01")

    title = "Average Weekly Hours of All Employees, Total Private"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)
    chart = Chart(title=title, metadata=metadata, filename="us_avg_weekly_hours_private.png")

    chart.configure_y_axis(y_axis_index=0, label="Hours")

    major_locator = mdates.YearLocator(base=2)
    minor_locator = mdates.YearLocator(base=1)

    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()

