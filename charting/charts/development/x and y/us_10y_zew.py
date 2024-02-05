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

    us10_df, us10_title = blp.get_series(series_id="USGG10YR Index", observation_start="19950101")
    zew_df, zew_title = blp.get_series(series_id="GRZEUSLT Index", observation_start="19950101")

    title = "US 10y Yields vs. ZEW USA Expectations of Long Term Interest Rates"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_10y_zew.png",num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(0.5), major_locator=MultipleLocator(1))
   #chart.configure_y_axis(y_axis_index=0,minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    us10_df['z'] = us10_df['y']-us10_df['y'].shift(250)

    chart.add_series(us10_df.index, us10_df['z'], label="US 10yr Yield 1yr Change",y_axis_index=0)
    chart.add_series(zew_df.index, zew_df['y'], label=zew_title,y_axis_index=1,transformer=Lag(offset=DateOffset(months=-6)))


    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.plot()



if __name__ == '__main__':
    main()
