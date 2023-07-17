import matplotlib.dates as mdates

from charting.model.chart import Chart
from charting.transformer.center import Center
from charting import fred, blp

if __name__ == '__main__':
    d1, t1 = blp.get_series(series_id='MUVIYOY Index', observation_start=19900131)
    d2, t2 = blp.get_series(series_id='MUVIMOM Index', observation_start=19900131)
    d3, t3 = blp.get_series(series_id='CPRTUCT% Index', observation_start=19900131)

    chart = Chart(title="US Inflation",  filename="us_muv_inflation.png")

    chart.configure_y_axis(y_axis_index=0, label="Index")

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=4)
    major_formatter = mdates.AutoDateFormatter(major_locator)
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_series(x=d2.index, y=d2['y'], label=t2, chart_type='bar', alpha=0.7)
    chart.add_series(x=d3.index, y=d3["y"], label=t3)

    chart.add_horizontal_line()

    chart.legend(ncol=2)
    chart.plot()
