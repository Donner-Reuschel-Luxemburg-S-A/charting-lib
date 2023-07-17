import matplotlib.dates as mdates
from pandas import DateOffset

from charting.model.chart import Chart
from charting import blp
from charting.model.metadata import Metadata, Country, Category
from charting.transformer.lead import Lead

if __name__ == '__main__':
    d1, t1 = blp.get_series(series_id='MUVIYOY Index', observation_start=19950101)
    d2, t2 = blp.get_series(series_id='MUVIMOM Index', observation_start=19950101)
    d3, t3 = blp.get_series(series_id='CPRTUCT% Index', observation_start=19950101)

    title = "Manheim US Vehicle Inflation"
    metadata = Metadata(title=title, country=Country.US, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="us_vehicle_inflation.png", num_y_axis=2)

    chart.configure_y_axis(y_axis_index=0, label="%", y_lim=(-50, 50))
    chart.configure_y_axis(y_axis_index=1, label="%", y_lim=(-15, 15))

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=4)
    major_formatter = mdates.AutoDateFormatter(major_locator)
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label="Manheim US Used Vehicle Value (YoY)")
    chart.add_series(x=d3.index, y=d3['y'], label=t3, transformer=Lead(offset=DateOffset(months=2)))
    chart.add_series(x=d2.index, y=d2['y'], label="Manheim US Used Vehicle Value (MoM)", chart_type='bar', alpha=0.7,
                     y_axis_index=1)

    chart.add_horizontal_line()

    chart.legend(ncol=2)
    chart.plot()
