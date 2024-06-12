import datetime

import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


DEFAULT_START_DATE = datetime.date(1970, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()

    vehicle_sales_df, vehicle_sales_title = blp.get_series(series_id="SAARTOTL Index",
                                                           observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=observation_start.strftime("%Y-%m-%d"),
                            observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "US Vehicle Sales"
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_vehicle_sales.png", metadata=metadata)

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="Million Units")

    chart.add_series(vehicle_sales_df.index, vehicle_sales_df['y'], label=vehicle_sales_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
