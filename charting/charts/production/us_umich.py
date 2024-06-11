import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19780101"

    sentiment_df, sentiment_title = blp.get_series(series_id="CONSSENT Index", observation_start=start_time)
    expectations_df, expectations_title = blp.get_series(series_id="CONSEXP Index", observation_start=start_time)
    conditions_df, conditions_title = blp.get_series(series_id="CONSCURR Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US University Michigan Surveys"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_umich_surveys.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5),
                           label="Percentage Points")

    chart.add_series(sentiment_df.index, sentiment_df['y'], label=sentiment_title)
    chart.add_series(expectations_df.index, expectations_df['y'], label=expectations_title)
    chart.add_series(conditions_df.index, conditions_df['y'], label=conditions_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=100)
    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
