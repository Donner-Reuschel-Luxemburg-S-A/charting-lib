
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region


def main():
    blp = BloombergSource()

    m1_df, m1_title = blp.get_series(series_id="ECMAM1YY Index", observation_start="19990101")
    m2_df, m2_title = blp.get_series(series_id="ECMAM2YY Index", observation_start="19990101")
    m3_df, m3_title = blp.get_series(series_id="ECMAM3YY Index", observation_start="19990101")

    title = "EU Money Supply Measures YoY"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_money_measures_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(m1_df.index, m1_df['y'], label=m1_title)
    chart.add_series(m2_df.index, m2_df['y'], label=m2_title)
    chart.add_series(m3_df.index, m3_df['y'], label=m3_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.plot()


if __name__ == '__main__':
    main()
