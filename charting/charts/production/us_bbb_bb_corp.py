import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()
    df, t = blp.get_series(series_id='I00182US Index', observation_start='20140101', field='BX218')
    df2, t2 = blp.get_series(series_id='LCB1TRUU Index', observation_start='20140101', field='BX218')
    title = 'US BB - BBB Spread'
    t = 'Bloomberg Ba US High Yield  TR Index Value Unhedged USD'
    t2 = 'Bloomberg Baa Corporate Total Return Index Value Unhedged USD'
    metadata = Metadata(title=title, region=Region.EU, category=Category.CREDIT)
    common_index = pd.DatetimeIndex(set(df.index).intersection(set(df2.index))).sort_values()
    chart = Chart(title=title, num_rows=2, filename=__name__ + ".png", metadata=metadata)
    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)
    chart.configure_y_axis(y_axis_index=0, row_index=0, label='Spread BPS vs Tsy', minor_locator=MultipleLocator(50),
                           major_locator=MultipleLocator(100))
    chart.configure_y_axis(y_axis_index=0, row_index=1, label='Spread Difference BPS',
                           minor_locator=MultipleLocator(25),
                           major_locator=MultipleLocator(50))
    chart.add_series(x=common_index, y=df.loc[common_index]['y'], label=t)
    chart.add_series(x=common_index, y=df2.loc[common_index]['y'], label=t2)
    chart.add_series(x=common_index, y=(df.loc[common_index] - df2.loc[common_index])['y'], row_index=1, label=title)
    chart.add_horizontal_line(row_index=1, y_axis_index=0, y=0)
    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
