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

    start_date = "20050101"

    de_ind_prod_df, de_ind_prod_title = blp.get_series(series_id="GRIPIMOM Index", observation_start=start_date)


    # Industrial Production

    title = "Germany Industrial Production: 3M Ann."

    chart = Chart(title=title, filename="de_industrial_production_mom_3.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(10), label="%")

    chart.add_series(de_ind_prod_df.index, de_ind_prod_df['y'] * 12, label=de_ind_prod_title, transformer=[Avg(offset=DateOffset(months=3))])


    chart.add_horizontal_line()
    chart.legend(ncol=2)
    chart.plot()

    # IFO

    df1, t1 = blp.get_series(series_id='GRIFPEX Index', observation_start=start_date)
    df2, t2 = blp.get_series(series_id='GRIFPCA Index', observation_start=start_date)
    df3, t3 = blp.get_series(series_id='GRIFPBUS Index', observation_start=start_date)

    title = "Germany: IFO Business Climate"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="de_ifo_business_climate.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(5))

    major_locator = mdates.MonthLocator(interval=24)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1)
    chart.add_series(x=df2.index, y=df2['y'], label=t2)
    chart.add_series(x=df3.index, y=df3['y'], label=t3)

    chart.legend(ncol=2)
    chart.plot()

    # ZEW

    df4, t4 = blp.get_series(series_id='GRZECURR Index', observation_start=start_date)
    df5, t5 = blp.get_series(series_id='GRZEWI Index', observation_start=start_date)

    title = "ZEW Germany Surveys"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="de_zew_business_climate.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(10))

    major_locator = mdates.MonthLocator(interval=24)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df4.index, y=df4['y'], label=t4)
    chart.add_series(x=df5.index, y=df5['y'], label=t5)

    chart.legend(ncol=2)
    chart.plot()

    # Eurozone

    df7, t7 = blp.get_series(series_id='GRZEEUCU Index', observation_start=start_date)
    df8, t8 = blp.get_series(series_id='GRZEEUEX Index', observation_start=start_date)

    title = "ZEW Eurozone Surveys"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_zew_business_climate.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(10))

    major_locator = mdates.MonthLocator(interval=24)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df7.index, y=df7['y'], label=t7)
    chart.add_series(x=df8.index, y=df8['y'], label=t8)


    chart.legend(ncol=2)
    chart.plot()

    # Citi

    df9, t9 = blp.get_series(series_id='CESIEUR Index', observation_start=start_date)

    title = "Citi Economic Surprise Index: Eurozone"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_citi.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(50))

    major_locator = mdates.MonthLocator(interval=24)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df9.index, y=df9['y'], label=t9)


    chart.legend(ncol=2)
    chart.plot()

    # PMIs

    df10, t10 = blp.get_series(series_id='MPMIEZCA Index', observation_start=start_date)
    df11, t11 = blp.get_series(series_id='MPMIFRCA Index', observation_start=start_date)
    df12, t12 = blp.get_series(series_id='MPMIITCA Index', observation_start=start_date)
    df13, t13 = blp.get_series(series_id='MPMIDECA Index', observation_start=start_date)

    title = "Composite PMIs: Eurozone"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_pmi.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(50))

    major_locator = mdates.MonthLocator(interval=24)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df10.index, y=df10['y'], label=t10)
    chart.add_series(x=df11.index, y=df11['y'], label=t11)
    chart.add_series(x=df12.index, y=df12['y'], label=t12)
    chart.add_series(x=df13.index, y=df13['y'], label=t13)

    chart.legend(ncol=2)
    chart.plot()

    # Stock Market Inside

    df14, t14 = blp.get_series(series_id='SXAP Index', observation_start=start_date)
    df15, t15 = blp.get_series(series_id='SX86P Index', observation_start=start_date)
    df16, t16 = blp.get_series(series_id='SXNP Index', observation_start=start_date)
    df17, t17 = blp.get_series(series_id='SX6P Index', observation_start=start_date)

    title = "STOXX 600: Cyclicals vs. Defensives"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_inside_stocks.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(0.5),
                           major_locator=MultipleLocator(0.5))

    major_locator = mdates.MonthLocator(interval=24)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    s1 = df14['y'] / df17['y']
    s3 = df16['y'] / df17['y']

    chart.add_series(x=df14.index, y=s1, label="Autos / Utilities")
    chart.add_series(x=df16.index, y=s3, label="Industrials / Utilities")


    chart.legend(ncol=2)
    chart.plot()

    title = "STOXX 600: Real Estate vs. Utes"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_inside_stocks2.png")

    chart.configure_y_axis(y_axis_index=0, label="Index", minor_locator=MultipleLocator(0.5),
                           major_locator=MultipleLocator(0.5))

    major_locator = mdates.MonthLocator(interval=24)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    s2 = df15['y'] / df17['y']


    chart.add_series(x=df15.index, y=s2, label="Real Estate / Utilities")



    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
