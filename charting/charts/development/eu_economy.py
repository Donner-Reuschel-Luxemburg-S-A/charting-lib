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

    start_date = "20220101"

    blp = BloombergSource()


    gdp_df, gdp_title = blp.get_series(series_id="EUGNEMUY Index",field="PX_LAST", observation_start=start_date)
    ip_df, ip_title = blp.get_series(series_id="EUIPEMUY Index",field="PX_LAST", observation_start=start_date)
    rs_df, rs_title = blp.get_series(series_id="RSWAEMUY Index", field="PX_LAST", observation_start=start_date)


    title = "Eurozone Economy"
    #title = "Euro Unternehmensanleihen: Refinanzierungskosten"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="eu_economy.png",num_rows = 3)

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(row_index=0,minor_locator=MultipleLocator(5), major_locator=MultipleLocator(10), label="%")
    chart.configure_y_axis(row_index=1, minor_locator=MultipleLocator(5), major_locator=MultipleLocator(10), label="%")
    chart.configure_y_axis(row_index=2, minor_locator=MultipleLocator(5), major_locator=MultipleLocator(10), label="%")

    chart.add_series(gdp_df.index, gdp_df['y'], label="Eurozone GDP", row_index=0)
    chart.add_series(ip_df.index, ip_df['y'], label="Eurozone Industrial Production", row_index=1)
    chart.add_series(rs_df.index, rs_df['y'], label="Eurozone Retail Sales", row_index=2)

    chart.add_horizontal_line(y=0,row_index=0)
    chart.add_horizontal_line(y=0,row_index=1)
    chart.add_horizontal_line(y=0,row_index=2)
    chart.legend(ncol=1)
    chart.plot()





if __name__ == '__main__':
    main()
