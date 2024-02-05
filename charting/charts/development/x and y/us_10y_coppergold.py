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
from charting.transformer.invert import Invert



def main():
    blp = BloombergSource()

    start_date="20030101"

    us10_df, us10_title = blp.get_series(series_id="USGG10YR Index", observation_start=start_date)
    coppergold_df, coppergold_title = blp.get_series(series_id=".GLDHG G Index", observation_start=start_date)

    title = "US 10y Yields vs. Copper/Gold Ratio"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_10y_coppergold.png",num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(0.5), major_locator=MultipleLocator(1))
   #chart.configure_y_axis(y_axis_index=0,minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))


    chart.add_series(us10_df.index, us10_df['y'], label=us10_title,y_axis_index=0)
    chart.add_series(coppergold_df.index, coppergold_df['y'], label=coppergold_title,y_axis_index=1,transformer=Invert())


    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.plot()



if __name__ == '__main__':
    main()
