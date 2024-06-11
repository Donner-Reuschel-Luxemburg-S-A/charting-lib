import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    fred = FredSource()
    df1, t1 = fred.get_series(series_id='DGS2', observation_start="2017-01-01")
    df2, t2 = fred.get_series(series_id='DGS5', observation_start="2017-01-01")

    df = df2 - df1

    title = "U.S. Treasury Spread 5-2-Year"
    metadata = Metadata(title=title, region=Region.US, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="us_treasury_spread_5y_2y.png")

    chart.configure_y_axis(y_axis_index=0, label="BPS", minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(10))

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_horizontal_line()
    chart.add_series(x=df.index, y=df['y'] * 100, label=title)

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
