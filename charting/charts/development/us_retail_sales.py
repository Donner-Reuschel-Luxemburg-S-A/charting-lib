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

    retailsales_df, retailsales_title = blp.get_series(series_id="RSTAMOM  Index", observation_start=start_time)
    retailsales_ex_auto_df, retailsales_ex_auto_title = blp.get_series(series_id="RSTAXMOM Index",
                                                                       observation_start=start_time)
    retailsales_ex_auto_gas_df, retailsales_ex_auto_gas_title = blp.get_series(series_id="RSTAXMOM Index",
                                                                               observation_start=start_time)
    redbook_df, redbook_title = blp.get_series(series_id="REDSWYOY Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Retail Sales 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_retail_sales_mom_6", metadata=metadata, language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5),
                           label="Percentage Points")

    chart.add_series(retailsales_df.index, retailsales_df['y'] * 12, label=retailsales_title,
                     transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(retailsales_ex_auto_df.index, retailsales_ex_auto_df['y'] * 12, label=retailsales_ex_auto_title,
                     transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(retailsales_ex_auto_gas_df.index, retailsales_ex_auto_gas_df['y'] * 12,
                     label=retailsales_ex_auto_gas_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US Retail Sales 12M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_retail_sales_mom_12", metadata=metadata, language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5),
                           label="Percentage Points")

    chart.add_series(retailsales_df.index, retailsales_df['y'] * 12, label=retailsales_title,
                     transformer=[Avg(offset=DateOffset(months=12))])
    chart.add_series(retailsales_ex_auto_df.index, retailsales_ex_auto_df['y'] * 12, label=retailsales_ex_auto_title,
                     transformer=[Avg(offset=DateOffset(months=12))])
    chart.add_series(retailsales_ex_auto_gas_df.index, retailsales_ex_auto_gas_df['y'] * 12,
                     label=retailsales_ex_auto_gas_title, transformer=[Avg(offset=DateOffset(months=12))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US Retail Sales YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_retail_sales_yoy", metadata=metadata, language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5),
                           label="Percentage Points")

    retailsales_df['z'] = retailsales_df['y'].rolling(12).sum()
    retailsales_ex_auto_df['z'] = retailsales_ex_auto_df['y'].rolling(12).sum()
    retailsales_ex_auto_gas_df['z'] = retailsales_ex_auto_gas_df['y'].rolling(12).sum()

    chart.add_series(retailsales_df.index, retailsales_df['z'], label=retailsales_title)
    chart.add_series(retailsales_ex_auto_df.index, retailsales_ex_auto_df['z'], label=retailsales_ex_auto_title)
    chart.add_series(retailsales_ex_auto_gas_df.index, retailsales_ex_auto_gas_df['z'],
                     label=retailsales_ex_auto_gas_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US Johnson Redbook Same Store Sales"
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_redbook", metadata=metadata, language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5),
                           label="Percentage Points")

    chart.add_series(redbook_df.index, redbook_df['y'], label=redbook_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
