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

    cpi_df, cpi_title = blp.get_series(series_id="GRCP20YY Index", observation_start="19920101")
    ppi_df, ppi_title = blp.get_series(series_id="GRPFIYOY Index", observation_start="19920101")
    wpi_df, wpi_title = blp.get_series(series_id="GRWPYOYI Index", observation_start="19920101")


    title = "Germany: Producer, Wholesale and Consumer Inflation"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="de_cpi_ppi.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(ppi_df.index, ppi_df['y'], label=ppi_title)
    chart.add_series(wpi_df.index, wpi_df['y'], label=wpi_title)

    chart.add_horizontal_line()
    chart.legend()
    chart.plot()

    title = "Germany: Producer, Wholesale and Consumer Inflation: Changes"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="de_cpi_ppi_adj.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    cpi_df['z'] = np.diff(cpi_df['y'], prepend=0)
    ppi_df['z'] = np.diff(ppi_df['y'], prepend=0)
    wpi_df['z'] = np.diff(wpi_df['y'], prepend=0)

    # Regression Beta Adjusted
    chart.add_series(cpi_df.index, cpi_df['z'], label=cpi_title)
    chart.add_series(ppi_df.index, ppi_df['z'], label=ppi_title)
    chart.add_series(wpi_df.index, wpi_df['z'], label=wpi_title)

    chart.add_horizontal_line()
    chart.legend()
    chart.plot()

if __name__ == '__main__':
    main()
