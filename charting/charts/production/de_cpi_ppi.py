import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(1992, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    cpi_df, cpi_title = blp.get_series(series_id="GRCP20YY Index",
                                       observation_start=observation_start.strftime("%Y%m%d"),
                                       observation_end=observation_end.strftime("%Y%m%d"))
    ppi_df, ppi_title = blp.get_series(series_id="GRPFIYOY Index",
                                       observation_start=observation_start.strftime("%Y%m%d"),
                                       observation_end=observation_end.strftime("%Y%m%d"))
    wpi_df, wpi_title = blp.get_series(series_id="GRWPYOYI Index",
                                       observation_start=observation_start.strftime("%Y%m%d"),
                                       observation_end=observation_end.strftime("%Y%m%d"))

    title = "Germany: Producer, Wholesale and Consumer Inflation"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="de_cpi_ppi.png")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="Percentage Points")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(ppi_df.index, ppi_df['y'], label=ppi_title)
    chart.add_series(wpi_df.index, wpi_df['y'], label=wpi_title)

    chart.add_horizontal_line()
    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
