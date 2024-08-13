import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.transformer.lag import Lag


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "20120101"

    ism_manu_df, ism_manu_title = blp.get_series(series_id="NAPMPRIC Index", observation_start=start_time)
    ism_serv_df, ism_serv_title = blp.get_series(series_id="NAPMNPRC Index", observation_start=start_time)

    cpi_df, cpi_title = blp.get_series(series_id="CPI YOY Index", observation_start=start_time)

    cpi_serv_df, cpi_serv_title = blp.get_series(series_id="CPUPSXEN Index", observation_start=start_time)

    title = "US ISM Man. Prices Paid vs. CPI"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="cpi_ism_manu.jpeg", num_rows=1, num_y_axis=2)

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(ism_manu_df.index, ism_manu_df['y'], label=ism_manu_title, y_axis_index=1,
                     transformer=[Lag(DateOffset(months=-2))])

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot(upload_chart='observation_start' not in kwargs)

    title = "US ISM Serv./Man. Prices Paid vs. CPI"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="cpi_ism_serv.jpeg", num_rows=1, num_y_axis=2)


    # chart.add_series(cpi_serv_df.index, cpi_serv_df['y'], label=cpi_serv_title,transformer=[Pct(periods=12)])
    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(ism_serv_df.index, ism_serv_df['y'], label=ism_serv_title, y_axis_index=1,
                     transformer=[Lag(DateOffset(months=-2))])

    chart.add_horizontal_line(y=2)
    chart.legend(ncol=2)
    chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
