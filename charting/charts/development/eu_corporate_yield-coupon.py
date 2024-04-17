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

    corp_ytw_df, corp_ytw_title = blp.get_series(series_id="LECPSTAT Index",field="YIELD_TO_WORST", observation_start="19900101")
    corp_cpn_df, corp_cpn_title = blp.get_series(series_id="LECPSTAT Index",field="CPN", observation_start="19900101")

    hy_ytw_df, hy_ytw_title = blp.get_series(series_id="LP01TREU Index", field="YIELD_TO_WORST", observation_start="19900101")
    hy_cpn_df, hy_cpn_title = blp.get_series(series_id="LP01TREU Index", field="CPN", observation_start="19900101")

    title = "Euro IG Corporates Refinancing Costs"
    #title = "Euro Unternehmensanleihen: Refinanzierungskosten"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="eu_corporate_yield-coupon.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(0.5), major_locator=MultipleLocator(1), label="%")

    chart.add_series(corp_ytw_df.index, corp_ytw_df['y']-corp_cpn_df['y'], label="Euro IG Corporates: Yield to Worst minus Coupon")


    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.plot()

    title = "Euro HY Corporates Refinancing Costs"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="eu_hy_yield-coupon.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(0.5), major_locator=MultipleLocator(1), label="%")

    chart.add_series(hy_ytw_df.index, hy_ytw_df['y']-hy_cpn_df['y'], label="Euro HY Corporates: Yield to Worst minus Coupon")


    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.plot()




if __name__ == '__main__':
    main()
