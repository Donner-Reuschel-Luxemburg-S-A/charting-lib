import datetime

import matplotlib.dates as mdates
import pandas as pd
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag

DEFAULT_START_DATE = datetime.date(1976, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()
    credit_df, credit_title = fred.get_series(series_id="TOTBKCR",
                                              observation_start=observation_start.strftime("%Y-%m-%d"),
                                              observation_end=observation_end.strftime("%Y-%m-%d"))
    credit_df = credit_df.resample("QS").last()

    gdp_df, gdp_title = fred.get_series(series_id="GDP", observation_start=observation_start.strftime("%Y-%m-%d"),
                                        observation_end=observation_end.strftime("%Y-%m-%d"))
    cpi_df, cpi_title = blp.get_series(series_id="CPI YOY Index",
                                       observation_start=observation_start.strftime("%Y%m%d"),
                                       observation_end=observation_end.strftime("%Y%m%d"))

    credit_df = credit_df.pct_change(periods=4) * 100
    gdp_df = gdp_df.pct_change(periods=4) * 100

    final_df = credit_df - gdp_df

    title = "Bank Credit, GDP & CPI (YoY)"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="cpi_gdp.jpeg")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.add_series(final_df.index, final_df['y'], label="Credit/GDP Diff")
    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title, transformer=Lag(offset=pd.DateOffset(months=24)))

    chart.add_horizontal_line()
    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
