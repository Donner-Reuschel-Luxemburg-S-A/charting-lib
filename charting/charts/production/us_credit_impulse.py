import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19290101"
    credit_impulse_df, credit_impulse_title = blp.get_series(series_id="BCMPCIUS Index", observation_start=start_time)
    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Credit Impulse"
    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)

    chart = Chart(title=title, metadata=metadata, filename="us_credit_impulse_measures_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5),
                           label="Percentage Points")

    chart.add_series(credit_impulse_df.index, credit_impulse_df['y'], label=credit_impulse_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
