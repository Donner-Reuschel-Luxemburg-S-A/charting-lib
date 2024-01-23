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
    fred = FredSource()

    start_time = "19980101"

    mba_df, mba_title = blp.get_series(series_id="MBAVCHNG Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)





    title = "US MBA Mortgage Applications"
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_mba.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    mba_df = mba_df.iloc[12:,]
    chart.add_series(mba_df.index, mba_df['y'], label=mba_title, transformer=[Avg(offset=DateOffset(months=12))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    # title = "US Inflation Measures YoY: Change"
    #
    # chart = Chart(title=title, filename="us_inflation_measures_yoy_delta.png")
    # chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    # chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")
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
