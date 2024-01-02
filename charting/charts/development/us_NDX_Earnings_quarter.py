import datetime

import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.pct import Pct
from charting.transformer.resample import Resample


def main():
    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='NDX Index', field="RR906", observation_start="20170101")

    title = "Nasdaq100 Earnings Quarter"


    chart = Chart(title=title, filename="Nasdaq100_Earnings_Quarter.png",  num_y_axis=2)

    chart.configure_y_axis(y_axis_index=0, label="EUR €")
    chart.configure_y_axis(y_axis_index=1, label="%")

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], chart_type='bar', transformer=[Resample('Q'), Pct(periods=4)], label=t1, y_axis_index=1)

    df1 = df1[df1.index >= datetime.datetime(2018, 1, 1)]

    chart.add_series(x=df1.index, y=df1['y'], transformer=Resample('Q'), label=t1)

    chart.add_horizontal_line(y_axis_index=1)

    chart.legend()
    chart.plot()

if __name__ == '__main__':
    main()
