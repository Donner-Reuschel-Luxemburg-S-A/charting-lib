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

    start_time = "19980101"

    ehs_df, ehs_title = blp.get_series(series_id="ETSLMOM Index", observation_start=start_time)
    nhs_df, nhs_title = blp.get_series(series_id="NHSLCHNG Index", observation_start=start_time)
    phs_df, phs_title = blp.get_series(series_id="USPHTMOM Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Home Sales 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_home_sales_mom_6.jpeg", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(2), major_locator=MultipleLocator(10),
                           label="Percentage Points")

    chart.add_series(ehs_df.index, ehs_df['y'] * 12, label=ehs_title, transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(nhs_df.index, nhs_df['y'] * 12, label=nhs_title, transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(phs_df.index, phs_df['y'] * 12, label=phs_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US Home Sales 12M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_home_sales_12.jpeg", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(2), major_locator=MultipleLocator(10),
                           label="Percentage Points")

    chart.add_series(ehs_df.index, ehs_df['y'] * 12, label=ehs_title, transformer=[Avg(offset=DateOffset(months=12))])
    chart.add_series(nhs_df.index, nhs_df['y'] * 12, label=nhs_title, transformer=[Avg(offset=DateOffset(months=12))])
    chart.add_series(phs_df.index, phs_df['y'] * 12, label=phs_title, transformer=[Avg(offset=DateOffset(months=12))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US Home Sales YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_home_sales_yoy.jpeg", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(2), major_locator=MultipleLocator(10),
                           label="Percentage Points")

    ehs_df['z'] = ehs_df['y'].rolling(12).sum()
    nhs_df['z'] = nhs_df['y'].rolling(12).sum()
    phs_df['z'] = phs_df['y'].rolling(12).sum()

    chart.add_series(ehs_df.index, ehs_df['z'], label=ehs_title)
    chart.add_series(nhs_df.index, nhs_df['z'], label=nhs_title)
    chart.add_series(phs_df.index, phs_df['z'], label=phs_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
