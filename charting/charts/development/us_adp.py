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

    start_time = "19700101"

    adp_df, adp_title = blp.get_series(series_id="ADP CHNG Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)





    title = "US ADP Employment Change 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="us_adp_mom_6.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(500), major_locator=MultipleLocator(1000), label="")

    df = adp_df.iloc[6:, ]
    chart.add_series(df.index, df['y']*12, label=adp_title, transformer=[Avg(offset=DateOffset(months=6))])


    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US ADP Employment Change MoM"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="us_adp_mom.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(500), major_locator=MultipleLocator(1000), label="")

    chart.add_series(adp_df.index, adp_df['y'], label=adp_title)


    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US ADP Employment Change YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="us_adp_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(500), major_locator=MultipleLocator(1000), label="")

    adp_df['z']=adp_df['y'].rolling(12).sum()
    adp_df = adp_df.iloc[12:,]

    chart.add_series(adp_df.index, adp_df['z'], label=adp_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

if __name__ == '__main__':
    main()
