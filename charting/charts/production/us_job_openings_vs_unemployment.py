from matplotlib.ticker import MultipleLocator
from pandas import DateOffset

import matplotlib.dates as mdates

from charting.model.chart import Chart
from charting import fred
from charting.model.metadata import Metadata, Region, Category

def main():
    d1, t1 = fred.get_series(series_id='JTSJOL', observation_start="2000-12-01")
    d2, t2 = fred.get_series(series_id='UNRATE', observation_start="2000-12-01")
    d3, t3 = fred.get_series(series_id='JHDUSRGDPBR')

    title = "Job Openings (Total Nonfarm) vs. Unemployment Rate"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)
    chart = Chart(title=title, metadata=metadata, filename="us_job_openings_vs_unemployment.png", num_y_axis=2)

    chart.configure_y_axis(y_axis_index=0, label="Level in Thousands", minor_locator=MultipleLocator(500),
                           major_locator=MultipleLocator(1000))
    chart.configure_y_axis(y_axis_index=1, label="%", minor_locator=MultipleLocator(0.5),
                           major_locator=MultipleLocator(1))

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=3)
    major_formatter = mdates.DateFormatter("%Y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1, y_axis_index=0, invert=True)
    chart.add_series(x=d2.index, y=d2['y'], label=t2, y_axis_index=1)
    chart.add_vertical_line(x=d3.index, y=d3["y"], label="US Recession")

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()

