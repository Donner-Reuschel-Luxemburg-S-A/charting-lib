import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg


def main():
    blp = BloombergSource()

    credit_corp_df, credit_corp_title = blp.get_series(series_id="MFIKNFG Index", observation_start="19990101")
    credit_hh_df, credit_hh_title = blp.get_series(series_id="MFIPHGS Index", observation_start="19990101")
    credit_impulse_df, credit_impulse_title = blp.get_series(series_id="BCMPCIGD Index", observation_start="19990101")
    credit_impulse_hh_df, credit_impulse_hh_title = blp.get_series(series_id="BCMPCIHN Index", observation_start="19990101")
    credit_impulse_ps_df, credit_impulse_ps_title = blp.get_series(series_id="BCMPCIPD Index", observation_start="19990101")

    title = "EU Credit Measures YoY"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="eu_credit_measures_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(credit_corp_df.index, credit_corp_df['y'], label=credit_corp_title)
    chart.add_series(credit_hh_df.index, credit_hh_df['y'], label=credit_hh_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.plot()

    title = "EU Credit Impulse"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="eu_credit_impulse_measures_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(credit_impulse_df.index, credit_impulse_df['y'], label=credit_impulse_title)
    chart.add_series(credit_impulse_hh_df.index, credit_impulse_hh_df['y'], label=credit_impulse_hh_title)
    chart.add_series(credit_impulse_ps_df.index, credit_impulse_ps_df['y'], label=credit_impulse_ps_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.plot()



if __name__ == '__main__':
    main()
