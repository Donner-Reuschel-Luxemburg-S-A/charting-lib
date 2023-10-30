import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata
from charting.transformer.lead import Lead
from charting.transformer.resample import Resample


def main():
    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='SBOIPRIC Index', observation_start='19950131')
    df2, t2 = blp.get_series(series_id='CLEVCPIA Index', observation_start='19950131')

    title = "NFIB Small Business Higher Prices & Nat'l Fed. of Ind. Business"
    metadata = Metadata(title=title, region=Region.US, category=[Category.INFLATION, Category.SURVEY])
    chart = Chart(title=title, metadata=metadata, num_y_axis=2, filename="us_nfib_cpi.png")

    chart.configure_y_axis(y_axis_index=0, label="Last Price [€]", y_lim=(-35, 70), minor_locator=MultipleLocator(10))
    chart.configure_y_axis(y_axis_index=1, label="Last Price [€]", minor_locator=MultipleLocator(0.5))

    major_locator = mdates.YearLocator(base=5)
    minor_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0, fill=True,
                     fill_threshold=-35, transformer=[Resample('M'), Lead(offset=DateOffset(months=10))])
    chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=1,  transformer=Resample('M'))

    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()


