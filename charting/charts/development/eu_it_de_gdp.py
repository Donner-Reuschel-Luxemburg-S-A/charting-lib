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

    start_date = "20220201"

    it_gdp_df, it_gdp_title = blp.get_series(series_id="ITGLALEV Index",field="PX_LAST", observation_start=start_date)
    de_gdp_df, de_gdp_title = blp.get_series(series_id="GRGDEGDP Index", field="PX_LAST", observation_start=start_date)



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
