from charting.model.chart import Chart
from charting.model.metadata import Category, Country, Metadata
from examples import blp
import matplotlib.dates as mdates

if __name__ == '__main__':
    title = "German food inflation and price expectations of food manufacturers"

    metadata = Metadata(title=title, country=Country.DE, category=Category.INFLATION)

    d1, t1 = blp.get_series(series_id='GMFDDSE3 Index')
    d2, t2 = blp.get_series(series_id='GRCPH11Y Index')

    chart = Chart(title=title, metadata=metadata, num_y_axis=2, filename="german_food_inflation.png")

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=5)
    major_formatter = mdates.DateFormatter(fmt="%Y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(y_axis_index=0, label="Index", y_lim=(-5, 22.5))
    chart.configure_y_axis(y_axis_index=1, label="Index", y_lim=(-20, 90))

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_series(x=d2.index, y=d2['y'], label=t2)

    chart.legend()
    chart.plot()
