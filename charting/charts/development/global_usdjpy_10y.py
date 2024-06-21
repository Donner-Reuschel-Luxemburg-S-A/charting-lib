
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag


def main():
    blp = BloombergSource()

    #us10_df, us10_title = blp.get_series(series_id="USGG10YR Index", observation_start="19920101")
    usdjpy_df, usdjpy_title = blp.get_series(series_id="USDJPY Curncy", observation_start="19920101")


    title = "USDJPY"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="global_usdjpy_10y.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="Level")

    #chart.add_series(us10_df.index, us10_df['y'], label=us10_title)
    chart.add_series(usdjpy_df.index, usdjpy_df['y'], label=usdjpy_title)

    chart.add_horizontal_line()
    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()
