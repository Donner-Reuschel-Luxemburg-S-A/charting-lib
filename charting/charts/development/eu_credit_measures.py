import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    credit_corp_df, credit_corp_title = blp.get_series(series_id="MFIKNFG Index", observation_start="19990101")
    credit_hh_df, credit_hh_title = blp.get_series(series_id="MFIPHGS Index", observation_start="19990101")

    title = "EU Credit Measures YoY"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_credit_measures_yoy.png")
    chart.configure_y_axis(label="%")

    chart.add_series(credit_corp_df.index, credit_corp_df['y'], label=credit_corp_title)
    chart.add_series(credit_hh_df.index, credit_hh_df['y'], label=credit_hh_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
