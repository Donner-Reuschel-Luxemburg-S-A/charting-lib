from pandas import DateOffset

from charting.charts.time_series_chart import TimeSeriesChart

from charting.transformer.avg import Avg
from charting.transformer.pct import Pct
import matplotlib.dates as mdates

from examples import fred

if __name__ == '__main__':
    d1, t1, a1 = fred.get_series(series_id='RSAFS', observation_start="2020-01-01")

    chart = TimeSeriesChart(title="US retail sales: YoY change",
                            figsize=(10, 6), num_y_axes=1)

    major_locator = mdates.MonthLocator(interval=2)
    major_formatter = mdates.DateFormatter(fmt="%b %Y")
    chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)
    chart.configure_x_ticks(length=5, pad=5, rotation=90)

    chart.configure_y_axis(axis_index=0, label="Percent [%]", y_lim=(0, 35))

    chart.add_data(x=d1.index, y=d1['y'], label=t1, chart_type='bar',
                   y_axis=0, bar_bottom=0, transformer=[Pct(periods=12), Avg(offset=DateOffset(months=3))])

    chart.legend(frameon=False, ncol=1, bbox_to_anchor=(0.5, -0.3))
    chart.plot(path="output/retail.png")
