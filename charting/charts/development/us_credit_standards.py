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
    fred=FredSource()

    start_time="19290101"
    credit_small_df, credit_small_title = blp.get_series(series_id="SLDETGTS Index", observation_start=start_time)
    credit_large_df, credit_large_title = blp.get_series(series_id="SLDETIGT Index", observation_start=start_time)
    credit_consumer_df, credit_consumer_title = blp.get_series(series_id="SDCLTGTC Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US % of Bank Tightening Credit Standards"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_credit_standards.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(credit_small_df.index, credit_small_df['y'], label=credit_small_title)
    chart.add_series(credit_large_df.index, credit_large_df['y'], label=credit_large_title)
    chart.add_series(credit_consumer_df.index, credit_consumer_df['y'], label=credit_consumer_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.plot()



if __name__ == '__main__':
    main()
