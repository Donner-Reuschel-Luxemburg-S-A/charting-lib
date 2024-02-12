from matplotlib.ticker import MultipleLocator, NullLocator
from source_engine.bloomberg_source import BloombergSource
from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
import matplotlib.dates as mdates
import pandas as pd


def main():
    blp = BloombergSource()
    df, t = blp.get_series(series_id='QX3A Index', observation_start='20140101', field='SP039')
    df2, t2 = blp.get_series(series_id='I02561EU Index', observation_start='20140101', field='BX219')
    title = 'EUR Corporate BBB -German Covered Bonds'
    t = 'iBoxx Euro Germany Covered Total Return Index'
    t2 = 'Bloomberg Pan-European Aggregate: Corporate Baa Total Return'
    metadata = Metadata(title=title, region=Region.EU, category=Category.CREDIT)

    common_index = pd.DatetimeIndex(set(df.index).intersection(set(df2.index))).sort_values()

    chart = Chart(title=title, num_rows=2, num_y_axis=2, filename=__name__ + ".png", metadata=metadata)
    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)
    chart.configure_y_axis(y_axis_index=0, row_index=0, label='Spread BPS', minor_locator=MultipleLocator(50),
                           major_locator=MultipleLocator(100))
    chart.configure_y_axis(y_axis_index=1, row_index=0, label='Spread BPS', minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(10))
    chart.configure_y_axis(y_axis_index=0, row_index=1, label='Spread Difference BPS',
                           minor_locator=MultipleLocator(25),
                           major_locator=MultipleLocator(50))
    chart.add_series(x=common_index, y=df.loc[common_index]['y'], label=t, y_axis_index=1)
    chart.add_series(x=common_index, y=df2.loc[common_index]['y'], label=t2, y_axis_index=0)
    chart.add_series(x=common_index, y=(df2.loc[common_index] - df.loc[common_index])['y'], row_index=1, y_axis_index=0,
                     label=title)
    chart.configure_y_axis(label='', row_index=1, y_axis_index=1, major_locator=NullLocator())
    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()
