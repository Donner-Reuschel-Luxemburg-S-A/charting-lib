import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from source_engine.bloomberg_source import BloombergSource

from charting.model import style
from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.model.style import colors

DEFAULT_START_DATE = datetime.datetime.today() - relativedelta(years=10)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    df2, t2 = blp.get_series(series_id='I02177EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX218')

    df4, t4 = blp.get_series(series_id='I09502EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX219')

    title = "Securitized & Agency Spreads"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)

    chart = Chart(title=title, num_rows=2, metadata=metadata, filename="securitzed_spreads", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(row_index=0, label="BPS")
    chart.configure_y_axis(row_index=1, label="BPS")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    mean_val = [df2['y'].mean()] * len(df2.index)
    chart.add_series(row_index=0, x=df2.index, y=df2['y'], label="Securitized")
    chart.add_series(row_index=0, x=df2.index, y=mean_val, label="Securitized - 10Y Avg", linestyle="--", color=style.get_color(0))

    mean_val = [df4['y'].mean()] * len(df4.index)
    chart.add_series(row_index=1, x=df4.index, y=df4['y'], label="Agency", color=style.get_color(1))
    chart.add_series(row_index=1, x=df4.index, y=mean_val, label="Agency - 10Y Avg", linestyle="--", color=style.get_color(1))

    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
