import datetime

import matplotlib.dates as mdates
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.pct import Pct

DEFAULT_START_DATE = datetime.date(1970, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    fred = FredSource()

    bankcredit_df, bankcredit_title = fred.get_series(series_id="LOANINV",
                                                      observation_start=observation_start.strftime("%Y-%m-%d"),
                                                      observation_end=observation_end.strftime("%Y-%m-%d"))
    ci_loans_df, ci_loans_title = fred.get_series(series_id="BUSLOANS",
                                                  observation_start=observation_start.strftime("%Y-%m-%d"),
                                                  observation_end=observation_end.strftime("%Y-%m-%d"))
    consumer_loans_df, consumer_loans_title = fred.get_series(series_id="CONSUMER",
                                                              observation_start=observation_start.strftime("%Y-%m-%d"),
                                                              observation_end=observation_end.strftime("%Y-%m-%d"))

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR',
                                                observation_start=observation_start.strftime("%Y-%m-%d"),
                                                observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "US Credit Measures"
    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)

    chart = Chart(title=title, metadata=metadata, filename="us_credit_measures.png")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="Percentage Points")

    chart.add_series(bankcredit_df.index, bankcredit_df['y'], label=bankcredit_title, transformer=[Pct(12)])
    chart.add_series(ci_loans_df.index, ci_loans_df['y'], label=ci_loans_title, transformer=[Pct(12)])
    chart.add_series(consumer_loans_df.index, consumer_loans_df['y'], label=consumer_loans_title, transformer=[Pct(12)])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line()
    chart.add_last_value_badge(decimals=2)
    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
