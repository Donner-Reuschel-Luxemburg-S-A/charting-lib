import datetime

import matplotlib.dates as mdates
from source_engine.sdmx_source import Ecb

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region

DEFAULT_START_DATE = datetime.date(2017, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    source = Ecb()
    df1, t1 = source.get_data(flow_ref="EXR", key='D.JPY.EUR.SP00.A',
                              parameters={'startPeriod': observation_start.strftime("%Y-%m-%d"),
                                          'endPeriod': observation_end.strftime("%Y-%m-%d")}
                              )

    title = "Japanese Yen ¥"
    metadata = Metadata(title=title, region=[Region.EU, Region.DE, Region.JP], category=Category.FX)

    chart = Chart(title=title, metadata=metadata, filename="currency_eur_jpy", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(label="JPY ¥")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label='ECB reference exchange rate, EUR/JPY')
    chart.add_last_value_badge(decimals=2)

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
