
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.pct import Pct


def main():
    fred = FredSource()

    us, us_title = fred.get_series(series_id='CPIAUCSL', observation_start='2000-01-01')
    de, de_title = fred.get_series(series_id='DEUCPALTT01CTGYM', observation_start='2000-01-01')
    jp, jp_title = fred.get_series(series_id='JPNCPIALLMINMEI', observation_start='2000-01-01')
    uk, uk_title = fred.get_series(series_id='GBRCPALTT01CTGYM', observation_start='2000-01-01')
    ch, ch_title = fred.get_series(series_id='CPALTT01CNM659N', observation_start='2000-01-01')

    us = (us.pct_change(periods=12) * 100).shift(1)
    jp = (jp.pct_change(periods=12) * 100).shift(1)

    title = "Inflation Trend"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="global_inflation.png")

    chart.configure_y_axis(y_axis_index=0, label="%", minor_locator=MultipleLocator(1), y_lim=(-2.5, 10))

    major_locator = mdates.YearLocator(base=2)
    minor_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.AutoDateFormatter(major_locator)
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_horizontal_line(y_axis_index=0)

    chart.add_series(x=us.index, y=us['y'], label="U.S.")
    chart.add_series(x=de.index, y=de['y'], label="Germany")
    chart.add_series(x=jp.index, y=jp['y'], label="Japan")
    chart.add_series(x=uk.index, y=uk['y'], label="UK")
    chart.add_series(x=ch.index, y=ch['y'], label="China")

    chart.legend(ncol=4)
    chart.plot()


if __name__ == '__main__':
    main()

