import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset

from charting.model.chart import Chart
from charting import blp, fred
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg


def main():
    df1, t1 = blp.get_series(series_id='INJCJC Index', observation_start='19800101')
    df2, t2 = blp.get_series(series_id='SBOIHIRE Index', observation_start='19800101')
    df3, t3 = fred.get_series(series_id='JHDUSRGDPBR')

    title = "Small Business hiring plans point to higher jobless claims"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, num_y_axis=2, metadata=metadata, filename="us_nfib_jobless_claims.png")

    chart.configure_y_axis(y_axis_index=0, label="Thousands", y_lim=(100, 800), minor_locator=MultipleLocator(50))
    chart.configure_y_axis(y_axis_index=1, label="%", y_lim=(-20, 30), reverse_axis=True,
                           minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    major_locator = mdates.YearLocator(base=3)
    minor_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.DateFormatter("%Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0, transformer=Avg(offset=DateOffset(months=1)))
    chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=1)
    chart.add_vertical_line(x=df3.index, y=df3["y"], label="US Recession")

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()

