import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource
from pandas import DateOffset

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag

from charting.transformer.avg import Avg


def main():
    blp = BloombergSource()

    start_time="20010101"

    bkrp_df, bkrp_title = blp.get_series(series_id="BNKRINDX Index", observation_start=start_time)
    hy_oas_df, hy_oas_title = blp.get_series(series_id="LF98OAS Index", observation_start=start_time)



    title = "High Yield Credit Spreads vs. Bankruptcy Filings"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_bankruptcy_hy_oas.png",num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(100), major_locator=MultipleLocator(50))

    chart.add_series(bkrp_df.index, bkrp_df['y'], label=bkrp_title,y_axis_index=0,transformer=[Lag(offset=DateOffset(months=3))])
    chart.add_series(hy_oas_df.index, hy_oas_df['y'], label=hy_oas_title,y_axis_index=1)


    chart.add_horizontal_line()
    chart.legend()
    chart.plot()



if __name__ == '__main__':
    main()
