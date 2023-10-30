import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.lead import Lead


def main():
    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='MUVIYOY Index', observation_start='20200101')
    d2, t2 = blp.get_series(series_id='MUVIMOM Index', observation_start='20200101')
    d3, t3 = blp.get_series(series_id='CPRTUCT% Index', observation_start='20200101')

    title = "Manheim US Vehicle Inflation"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="us_vehicle_inflation.png", num_y_axis=2)

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", y_lim=(-55, 55), minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(10))
    chart.configure_y_axis(y_axis_index=1, label="Percentage Points", y_lim=(-15, 15), minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(5))

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=6)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d2.index, y=d2['y'], label="Manheim US Used Vehicle Value (MoM)", chart_type='bar', alpha=0.7,
                     y_axis_index=1, transformer=Lead(offset=DateOffset(months=2)))
    chart.add_series(x=d1.index, y=d1['y'], label="Manheim US Used Vehicle Value (YoY)",
                     transformer=Lead(offset=DateOffset(months=2)))
    chart.add_series(x=d3.index, y=d3['y'], label=t3)

    chart.add_horizontal_line()
    chart.add_last_value_badge()
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()

