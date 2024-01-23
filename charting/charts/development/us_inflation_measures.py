import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg
from charting.transformer.lag import Lag


def main():
    blp = BloombergSource()

    start_time = "19980101"

    cpi_df, cpi_title = blp.get_series(series_id="CPI YOY Index", observation_start=start_time)
    cpix_df, cpix_title = blp.get_series(series_id="CPI XYOY Index", observation_start=start_time)
    pce_df, pce_title = blp.get_series(series_id="PCE CYOY Index", observation_start=start_time)
    cpim_df, cpim_title = blp.get_series(series_id="CPI CHNG Index", observation_start=start_time)
    cpixm_df, cpixm_title = blp.get_series(series_id="CPUPXCHG Index", observation_start=start_time)
    pcem_df, pcem_title = blp.get_series(series_id="PCE CMOM Index", observation_start=start_time)

    cpi_ex_shelter_df, cpi_ex_shelter_title = blp.get_series(series_id="CPUPNFEY Index", observation_start=start_time)
    cpi_shelter_df, cpi_shelter_title = blp.get_series(series_id="CPRHOERY Index", observation_start=start_time)
    zillow_df, zillow_title = blp.get_series(series_id="ZRIOAYOY Index", observation_start=start_time)

    ppi_df, ppi_title = blp.get_series(series_id="FDIUFDYO Index", observation_start=start_time)
    ppix_df, ppix_title = blp.get_series(series_id="FDIUSGYO Index", observation_start=start_time)

    import_prices_df, import_prices_title = blp.get_series(series_id="IMP1YOY% Index", observation_start=start_time)
    import_pricesm_df, import_pricesm_title = blp.get_series(series_id="IMP1CHNG Index", observation_start=start_time)

    export_prices_df, export_prices_title = blp.get_series(series_id="EXP1CYOY Index", observation_start=start_time)
    export_pricesm_df, export_pricesm_title = blp.get_series(series_id="EXP1CMOM Index", observation_start=start_time)

    inflation_exp1y_df, inflation_exp1y_title = blp.get_series(series_id="CONSPXMD Index", observation_start=start_time)
    inflation_exp5y_df, inflation_exp5y_title = blp.get_series(series_id="CONSP5MD Index", observation_start=start_time)

    title = "US Inflation Measures YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inflation_measures_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['y'], label=cpix_title)
    chart.add_series(pce_df.index, pce_df['y'], label=pce_title)

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Inflation Measures 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inflation_measures_mom_6.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title,
                     transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(pcem_df.index, pcem_df['y'] * 12, label=pcem_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Inflation Measures 3M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inflation_measures_mom_3.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title,
                     transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(pcem_df.index, pcem_df['y'] * 12, label=pcem_title, transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US PPI vs. CPI YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_ppi_cpi_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(ppi_df.index, ppi_df['y'], label=ppi_title)
    chart.add_series(ppix_df.index, ppix_df['y'], label=ppix_title)

    start_min = ppi_df.index[0]
    filtered_cpi_df = cpi_df[cpi_df.index >= start_min]
    filtered_cpix_df = cpix_df[cpix_df.index >= start_min]

    chart.add_series(filtered_cpi_df.index, filtered_cpi_df['y'], label=cpi_title)
    chart.add_series(filtered_cpix_df.index, filtered_cpix_df['y'], label=cpix_title)

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US CPI ex Shelter YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_ex_shelter_cpi_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(cpi_ex_shelter_df.index, cpi_ex_shelter_df['y'], label=cpi_ex_shelter_title)

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US CPI Shelter YoY vs. Zillow Rent Index"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_shelter_cpi_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    start_min = zillow_df.index[0]
    filtered_cpi_shelter_df = cpi_shelter_df[cpi_shelter_df.index >= start_min]

    chart.add_series(filtered_cpi_shelter_df.index, filtered_cpi_shelter_df['y'], label=cpi_shelter_title)
    chart.add_series(zillow_df.index, zillow_df['y'], label=zillow_title,
                     transformer=Lag(offset=DateOffset(months=-12)))

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Import and Export Prices YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_import_export_prices_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(import_prices_df.index, import_prices_df['y'], label=import_prices_title)
    chart.add_series(export_prices_df.index, export_prices_df['y'], label=export_prices_title)

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Import and Export Prices 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_import_export_prices_mom_6.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(import_pricesm_df.index, import_pricesm_df['y'] * 12, label=import_pricesm_title,
                     transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(export_pricesm_df.index, export_pricesm_df['y'] * 12, label=export_pricesm_title,
                     transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Import and Export Prices 3M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_import_export_prices_mom_3.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(import_pricesm_df.index, import_pricesm_df['y'] * 12, label=import_pricesm_title,
                     transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(export_pricesm_df.index, export_pricesm_df['y'] * 12, label=export_pricesm_title,
                     transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Inflation Expectations"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inflation_expectations.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=2))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(inflation_exp1y_df.index, inflation_exp1y_df['y'], label=inflation_exp1y_title)
    chart.add_series(inflation_exp5y_df.index, inflation_exp5y_df['y'], label=inflation_exp5y_title)

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    # title = "US Inflation Measures YoY: Change"
    #
    # chart = Chart(title=title, filename="us_inflation_measures_yoy_delta.png")
    # chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    # chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="Percentage Points")
    #
    # cpi_df['z'] = np.diff(cpi_df['y'],prepend=0)
    # cpix_df['z'] = np.diff(cpix_df['y'],prepend=0)
    # pce_df['z'] = np.diff(pce_df['y'],prepend=0)
    #
    # chart.add_series(cpi_df.index, cpi_df['z'] * 12, label=cpi_title, transformer=[Avg(offset=DateOffset(months=3))])
    # chart.add_series(cpix_df.index, cpix_df['z'] * 12, label=cpix_title,
    #                  transformer=[Avg(offset=DateOffset(months=3))])
    # chart.add_series(pce_df.index, pce_df['z'] * 12, label=pce_title, transformer=[Avg(offset=DateOffset(months=3))])
    #
    # chart.add_horizontal_line()
    # chart.legend(ncol=2)
    # chart.plot()


if __name__ == '__main__':
    main()
