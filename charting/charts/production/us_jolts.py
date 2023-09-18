import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.fred_source import FredSource
from source_engine.indeed_source import IndeedSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.lag import Lag
from charting.transformer.lead import Lead


def main():
    fred = FredSource()
    indeed = IndeedSource()
    d0, t0 = fred.get_series(series_id="JTSJOL", observation_start="2019-06-01")
    percentage_change = (d0['y'] / d0['y'][0]) * 100

    d1, t1 = indeed.get_series(series_id="US")

    title = "JOLTs job openings likely eased moderately"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="us_jolts.png", metadata=metadata)

    chart.configure_y_axis(y_axis_index=0, minor_locator=MultipleLocator(5), major_locator=MultipleLocator(10))

    chart.add_sup_y_label(label="%")

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=3)
    major_formatter = mdates.DateFormatter("%b-%Y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator,
                           major_locator=major_locator)

    chart.add_series(d0.index, percentage_change, label=t0, transformer=Lead(offset=DateOffset(months=1)))
    chart.add_series(d1.index, d1["indeed_job_postings_index_SA"].values, label="Indeed, Seasonally Adjusted")
    chart.add_horizontal_line(y=100)

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()

