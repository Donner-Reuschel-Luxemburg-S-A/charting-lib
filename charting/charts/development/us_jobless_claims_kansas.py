import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.transformer.invert import Invert
from charting.transformer.lag import Lag


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19600101"

    jc_df, jc_title = blp.get_series(series_id="INJCJC Index", observation_start="20190101")
    kf_df, kf_title = blp.get_series(series_id="KCMTLMCI Index", observation_start="20190101")

    title = "US Jobless Claims vs. Kansas Fed Labor Market Conditions"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_jobless_claims_kansas.jpeg", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(1000), major_locator=MultipleLocator(1000), label="")

    chart.add_series(jc_df.index, jc_df['y'], label=jc_title, y_axis_index=0, transformer=[Lag(DateOffset(months=-1))])
    chart.add_series(kf_df.index, kf_df['y'], label=kf_title, transformer=[Invert()], y_axis_index=1)

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
