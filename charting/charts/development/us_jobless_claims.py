import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19700101"

    ic_df, ic_title = blp.get_series(series_id="INJCJC Index", observation_start=start_time)
    cc_df, cc_title = blp.get_series(series_id="INJCSP Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Initial Jobless Claims"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="us_initial_claims.jpeg", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(100), major_locator=MultipleLocator(500), label="")

    chart.add_series(ic_df.index, ic_df['y'], label=ic_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US Continuing Jobless Claims"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="us_continuing_claims.jpeg", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1000), major_locator=MultipleLocator(5000), label="")

    chart.add_series(cc_df.index, cc_df['y'], label=cc_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
