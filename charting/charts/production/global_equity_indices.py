import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.transformer.ytd import Ytd


def main(**kwargs):
    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='SX5E Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))
    df2, t2 = blp.get_series(series_id='SXXP Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))
    df3, t3 = blp.get_series(series_id='DAX Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))
    df4, t4 = blp.get_series(series_id='SPX Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))
    df5, t5 = blp.get_series(series_id='MXEF Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))

    title = "Euro Stoxx 50, Stoxx Euro 600, DAX, S&P 500, Emerging Markets - Performance"

    chart = Chart(title=title, filename="global_indices_performance.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(5))

    major_locator = mdates.MonthLocator(interval=1)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Ytd())
    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Ytd())
    chart.add_series(x=df3.index, y=df3['y'], label=t3, transformer=Ytd())
    chart.add_series(x=df4.index, y=df4['y'], label=t4, transformer=Ytd())
    chart.add_series(x=df5.index, y=df5['y'], label=t5, transformer=Ytd())

    chart.add_horizontal_line()
    chart.add_last_value_badge(2)

    chart.legend(ncol=3)

    return chart.plot(upload_chart='observation_start' not in kwargs)
