import datetime

from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region

DEFAULT_START_DATE = datetime.date(1970, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    nfp_df, nfp_title = blp.get_series(series_id="CANLNETJ Index",
                                       observation_start=observation_start.strftime("%Y%m%d"),
                                       observation_end=observation_end.strftime("%Y%m%d"))

    title = "Canada Employment Change YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="ca_payrolls_yoy.jpeg", metadata=metadata)

    nfp_df['z'] = nfp_df['y'].rolling(12).sum()
    nfp_df = nfp_df.iloc[12:, ]

    chart.add_series(nfp_df.index, nfp_df['z'], label=nfp_title)

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    chart.add_last_value_badge(decimals=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
