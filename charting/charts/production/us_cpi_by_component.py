import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.pct import Pct


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()
    headline_df, headline_title = fred.get_series(series_id='CPIAUCSL', observation_start='2019-01-01')
    core_df, core_title = fred.get_series(series_id='CPILFESL', observation_start='2019-01-01')

    food_df, _ = blp.get_series(series_id='CPSFFOOD Index', observation_start='20190101')
    x, y = Pct(periods=12).transform(food_df.index, food_df['y'])
    food_df = DataFrame({'y': y}, index=x)
    food_weights_df, _ = blp.get_series(series_id='CPIVFOOD Index', observation_start='20190101')
    food_df['weighted'] = food_df['y'] * food_weights_df['y'].shift(12) / 100
    food_df.index = food_df.index.to_period('M').to_timestamp(how='start')

    energy_df, _ = blp.get_series(series_id='CPUPENER Index', observation_start='20190101')
    energy_weights_df, _ = blp.get_series(series_id='CPIVENER Index', observation_start='20190101')
    x, y = Pct(periods=12).transform(energy_df.index, energy_df['y'])
    energy_df = DataFrame({'y': y}, index=x)
    energy_df['weighted'] = energy_df['y'] * energy_weights_df['y'].shift(12) / 100
    energy_df.index = energy_df.index.to_period('M').to_timestamp(how='start')

    goods_df, _ = blp.get_series(series_id='CPUPCXFE Index', observation_start='20190101')
    goods_weights_df, _ = blp.get_series(series_id='CPIVCLFE Index', observation_start='20190101')
    x, y = Pct(periods=12).transform(goods_df.index, goods_df['y'])
    goods_df = DataFrame({'y': y}, index=x)
    goods_df['weighted'] = goods_df['y'] * goods_weights_df['y'].shift(12) / 100
    goods_df.index = goods_df.index.to_period('M').to_timestamp(how='start')

    services_df, _ = blp.get_series(series_id='CPUPSXEN Index', observation_start='20190101')
    services_weights_df, _ = blp.get_series(series_id='CPIVSLES Index', observation_start='20190101')
    x, y = Pct(periods=12).transform(services_df.index, services_df['y'])
    services_df = DataFrame({'y': y}, index=x)
    services_df['weighted'] = services_df['y'] * services_weights_df['y'].shift(12) / 100
    services_df.index = services_df.index.to_period('M').to_timestamp(how='start')

    title = "U.S. CPI by Component"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="us_cpi_by_component.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(1),
                           y_lim=(-2.5, 10))

    major_locator = mdates.YearLocator(base=1)
    minor_locator = mdates.MonthLocator(interval=2)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_horizontal_line(y_axis_index=0)

    chart.add_series(x=headline_df.index, y=headline_df['y'], label="Headline YoY", transformer=Pct(periods=12),
                     linewidth=2)
    chart.add_series(x=core_df.index, y=core_df['y'], label="Core YoY", transformer=Pct(periods=12), linewidth=2)

    chart.add_series(x=services_df.index, y=services_df['weighted'], chart_type='bar', stacked=True,
                     label="Services (Ex Food & Energy)")

    chart.add_series(x=goods_df.index, y=goods_df['weighted'], chart_type='bar', stacked=True,
                     label="Goods (Ex Food & Energy)")

    chart.add_series(x=food_df.index, y=food_df['weighted'], chart_type='bar', stacked=True, label="Food")

    chart.add_series(x=energy_df.index, y=energy_df['weighted'], chart_type='bar', stacked=True, label="Energy")

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
