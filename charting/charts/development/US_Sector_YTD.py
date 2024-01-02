import datetime

import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.pct import Pct
from charting.transformer.resample import Resample
from charting.transformer.ytd import Ytd


def main():
    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='S5ENRS Index', observation_start="20230101", field="px_close_1d")
    df2, t2 = blp.get_series(series_id='S5CONS Index', observation_start="20230101", field="px_close_1d")
    df3, t3 = blp.get_series(series_id='S5HLTH Index', observation_start="20230101", field="px_close_1d")
    df4, t4 = blp.get_series(series_id='S5TELS Index', observation_start="20230101", field="px_close_1d")
    df5, t5 = blp.get_series(series_id='s5matr Index', observation_start="20230101", field="px_close_1d")
    df6, t6 = blp.get_series(series_id='s5indu Index', observation_start="20230101", field="px_close_1d")
    df7, t7 = blp.get_series(series_id='s5cond Index', observation_start="20230101", field="px_close_1d")
    df8, t8 = blp.get_series(series_id='s5finl Index', observation_start="20230101", field="px_close_1d")
    df9, t9 = blp.get_series(series_id='s5inft Index', observation_start="20230101", field="px_close_1d")
    df10, t10 = blp.get_series(series_id='s5rlst Index', observation_start="20230101", field="px_close_1d")

    title = "USA Sektoren YTD"

    chart = Chart(title=title, filename="USA_Sektoren_YTD.png")

    chart.configure_y_axis(y_axis_index=0, label="%",minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=2)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Ytd())
    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Ytd())
    chart.add_series(x=df3.index, y=df3['y'], label=t3, transformer=Ytd())
    chart.add_series(x=df4.index, y=df4['y'], label=t4, transformer=Ytd())
    chart.add_series(x=df5.index, y=df5['y'], label=t5, transformer=Ytd())
    chart.add_series(x=df6.index, y=df6['y'], label=t6, transformer=Ytd())
    chart.add_series(x=df7.index, y=df7['y'], label=t7, transformer=Ytd())
    chart.add_series(x=df8.index, y=df8['y'], label=t8, transformer=Ytd())
    chart.add_series(x=df9.index, y=df9['y'], label=t9, transformer=Ytd())
    chart.add_horizontal_line()
    chart.add_last_value_badge()

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
