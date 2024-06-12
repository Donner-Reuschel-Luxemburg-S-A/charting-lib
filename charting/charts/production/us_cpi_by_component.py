import datetime

import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.pct import Pct


DEFAULT_START_DATE = datetime.date(2019, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()
    headline_df, headline_title = fred.get_series(series_id='CPIAUCSL', observation_start=observation_start.strftime("%Y-%m-%d"),
                           observation_end=observation_end.strftime("%Y-%m-%d"))
    core_df, core_title = fred.get_series(series_id='CPILFESL', observation_start=observation_start.strftime("%Y-%m-%d"),
                           observation_end=observation_end.strftime("%Y-%m-%d"))

    food_df, _ = blp.get_series(series_id='CPSFFOOD Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    x, y = Pct(periods=12).transform(food_df.index, food_df['y'])
    food_df = DataFrame({'y': y}, index=x)
    food_weights_df, _ = blp.get_series(series_id='CPIVFOOD Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    food_df['weighted'] = food_df['y'] * food_weights_df['y'].shift(12) / 100
    food_df.index = food_df.index.to_period('M').to_timestamp(how='start')

    energy_df, _ = blp.get_series(series_id='CPUPENER Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    energy_weights_df, _ = blp.get_series(series_id='CPIVENER Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    x, y = Pct(periods=12).transform(energy_df.index, energy_df['y'])
    energy_df = DataFrame({'y': y}, index=x)
    energy_df['weighted'] = energy_df['y'] * energy_weights_df['y'].shift(12) / 100
    energy_df.index = energy_df.index.to_period('M').to_timestamp(how='start')

    goods_df, _ = blp.get_series(series_id='CPUPCXFE Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    goods_weights_df, _ = blp.get_series(series_id='CPIVCLFE Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    x, y = Pct(periods=12).transform(goods_df.index, goods_df['y'])
    goods_df = DataFrame({'y': y}, index=x)
    goods_df['weighted'] = goods_df['y'] * goods_weights_df['y'].shift(12) / 100
    goods_df.index = goods_df.index.to_period('M').to_timestamp(how='start')

    services_df, _ = blp.get_series(series_id='CPUPSXEN Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    services_weights_df, _ = blp.get_series(series_id='CPIVSLES Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    x, y = Pct(periods=12).transform(services_df.index, services_df['y'])
    services_df = DataFrame({'y': y}, index=x)
    services_df['weighted'] = services_df['y'] * services_weights_df['y'].shift(12) / 100
    services_df.index = services_df.index.to_period('M').to_timestamp(how='start')

    title = "U.S. CPI by Component"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="us_cpi_by_component.png")

    chart.configure_y_axis(label="Percentage Points", y_lim=(-2.5, 10))

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

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
