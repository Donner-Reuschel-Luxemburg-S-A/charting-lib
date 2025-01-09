import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource
from pandas import DateOffset

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg
from charting.transformer.pct import Pct
from charting.transformer.invert import Invert

def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "20220601"



    citi_us_df, citi_us_title = blp.get_series(series_id="CESIUSD Index", observation_start=start_time)
    us10y_df, us10y_title = blp.get_series(series_id="USGG10YR Index", observation_start=start_time)

    title = "US Economic Surprise Index vs. 10y Yield"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_citisurprise_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.MonthLocator(bymonth=3), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(20), major_locator=MultipleLocator(20),label="%")

    chart.add_series(citi_us_df.index, citi_us_df['y'], label=citi_us_title)
    chart.add_series(us10y_df.index,us10y_df['y'], label=us10y_title,y_axis_index=1,transformer=[Lag(DateOffset(months=3))])


    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()



if __name__ == '__main__':
    main()
