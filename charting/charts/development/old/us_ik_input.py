import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg


def main():
    blp = BloombergSource()

    # ******************
    # LEADING INDICATORS
    # ******************

    start_time = "19780101"

    us_yieldcurve_df, us_yieldcurve_title = blp.get_series(series_id="USYC2Y10 Index", observation_start=start_time)
    us_lei_df, us_lei_title = blp.get_series(series_id="LEI YOY Index", observation_start=start_time)
    us_lei6m_df, us_lei6m_title = blp.get_series(series_id="LEI 6MAN Index", observation_start=start_time)
    us_nber_df, us_nber_title = blp.get_series(series_id="USRINDEX Index", observation_start=start_time)

    title = "Yield Curve and Recessions"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_yield_curve_recessions.png", num_rows=1,num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(50))

    chart.add_series(us_yieldcurve_df.index, us_yieldcurve_df['y'], label=us_yieldcurve_title)
    chart.add_series(us_nber_df.index, us_nber_df['y'], label=us_nber_title,y_axis_index=1)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=1)
    chart.plot()

    # ---

    start_time = "19590101"

    us_lei_df, us_lei_title = blp.get_series(series_id="LEI YOY Index", observation_start=start_time)
    us_nber_df, us_nber_title = blp.get_series(series_id="USRINDEX Index", observation_start=start_time)

    title = "Conference Board Leading Indicator and Recessions"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_lei_recessions.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(50))

    chart.add_series(us_lei_df.index, us_lei_df['y'], label=us_lei_title)
    chart.add_series(us_nber_df.index, us_nber_df['y'], label=us_nber_title, y_axis_index=1)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=1)
    chart.plot()

    # ---

    start_time = "20180101"

    us_philly_df, us_philly_title = blp.get_series(series_id="OUST#NEG Index", observation_start=start_time)

    title = "Philadelphia Fed Coincident Index Number Of States With Negative Monthly Change"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_philly_recessions.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(10))

    chart.add_series(us_philly_df.index, us_philly_df['y'], label=us_philly_title)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=1)
    chart.plot()

    # *********
    # INFLATION
    # *********

    start_time = "19700101"

    cpi_df, cpi_title = blp.get_series(series_id="CPI YOY Index", observation_start=start_time)
    cpix_df, cpix_title = blp.get_series(series_id="CPI XYOY Index", observation_start=start_time)
    pce_df, pce_title = blp.get_series(series_id="PCE CYOY Index", observation_start=start_time)
    cpim_df, cpim_title = blp.get_series(series_id="CPI CHNG Index", observation_start=start_time)
    cpixm_df, cpixm_title = blp.get_series(series_id="CPUPXCHG Index", observation_start=start_time)
    pcem_df, pcem_title = blp.get_series(series_id="PCE CMOM Index", observation_start=start_time)

    ppi_df, ppi_title = blp.get_series(series_id="FDIUFDYO Index", observation_start=start_time)
    ppix_df, ppix_title = blp.get_series(series_id="FDIUSGYO Index", observation_start=start_time)

    start_min = ppi_df.index[0]

    ppim_df, ppim_title = blp.get_series(series_id="FDIDFDMO Index", observation_start=start_time)
    ppixm_df, ppixm_title = blp.get_series(series_id="FDIDSGMO Index", observation_start=start_time)

    title = "US Inflation Measures YoY"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inflation_measures_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['y'], label=cpix_title)
    chart.add_series(pce_df.index, pce_df['y'], label=pce_title)

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Inflation Measures 6M Ann."

    chart = Chart(title=title, filename="us_inflation_measures_mom_6.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title,
                     transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(pcem_df.index, pcem_df['y'] * 12, label=pcem_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Inflation Measures 3M Ann."

    chart = Chart(title=title, filename="us_inflation_measures_mom_3.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title,
                     transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(pcem_df.index, pcem_df['y'] * 12, label=pcem_title, transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    # ---

    title = "US Producer Prices YoY"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_producer_prices_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(ppi_df.index, ppi_df['y'], label=ppi_title)
    chart.add_series(ppix_df.index, ppix_df['y'], label=ppix_title)


    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()

    title = "US PPI vs. CPI YoY"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_ppi_cpi_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(ppi_df.index, ppi_df['y'], label=ppi_title)
    chart.add_series(ppix_df.index, ppix_df['y'], label=ppix_title)

    filtered_cpi_df = cpi_df[cpi_df.index >= start_min]
    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['y'], label=cpix_title)

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot()



if __name__ == '__main__':
    main()
