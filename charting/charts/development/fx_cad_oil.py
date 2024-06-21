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

    start_time = "20210201"

    eurcad_df, eurcad_title = blp.get_series(series_id="EURCAD Curncy", observation_start=start_time)
    cl1_df, cl1_title = blp.get_series(series_id="CL1 Comdty", observation_start=start_time)

    gcan10y_df,gcan10y_title = blp.get_series(series_id="GCAN10YR Index", observation_start=start_time)
    gdbr10y_df, gdbr10y_title = blp.get_series(series_id="GDBR10 Index", observation_start=start_time)

    gcan2y_df, gcan2_title = blp.get_series(series_id="GCAN2YR Index", observation_start=start_time)
    gdbr2y_df, gdbr2y_title = blp.get_series(series_id="GDBR2 Index", observation_start=start_time)

    title = "EURCAD vs. Oil"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="fx_cad_oil.png", num_rows=1,num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.01),label="")

    chart.add_series(eurcad_df.index, eurcad_df['y'], label=eurcad_title)
    chart.add_series(cl1_df.index, cl1_df['y'], label=cl1_title,y_axis_index=1,transformer=[Invert()])

    chart.legend(ncol=1)
    chart.add_horizontal_line(y=1.47)
    chart.plot()

    df = gdbr10y_df
    df['y'] = df['y']-gcan10y_df['y']

    title = "EURCAD vs. Rates Delta (10y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="fx_cad_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurcad_df.index, eurcad_df['y'], label=eurcad_title)
    chart.add_series(df.index, df['y'], label="10y Bunds - 10y Canada", y_axis_index=1)

    chart.legend(ncol=1)
    chart.add_horizontal_line(y=1.47)
    chart.plot()

    title = "EURCAD vs. Rates Delta (2y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr2y_df
    df['y'] = df['y'] - gcan2y_df['y']

    chart = Chart(title=title, filename="fx_cad_2y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurcad_df.index, eurcad_df['y'], label=eurcad_title)
    chart.add_series(df.index, df['y'], label="2y Bunds - 2y Canada", y_axis_index=1)

    chart.legend(ncol=1)
    chart.add_horizontal_line(y=1.47)
    chart.plot()


if __name__ == '__main__':
    main()
