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
    eurusd_df, eurusd_title = blp.get_series(series_id="EURUSD Curncy", observation_start=start_time)
    eurjpy_df, eurjpy_title = blp.get_series(series_id="EURJPY Curncy", observation_start=start_time)
    eurchf_df, eurchf_title = blp.get_series(series_id="EURCHF Curncy", observation_start=start_time)
    euraud_df, euraud_title = blp.get_series(series_id="EURAUD Curncy", observation_start=start_time)
    eurgbp_df, eurgbp_title = blp.get_series(series_id="EURGBP Curncy", observation_start=start_time)




    cl1_df, cl1_title = blp.get_series(series_id="CL1 Comdty", observation_start=start_time)

    uk10y_df, uk10y_title = blp.get_series(series_id="GUKG10 Index", observation_start=start_time)
    ch10y_df, ch10y_title = blp.get_series(series_id="GSWISS10 Index", observation_start=start_time)
    au10y_df, au10y_title = blp.get_series(series_id="GACGB10 Index", observation_start=start_time)
    jp10y_df, jp10y_title = blp.get_series(series_id="GJGB10 Index", observation_start=start_time)
    us10y_df, us10y_title = blp.get_series(series_id="USGG10YR Index", observation_start=start_time)
    gcan10y_df,gcan10y_title = blp.get_series(series_id="GCAN10YR Index", observation_start=start_time)
    gdbr10y_df, gdbr10y_title = blp.get_series(series_id="GDBR10 Index", observation_start=start_time)

    uk2y_df, uk2y_title = blp.get_series(series_id="GUKG2 Index", observation_start=start_time)
    ch2y_df, ch2y_title = blp.get_series(series_id="GSWISS2 Index", observation_start=start_time)
    au2y_df, au2y_title = blp.get_series(series_id="GACGB2 Index", observation_start=start_time)
    jp2y_df, jp2y_title = blp.get_series(series_id="GJGB2 Index", observation_start=start_time)
    us2y_df, us2y_title = blp.get_series(series_id="USGG2YR Index", observation_start=start_time)
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

    df = gdbr10y_df.copy()
    df['y'] = df['y'] - gcan10y_df['y']

    title = "EURCAD vs. Rates Delta (10y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="fx_cad_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurcad_df.index, eurcad_df['y'], label=eurcad_title)
    chart.add_series(df.index, df['y'], label="10y Bunds - 10y Canada", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "EURCAD vs. Rates Delta (2y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr2y_df.copy()
    df['y'] = df['y'] - gcan2y_df['y']

    chart = Chart(title=title, filename="fx_cad_2y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurcad_df.index, eurcad_df['y'], label=eurcad_title)
    chart.add_series(df.index, df['y'], label="2y Bunds - 2y Canada", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "EURGBP vs. Rates Delta (10y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr10y_df.copy()
    df['y'] = df['y'] - uk10y_df['y']

    chart = Chart(title=title, filename="fx_uk_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurgbp_df.index, eurcad_df['y'], label=eurgbp_title)
    chart.add_series(df.index, df['y'], label="10y Bunds - 10y UK", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()


    title = "EURGBP vs. Rates Delta (2y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr2y_df.copy()
    df['y'] = df['y'] - uk2y_df['y']

    chart = Chart(title=title, filename="fx_uk_2y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurgbp_df.index, eurgbp_df['y'], label=eurgbp_title)
    chart.add_series(df.index, df['y'], label="2y Bunds - 2y UK", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()


    title = "EURGBP vs. Rates Delta (10y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr10y_df.copy()
    df['y'] = df['y'] - uk10y_df['y']

    chart = Chart(title=title, filename="fx_uk_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurgbp_df.index, eurgbp_df['y'], label=eurgbp_title)
    chart.add_series(df.index, df['y'], label="10y Bunds - 10y UK", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()


    title = "EURCHF vs. Rates Delta (2y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr2y_df.copy()
    df['y'] = df['y'] - ch2y_df['y']

    chart = Chart(title=title, filename="fx_ch_2y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurchf_df.index, eurchf_df['y'], label=eurchf_title)
    chart.add_series(df.index, df['y'], label="2y Bunds - 2y Swiss", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "EURCHF vs. Rates Delta (10y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr10y_df.copy()
    df['y'] = df['y'] - ch10y_df['y']

    chart = Chart(title=title, filename="fx_ch_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurchf_df.index, eurchf_df['y'], label=eurchf_title)
    chart.add_series(df.index, df['y'], label="10y Bunds - 10y Swiss", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()


    title = "EURUSD vs. Rates Delta (2y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr2y_df.copy()
    df['y'] = df['y'] - us2y_df['y']

    chart = Chart(title=title, filename="fx_us_2y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurusd_df.index, eurusd_df['y'], label=eurusd_title)
    chart.add_series(df.index, df['y'], label="2y Bunds - 2y UST", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "EURUSD vs. Rates Delta (10y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr10y_df.copy()
    df['y'] = df['y'] - us10y_df['y']

    chart = Chart(title=title, filename="fx_us_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.01), major_locator=MultipleLocator(.02), label="")

    chart.add_series(eurusd_df.index, eurusd_df['y'], label=eurusd_title)
    chart.add_series(df.index, df['y'], label="10y Bunds - 10y UST", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "EURJPY vs. Rates Delta (2y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr2y_df.copy()
    df['y'] = df['y'] - jp2y_df['y']

    chart = Chart(title=title, filename="fx_jp_2y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(10), major_locator=MultipleLocator(10), label="")

    chart.add_series(eurjpy_df.index, eurjpy_df['y'], label=eurjpy_title)
    chart.add_series(df.index, df['y'], label="2y Bunds - 2y Japan", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "EURJPY vs. Rates Delta (10y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr10y_df.copy()
    df['y'] = df['y'] - jp10y_df['y']

    chart = Chart(title=title, filename="fx_jp_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(10), major_locator=MultipleLocator(10), label="")

    chart.add_series(eurjpy_df.index, eurjpy_df['y'], label=eurjpy_title)
    chart.add_series(df.index, df['y'], label="10y Bunds - 10y Japan", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "EURAUD vs. Rates Delta (2y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr2y_df.copy()
    df['y'] = df['y'] - au2y_df['y']

    chart = Chart(title=title, filename="fx_au_2y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.1), major_locator=MultipleLocator(.1), label="")

    chart.add_series(euraud_df.index, euraud_df['y'], label=euraud_title)
    chart.add_series(df.index, df['y'], label="2y Bunds - 2y Australia", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "EURAUD vs. Rates Delta (10y)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    df = gdbr10y_df.copy()
    df['y'] = df['y'] - au10y_df['y']

    chart = Chart(title=title, filename="fx_au_10y.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.1), major_locator=MultipleLocator(.1), label="")

    chart.add_series(euraud_df.index, euraud_df['y'], label=euraud_title)
    chart.add_series(df.index, df['y'], label="10y Bunds - 10y Australia", y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()


if __name__ == '__main__':
    main()
