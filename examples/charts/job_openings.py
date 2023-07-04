from matplotlib.ticker import MultipleLocator
from pandas import DateOffset

from charting.model.chart import Chart
from charting.transformer.avg import Avg
from charting.transformer.center import Center
from charting.transformer.pct import Pct
from charting.transformer.resample import Resample
from examples import fred
import matplotlib.dates as mdates

if __name__ == '__main__':
    d0, t0 = fred.get_series(series_id='JHDUSRGDPBR', observation_start="2002-01-01")

    d1, t1 = fred.get_series(series_id="JTSJOL", observation_start="2002-01-01")
    d2, t2 = fred.get_series(series_id="JTS2300JOL", observation_start="2002-01-01")
    d3, t3 = fred.get_series(series_id="JTS3000JOL", observation_start="2002-01-01")

    chart = Chart(title="Job Openings", num_rows=3, num_y_axis=1)

    chart.configure_y_axis(row_index=0, y_axis_index=0,
                           minor_locator=MultipleLocator(1000), major_locator=MultipleLocator(2000))

    chart.configure_y_axis(row_index=1, y_axis_index=0,
                           minor_locator=MultipleLocator(50), major_locator=MultipleLocator(100))

    chart.configure_y_axis(row_index=2, y_axis_index=0,
                           minor_locator=MultipleLocator(100), major_locator=MultipleLocator(200))

    chart.add_sup_y_label(label="Level of Thousands")

    major_locator = mdates.YearLocator(base=2)
    minor_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.AutoDateFormatter(major_locator)

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator,
                           major_locator=major_locator)

    chart.add_vertical_line(x=d0.index, y=d0["y"], row_index=0, label="US Recession")
    chart.add_vertical_line(x=d0.index, y=d0["y"], row_index=1)
    chart.add_vertical_line(x=d0.index, y=d0["y"], row_index=2)

    chart.add_series(d1.index, d1["y"], row_index=0, label=t1, fill=True, fill_threshold=2000)
    chart.add_series(d2.index, d2["y"], row_index=1, label=t2, transformer=Center(val=250), fill=True, fill_threshold=0)
    chart.add_series(d3.index, d3["y"], row_index=2, chart_type='bar', label=t3,
                     transformer=Resample(rule='Y'))

    chart.legend(ncol=2)
    chart.plot("output/job-openings.png")
