from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
import matplotlib.dates as mdates


def main():
    blp = BloombergSource()
    df, t = blp.get_series(series_id='I05446EU Index', observation_start='20200101', field='BX219')
    df2, t2 = blp.get_series(series_id='I02561EU Index', observation_start='20200101', field='BX219')
    title = 'EUR Corporate BBB - BB Spread'
    t = 'Bloomberg Pan-Euro HY BB Rating Only Total Return Index Unhedged'
    t2 = 'Bloomberg Pan-European Aggregate: Corporate Baa Total Return'
    metadata = Metadata(title=title, region=Region.EU, category=Category.CREDIT)

    chart = Chart(title=title, num_rows=2,  metadata=metadata, filename=__name__ + ".png")
    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator,major_locator=major_locator)
    chart.configure_y_axis(y_axis_index=0, row_index=0, label='Spread BPS', minor_locator=MultipleLocator(50),
                           major_locator=MultipleLocator(100))
    chart.configure_y_axis(y_axis_index=0, row_index=1, label='Spread Difference BPS', minor_locator=MultipleLocator(25),
                           major_locator=MultipleLocator(50))
    chart.add_series(x=df.index, y=df['y'], label=t)
    chart.add_series(x=df2.index, y=df2['y'], label=t2)
    chart.add_series(x=df.index, y=(df-df2)['y'], row_index=1, label=title)
    chart.legend()
    chart.plot()

if __name__ == '__main__':
    main()