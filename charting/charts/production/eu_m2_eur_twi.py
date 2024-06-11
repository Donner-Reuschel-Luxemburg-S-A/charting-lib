import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata


def main(**kwargs):
    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='ECMAM2YY Index', observation_start='20200901')
    df2, t2 = blp.get_series(series_id='TWI EUSP Index', observation_start='20210101')

    title = "M2 Geldmengenwachstum und EUR Entwicklung"
    metadata = Metadata(title=title, region=Region.EU, category=Category.CB)

    chart = Chart(title=title, num_y_axis=2, metadata=metadata, filename="m2_twi_eur.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(2))
    chart.configure_y_axis(y_axis_index=1, label="Points", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(2))

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=1)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0)
    chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=1)

    chart.legend(ncol=2)
    chart.add_horizontal_line(y_axis_index=0)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
