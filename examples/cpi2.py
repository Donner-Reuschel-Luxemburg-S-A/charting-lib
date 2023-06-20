from matplotlib import pyplot as plt
from matplotlib.ticker import AutoLocator, MultipleLocator
from pandas import DateOffset

from charting.charts.time_series_chart import TimeSeriesChart
from charting.transformer.lead import Lead
from charting.transformer.pct import Pct
from charting.transformer.resample import Resample
import matplotlib.dates as mdates

from examples import blp, fred

if __name__ == '__main__':
    df1, t1 = fred.get_series(series_id='CPIAUCSL', observation_start='2016-01-01')
    df2, t2 = fred.get_series(series_id='CPILFESL', observation_start='2016-01-01')

    food_df, _ = fred.get_series(series_id='CPIUFDSL', observation_start='2016-12-01')
    energy_df, _ = fred.get_series(series_id='CPIENGSL', observation_start='2016-12-01')

    chart = TimeSeriesChart(title="U.S. CPI by Component", num_y_axes=1)

    chart.configure_y_axis(axis_index=0, label="%", y_lim=(-2.5, 10), minor_locator=MultipleLocator(1))

    major_locator = mdates.YearLocator(base=1)
    minor_locator = mdates.MonthLocator(interval=2)
    major_formatter = mdates.AutoDateFormatter(major_locator)
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_x_ticks(which='minor', length=3, width=1)
    chart.configure_x_ticks(which='major', length=20, width=1, pad=10)

    chart.add_horizontal_line(axis_index=0)
    chart.add_data(x=df1.index, y=df1['y'], label="Headline YoY", y_axis=0, transformer=Pct(periods=12))
    chart.add_data(x=df2.index, y=df2['y'], label="Core YoY", y_axis=0, transformer=Pct(periods=12))

    chart.add_data(x=food_df.index, y=food_df['y'], chart_type='bar', stacked=True, label="Food", y_axis=0,
                   transformer=Pct(periods=1))
    chart.add_data(x=energy_df.index, y=energy_df['y'], chart_type='bar', stacked=True, label="Energy",
                   y_axis=0, transformer=Pct(periods=1))
    chart.add_data(x=food_df.index, y=food_df['y'], chart_type='bar', stacked=True, label="Food 2", y_axis=0,
                   transformer=Pct(periods=1))

    chart.legend(frameon=False, ncol=2)
    chart.plot(path="output/cpi2.png")
