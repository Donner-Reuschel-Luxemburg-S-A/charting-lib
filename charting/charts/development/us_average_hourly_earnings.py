import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19700101"

    ahe_y_df, ahe_y_title = blp.get_series(series_id="AHE YOY% Index", observation_start=start_time)
    ahe_m_df, ahe_m_title = blp.get_series(series_id="AHE MOM% Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Average Hourly Earnings YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_ahe_yoy.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2),
                           label="Percentage Points")

    chart.add_series(ahe_y_df.index, ahe_y_df['y'], label=ahe_y_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US Average Hourly Earnings MoM 3M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_ahe_mom_3.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2),
                           label="Percentage Points")

    chart.add_series(ahe_m_df.index, ahe_m_df['y'] * 12, label=ahe_m_title,
                     transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US Average Hourly Earnings MoM 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_ahe_mom_6.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2),
                           label="Percentage Points")

    chart.add_series(ahe_m_df.index, ahe_m_df['y'] * 12, label=ahe_m_title,
                     transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
