import datetime

import matplotlib.dates as mdates
from source_engine.sdmx_source import Bbk, Ecb

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata
from charting.transformer.pct import Pct

DEFAULT_START_DATE = datetime.date(2006, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    bbk = Bbk()
    estat = Ecb()
    d1, t1 = bbk.get_data(flow_ref="BBXP1", key="M.U2.N.HICP.000000.IND.I00",
                          parameters={'startPeriod': observation_start.strftime("%Y-%m"),
                                      'endPeriod': observation_end.strftime("%Y-%m")})
    d2, t2 = estat.get_data(flow_ref="ICP", key="M.U2.N.XEF000.4.INX",
                            parameters={'startPeriod': observation_start.strftime("%Y-%m"),
                                        'endPeriod': observation_end.strftime("%Y-%m")})

    d1['y'] = d1['y'].astype(float)
    d2['y'] = d2['y'].astype(float)

    title = "Eurozone inflation"
    metadata = Metadata(title=title, region=Region.EU, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_cpi_pmi.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1['y'], label="Eurozone Harmonized CPI", transformer=Pct(periods=12))
    chart.add_series(x=d2.index, y=d2['y'], label="Eurozone Harmonized CPI ex. Energy, Food, Alcohol and Tabacco",
                     transformer=Pct(periods=12))
    chart.add_horizontal_line(y=2)
    chart.add_last_value_badge()
    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
