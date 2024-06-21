import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.center import Center


def main():
    blp = BloombergSource()
    fred = FredSource()
    d1, t1 = fred.get_series(series_id='DRTSCILM')
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR')
    d3, t3 = blp.get_series(series_id='NAPMPMI Index', observation_start='19900131')

    title = "As industrial loan standards tighten, manufacturing contracts"
    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)
    chart = Chart(title=title, num_y_axis=2, metadata=metadata, filename="us_industrial_loan_tightening.png")

    chart.configure_y_axis(y_axis_index=0, label="PMI Index", y_lim=(20, 65))
    chart.configure_y_axis(y_axis_index=1, label="Percentage Points", reverse_axis=True)

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=4)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label="Tightening standards for C&I loans", y_axis_index=1)
    chart.add_series(x=d3.index, y=d3['y'], label=t3, chart_type='bar', y_axis_index=0, bar_bottom=50,
                     transformer=Center(val=50), alpha=0.7)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")
    chart.add_horizontal_line(y_axis_index=1)

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
