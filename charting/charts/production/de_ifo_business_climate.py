import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata


def main(**kwargs):
    blp = BloombergSource()

    start_date = "20050101"

    df1, t1 = blp.get_series(series_id='GRIFPEX Index', observation_start=start_date)
    df2, t2 = blp.get_series(series_id='GRIFPCA Index', observation_start=start_date)
    df3, t3 = blp.get_series(series_id='GRIFPBUS Index', observation_start=start_date)

    title = "IFO Business Climate"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="de_ifo_business_climate.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(5))

    major_locator = mdates.MonthLocator(interval=24)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1)
    chart.add_series(x=df2.index, y=df2['y'], label=t2)
    chart.add_series(x=df3.index, y=df3['y'], label=t3)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
