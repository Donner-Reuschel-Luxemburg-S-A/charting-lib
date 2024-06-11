import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg


def main(**kwargs):
    blp = BloombergSource()

    start_time = "19700101"

    nfp_df, nfp_title = blp.get_series(series_id="CANLNETJ Index", observation_start=start_time)

    title = "Canada Employment Change 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="ca_payrolls_mom_6.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1000), major_locator=MultipleLocator(5000), label="")

    df = nfp_df.iloc[6:, ]
    chart.add_series(df.index, df['y'] * 12, label=nfp_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "Canada Employment Change MoM"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="ca_payrolls_mom.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1000), major_locator=MultipleLocator(5000), label="")

    chart.add_series(nfp_df.index, nfp_df['y'], label=nfp_title)

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "Canada Employment Change YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="ca_payrolls_yoy.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1000), major_locator=MultipleLocator(5000), label="")

    nfp_df['z'] = nfp_df['y'].rolling(12).sum()
    nfp_df = nfp_df.iloc[12:, ]

    chart.add_series(nfp_df.index, nfp_df['z'], label=nfp_title)

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
