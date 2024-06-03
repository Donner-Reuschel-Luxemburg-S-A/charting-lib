import pandas as pd
import numpy as np
from pandas import DateOffset
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg


def main():
    blp = BloombergSource()

    #indprod_df, indprod_title = blp.get_series(series_id="EUIPEMUY Index", observation_start="19920101")
    indprodcap_df, indprodcap_title = blp.get_series(series_id="EUIPCEZY Index", observation_start="19990101")


    title = "Eurozone: Industrial Production YoY"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="eu_industrial_production.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(5), major_locator=MultipleLocator(10),label="%")

    #chart.add_series(indprod_df.index, indprod_df['y'], label=indprod_title)
    chart.add_series(indprodcap_df.index, indprodcap_df['y'], label=indprodcap_title)


    chart.add_horizontal_line()
    chart.legend()
    chart.plot()



if __name__ == '__main__':
    main()
