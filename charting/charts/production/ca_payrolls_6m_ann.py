import datetime

from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg

DEFAULT_START_DATE = datetime.date(1970, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    nfp_df, nfp_title = blp.get_series(series_id="CANLNETJ Index",
                                       observation_start=observation_start.strftime("%Y%m%d"),
                                       observation_end=observation_end.strftime("%Y%m%d"))

    title = "Canada Employment Change 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="ca_payrolls_mom_6.png", metadata=metadata)

    df = nfp_df.iloc[6:, ]
    chart.add_series(df.index, df['y'] * 12, label=nfp_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    chart.add_last_value_badge(decimals=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
