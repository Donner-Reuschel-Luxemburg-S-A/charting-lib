from charting.charts.time_series_chart import TimeSeriesChart
import matplotlib.dates as mdates
from charting.transformer.center import Center
from examples import fred, blp

if __name__ == '__main__':
    d1, t1 = fred.get_series(series_id='DRTSCILM')  # DRTSCILM
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR')  # USRINDEX Index
    d3, t3 = blp.get_series(series_id='NAPMPMI Index', observation_start=19900131)

    chart = TimeSeriesChart(title="As industrial loan standards tighten, manufacturing contracts", num_y_axes=2)

    chart.configure_y_axis(axis_index=0, label="PMI Index", y_lim=(20, 65))
    chart.configure_y_axis(axis_index=1, label="%", y_lim=(80, -40), invert_axis=True)

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=4)
    major_formatter = mdates.AutoDateFormatter(major_locator)
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_data(x=d1.index, y=d1['y'], label="Tightening standards for C&I loans", y_axis=1)
    chart.add_data(x=d3.index, y=d3['y'], label=t3, chart_type='bar',
                   y_axis=0, bar_bottom=50, transformer=Center(val=50), alpha=0.7)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")
    chart.add_horizontal_line(y=0, axis_index=1)

    chart.legend(frameon=False, ncol=2)
    chart.plot(path="output/loan.png")
