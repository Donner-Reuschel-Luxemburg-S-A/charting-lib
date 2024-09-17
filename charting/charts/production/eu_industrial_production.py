import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata

DEFAULT_START_DATE = datetime.date(1990, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    indprodcap_df, indprodcap_title = blp.get_series(series_id="EUIPCEZY Index",
                                                     observation_start=observation_start.strftime("%Y%m%d"),
                                                     observation_end=observation_end.strftime("%Y%m%d"))

    title = "Eurozone: Industrial Production YoY"
    metadata = Metadata(title=title, region=Region.EU, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_industrial_production", language=kwargs.get('language', 'en'))
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.add_series(indprodcap_df.index, indprodcap_df['y'], label=indprodcap_title)

    chart.add_horizontal_line()
    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
