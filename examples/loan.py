import pandas as pd
from charting.charts.time_series_chart import TimeSeriesChart
import matplotlib.dates as mdates
from charting.transformer.center import Center
from examples import fred

if __name__ == '__main__':
    d1, t1, a1 = fred.get_series(series_id='DRTSCILM')  # DRTSCILM
    pmi = pd.read_excel('resources/us-pmi.xlsx', header=5, parse_dates=['Dates'], index_col='Dates')
    d2, t2, a2 = fred.get_series(series_id='JHDUSRGDPBR')  # USRINDEX Index

    chart = TimeSeriesChart(title="As industrial loan standards tighten, manufacturing contracts",
                            figsize=(14, 6), num_y_axes=2)

    chart.configure_y_axis(axis_index=0, label="PMI Index", y_lim=(20, 65))
    chart.configure_y_axis(axis_index=1, label=a1, y_lim=(80, -40), invert_axis=True)

    major_locator = mdates.YearLocator(base=2)
    major_formatter = mdates.AutoDateFormatter(major_locator)
    chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)

    chart.add_data(pmi.index, pmi['PX_LAST'], label="US Manufacturing PMI", chart_type='bar',
                   y_axis=0, bar_bottom=50, transformer=Center(val=50), alpha=0.7)
    chart.add_data(x=d1.index, y=d1['y'], label="Tightening standards for C&I loans", y_axis=1)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")
    chart.add_horizontal_line(y=0, axis_index=1)

    chart.legend(frameon=False, ncol=3)
    chart.plot(path="output/loan.png")
