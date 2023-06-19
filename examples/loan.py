import pandas as pd
from charting.charts.time_series_chart import TimeSeriesChart
import matplotlib.dates as mdates

from charting.transformer.center import Center

if __name__ == '__main__':
    df = pd.read_csv('resources/DRTSCILM.csv', header=0, parse_dates=['DATE'], index_col='DATE')
    pmi = pd.read_excel('resources/us-pmi.xlsx', header=5, parse_dates=['Dates'], index_col='Dates')
    rec = pd.read_excel('resources/us-recession.xlsx', header=5, parse_dates=['Dates'], index_col='Dates')

    chart = TimeSeriesChart(title="As industrial loan standards tighten, manufacturing contracts",
                            figsize=(14, 6), num_y_axes=2)

    chart.configure_y_axis(axis_index=0, label="PMI Index", y_lim=(20, 65))
    chart.configure_y_axis(axis_index=1, label="%", y_lim=(80, -40), invert_axis=True)

    major_locator = mdates.YearLocator(base=2)
    major_formatter = mdates.AutoDateFormatter(major_locator)
    chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)

    chart.add_data(pmi.index, pmi['PX_LAST'], label="US Manufacturing PMI", chart_type='bar',
                   y_axis=0, bar_bottom=50, transformer=Center(val=50), alpha=0.7)
    chart.add_data(df.index, df['DRTSCILM'], label="Tightening standards for C&I loans", y_axis=1)
    chart.add_horizontal_line(y=0, axis_index=1)
    chart.add_vertical_line(x=rec.index, y=rec["PX_LAST"], label="US Recession")

    chart.legend(frameon=False, ncol=3)
    chart.plot(path="output/loan.png")
