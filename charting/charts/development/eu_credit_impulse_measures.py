import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    credit_impulse_df, credit_impulse_title = blp.get_series(series_id="BCMPCIGD Index", observation_start="19990101")
    credit_impulse_hh_df, credit_impulse_hh_title = blp.get_series(series_id="BCMPCIHN Index",
                                                                   observation_start="19990101")
    credit_impulse_ps_df, credit_impulse_ps_title = blp.get_series(series_id="BCMPCIPD Index",
                                                                   observation_start="19990101")

    title = "EU Credit Impulse"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_credit_impulse_measures_yoy.png")
    chart.configure_y_axis( label="%")

    chart.add_series(credit_impulse_df.index, credit_impulse_df['y'], label=credit_impulse_title)
    chart.add_series(credit_impulse_hh_df.index, credit_impulse_hh_df['y'], label=credit_impulse_hh_title)
    chart.add_series(credit_impulse_ps_df.index, credit_impulse_ps_df['y'], label=credit_impulse_ps_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
