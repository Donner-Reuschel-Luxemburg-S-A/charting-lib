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

    jolts_df, jolts_title = blp.get_series(series_id="JOLTTOTL Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)


    title = "US JOLTS Job Openings"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="us_jolts.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(100), major_locator=MultipleLocator(500), label="")

    chart.add_series(jolts_df.index, jolts_df['y'], label=jolts_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()



if __name__ == '__main__':
    main()
