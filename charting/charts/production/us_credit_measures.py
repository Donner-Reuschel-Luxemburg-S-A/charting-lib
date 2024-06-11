import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.pct import Pct


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19700101"
    bankcredit_df, bankcredit_title = fred.get_series(series_id="LOANINV", observation_start=start_time)
    ci_loans_df, ci_loans_title = fred.get_series(series_id="BUSLOANS", observation_start=start_time)
    consumer_loans_df, consumer_loans_title = fred.get_series(series_id="CONSUMER", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Credit Measures"
    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)

    chart = Chart(title=title, metadata=metadata, filename="us_credit_measures.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(10), major_locator=MultipleLocator(50),
                           label="Percentage Points")

    chart.add_series(bankcredit_df.index, bankcredit_df['y'], label=bankcredit_title, transformer=[Pct(12)])
    chart.add_series(ci_loans_df.index, ci_loans_df['y'], label=ci_loans_title, transformer=[Pct(12)])
    chart.add_series(consumer_loans_df.index, consumer_loans_df['y'], label=consumer_loans_title, transformer=[Pct(12)])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
