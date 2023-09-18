from matplotlib.ticker import AutoLocator, MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.transformer.lead import Lead
from charting.transformer.pct import Pct
from charting.transformer.resample import Resample
import matplotlib.dates as mdates


if __name__ == '__main__':
    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='SPX Index', observation_start='20220631')
    # df3, t3 = blp.get_series(series_id='LEI YOY Index', observation_start='20220331')
    # df4, t4 = blp.get_series(series_id='USYC2Y10 Index', observation_start='20220331')

    list_sector = ["s5tels index", "s5util index"]
    # ["s5inft index","s5hlth index","s5cons index","s5cond index","s5enrs index","s5rlst index","s5matr index","s5indu index","s5finl index"]

    for sector in list_sector:
        df2, t2 = blp.get_series(series_id=sector, observation_start='20220331')

        df2['relative'] = df2['y'] / df1['y']/df2['y'].iloc[0]*df1['y'].iloc[0]

        chart = Chart(title=f"{sector} vs S&P 500 ", filename=f"spx_{sector}_relative.png")

        chart.configure_y_axis(y_axis_index=0, label="%")
        # chart.configure_y_axis(y_axis_index=1, label="PX LAST")
        # chart.configure_y_axis(y_axis_index=2, label="PX LAST")

        major_locator = mdates.YearLocator(base=5)
        minor_locator = mdates.YearLocator(base=1)
        major_formatter = mdates.AutoDateFormatter(major_locator)
        chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

        chart.configure_x_ticks(which='minor', length=1, width=1)
        chart.configure_x_ticks(which='major', length=1, width=1, pad=5)

        # chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0, transformer=[Resample(rule='W'), Pct(periods=1)])
        # chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=0, transformer=[Resample(rule='W'), Pct(periods=1)])

        chart.add_series(x=df2.index, y=df2['relative'], label=t2, y_axis_index=0,
                         transformer=[Resample(rule='W')])

        # chart.add_series(x=df3.index, y=df3['y'], label=t3, y_axis_index=1)
        # chart.add_series(x=df4.index, y=df4['y'], label="Sell 2Y/Buy 10Y Index", y_axis_index=2,transformer=[Resample(rule='W')])

        # chart.add_horizontal_line(y_axis_index=2)

        chart.legend()
        chart.plot()

